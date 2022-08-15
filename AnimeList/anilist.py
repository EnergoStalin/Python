#!/usr/bin/env python

import time, requests
from requests_oauth2client.client_authentication import ClientSecretBasic
from requests_oauth2client.client import OAuth2Client
from requests_oauth2client.auth import OAuth2DeviceCodeAuth

from queries.load import load_queries
from utils.CleverDict import CleverDict

class AniList:
    Query = load_queries()

    graphUrl = 'https://graphql.anilist.co'
    clientSecret = ''

    def __init__(self):       
        self.session = requests.Session()

    def _batchUpdate(self, collection):
        for tg, animes in collection.items():
            if tg == 'LOVED':
                continue
            
            for anime in animes:
                self.Update(tg, None, anime, print)

    def _query(self, query, variables, reqAuth = False):
        headers = {}
        if(reqAuth): self.Auth()
            
        #Perform query
        res = self.session.post(
            AniList.graphUrl,
            json={'query': query, 'variables': variables},
            headers=headers
        )

        #Handle quota
        if(int(res.headers['X-RateLimit-Remaining']) < 2):
            time.sleep(60)
        res = res.json()

        #Handle errors
        if 'errors' in res:
            raise Exception(res['errors'])

        return CleverDict(res)

    #Get media id and handle quota per minute
    #extract quota to another method
    def GetMediaInfo(self, title_eng: str):
        res = None
        try:
            res = self._query(AniList.Query.search, {'search': title_eng})
        except Exception as ex:
            print(ex)
            return res

        for title in res.data.Page.media:  # type: ignore
            if(title['type'] == 'ANIME'):  # type: ignore
                return CleverDict(title)
        return None

    def AddToList(self, status, res, info = None):
        variables = {
            'mediaId': res['id'],
            'status': status
        }

        if status != 'CURRENT': # If not currently watching update progress if possible
            variables['progress'] = 0 if (res['episodes'] == None) else res['episodes']

        if status == 'PLANNING':
            variables['progress'] = 0

        #Add to list
        self._query(AniList.Query.add, variables, True)
            
    def Update(self, category, title_rus, title_eng, info = None):
        if(not title_eng):
            return
        res = self.GetMediaInfo(title_eng)
        if res and res.type == 'ANIME':
            try:
                self.AddToList(category, res, info)

                if info: info(f'Success {category} {res}')
            except Exception as ex:
                if info: info(f'Addition failed. {ex}\n{res}')
        elif(info):
            info(f'Failed. {title_eng}')

    def MangaToAnime(self):
        id = int(self._query(AniList.Query.getUser, {'search': 'EnergoStalin'}).data.User.id)  # type: ignore
        lists = self._query(AniList.Query.getList, {'id': id, 'type': 'MANGA'}).data.MediaListCollection.lists  # type: ignore
        for list in lists:
            for entry in list['entries']:  # type: ignore
                res = self.GetMediaInfo(entry['media']['title']['userPreferred'])  # type: ignore
                try:
                    self.AddToList(list['status'], res, print)  # type: ignore
                    self._query(AniList.Query.delete, {'id': entry['id']}, True)  # type: ignore

                    print(f'Success {list["status"]} {res}')  # type: ignore
                except Exception as ex:
                    print(f'Merge failed.', ex, entry, res, sep='\n')

    def Report(self, *args):
        self.Update(*args, print)  # type: ignore

    def Auth(self) -> 'AniList':
        client = OAuth2Client(
            token_endpoint='https://anilist.co/api/v2/oauth',
            auth=ClientSecretBasic('5718', 'lhQ3ysYE2sk9548Z9jEOR1UVJD9HayydmNo1diTr'),
            device_authorization_endpoint='https://anilist.co/api/v2/oauth/authorize'
        )
        device = client.authorize_device()
        self.session.auth = OAuth2DeviceCodeAuth(
            client,
            device.device_code,
            interval=device.interval,  # type: ignore
            expires_in=(device.expires_at - datetime.datetime.now()).seconds,  # type: ignore
        )

        return self
                    
if __name__ == '__main__':
    print(AniList().Auth().GetMediaInfo(title_eng='One punch man'))
