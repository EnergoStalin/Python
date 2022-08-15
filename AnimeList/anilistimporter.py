#!/usr/bin/env python

import requests, json, time, webbrowser, datetime
from yummyexporter import *

class CleverDict(dict):
    def __init__(self, dc):
        self.update(dc)

    def __getattr__(self, name):
        if(isinstance(self[name], dict)):
            return CleverDict(self[name])
        elif(name == "__str__"):
            return self.__str__()
        else:
            return self[name]

class AniList:
    class Token:
        options = {
            "client_id": 5718,
            "redirect_uri": "https://anilist.co/api/v2/oauth/pin",
        }
        file = "token.tk"
        cached = None

        @classmethod
        def CheckTimestamp(cls, res):
            return not(
                int(datetime.datetime.now().timestamp()) - int(res["timestamp"]) > int(res["expires_in"])
            )

        @classmethod
        def _GetToken(cls):
            url = f"https://anilist.co/api/v2/oauth/authorize?client_id={cls.options['client_id']}&redirect_uri={cls.options['redirect_uri']}&response_type=code"
            webbrowser.open_new_tab(url)
            access = input("Paste Token Here: ")

            return requests.post('https://anilist.co/api/v2/oauth/token',
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                json={
                    'grant_type': 'authorization_code',
                    'client_id': cls.options["client_id"],
                    'client_secret': cls.options["client_secret"],
                    'redirect_uri': cls.options["redirect_uri"], # http://example.com/callback
                    'code': access # The Authorization Code received previously
                }
            ).json()

        @classmethod
        def Load(cls):
            if cls.cached != None and cls.CheckTimestamp(cls.cached):
                return cls.cached["access_token"]

            with open(cls.file, "r") as f:
                res = json.load(f)
                if(cls.CheckTimestamp(res)):
                    cls.cached = res
                    return res["access_token"]

        @classmethod
        def Save(cls, data):
            with open(cls.file, "w+") as f:
                json.dump(data,f)

        #Performing oauth authorization and store access token
        @classmethod
        def GetToken(cls):
            try:
                return cls.Load()
            except:
                access = cls._GetToken()
                #Setting up timestamp
                access["timestamp"] = datetime.datetime.now().timestamp()

                cls.Save(access)

                return access["access_token"]
        
    Query = CleverDict({
        "search": '''
            query ($id: Int, $pn: Int, $search: String = "deadman wonderlan") {
                Page(page: $pn, perPage: 10)
                {
                    media(id: $id, search: $search) {
                        id
                        episodes
                        type
                        title
                        {
                            userPreferred
                        }
                    }
                }
            }
        ''',
        "add": '''
            mutation ($mediaId: Int, $progress: Int, $status: MediaListStatus) {
                SaveMediaListEntry(mediaId: $mediaId, progress: $progress, status: $status)
                {
                    mediaId
                    status
                    progress
                }
            }
        ''',
        "getUser": '''
            query ($id: Int, $search: String) {
                User(id: $id, name: $search) {
                    id
                }
            }
        ''',
        "getList": '''
            query ($id: Int, $type: MediaType) {
                MediaListCollection(userId: $id, type: $type)
                {
                    lists
                    {
                        status
                        entries {
                            progress
                            id
                            media
                            {
                                id
                                title
                                {
                                    userPreferred
                                }
                            }
                        }
                    }
                }
            }
        ''',
        "delete": '''
            mutation($id: Int)
            {
                DeleteMediaListEntry(id: $id)
                {
                    deleted
                }
            }
        '''
    })

    shiki = ShikimoriConverter().TryLoad()
    graphUrl = 'https://graphql.anilist.co'

    def Report(self, *args):
        self.update(*args, print)

    def Start(self):
        if AniList.shiki.eng.empty():
            AniList.shiki.Convert(self.Report).Save()
        else:
            self.batchUpdate(AniList.shiki.eng)

    def batchUpdate(self, collection):
        for tg, animes in collection.items():
            if tg == "LOVED":
                continue
            
            for anime in animes:
                self.update(tg, None, anime, print)

    def query(self, query, variables, reqAuth = False):
        headers = {}
        if(reqAuth):
            headers.update({
                'Authorization': 'Bearer ' + AniList.Token.GetToken(),
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            })
            
        #Perform query
        res = requests.post(
            AniList.graphUrl,
            json={'query': query, 'variables': variables},
            headers=headers
        )

        #Handle quota
        if(int(res.headers["X-RateLimit-Remaining"]) < 2):
            time.sleep(60)
        res = res.json()

        #Handle errors
        if "errors" in res:
            raise Exception(res["errors"])

        return CleverDict(res)

    #Get media id and handle quota per minute
    #extract quota to another method
    def GetMediaInfo(self, title_eng):
        res = None
        try:
            res = self.query(AniList.Query.search, {"search": title_eng})
        except Exception as ex:
            print(ex)
            return res

        for title in res.data.Page.media:
            if(title["type"] == "ANIME"):
                return CleverDict(title)
        return None

    def AddToList(self, status, res, info = None):
        variables = {
            "mediaId": res["id"],
            "status": status
        }

        if status != "CURRENT": # If not currently watching update progress if possible
            variables["progress"] = 0 if (res["episodes"] == None) else res["episodes"]

        if status == "PLANNING":
            variables["progress"] = 0

        #Add to list
        self.query(AniList.Query.add, variables, True)
            

    def update(self, category, title_rus, title_eng, info = None):
        if(not title_eng):
            return
        res = self.GetMediaInfo(title_eng)
        if res and res.type == "ANIME":
            try:
                self.AddToList(category, res, info)
                info("Success " + category + " " + str(res))
            except Exception as ex:
                if info:
                    info("Addition failed.")
                    info(ex)
                    info(res)
        elif(info):
            info("Failed. " + title_eng)
    def MangaToAnime(self):
        id = int(self.query(AniList.Query.getUser, {"search": "EnergoStalin"}).data.User.id)
        lists = self.query(AniList.Query.getList, {"id": id, "type": "MANGA"}).data.MediaListCollection.lists
        for list in lists:
            for entry in list["entries"]:
                res = self.GetMediaInfo(entry["media"]["title"]["userPreferred"])
                try:
                    self.AddToList(list["status"], res, print)
                    self.query(AniList.Query.delete, {"id": entry["id"]}, True)
                    print("Success " + list["status"] + " " + str(res))
                except Exception as ex:
                    print("Merge failed.")
                    print(ex)
                    print(entry)
                    print(res)
                

if __name__ == "__main__":
    AniList().MangaToAnime()