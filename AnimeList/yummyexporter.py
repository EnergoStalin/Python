#!/usr/bin/env python
from shikimori_api import Shikimori
from requests import HTTPError
import json, os
from time import sleep
from threading import Timer

class AnimeCollection(dict):
    def __init__(self, dc = None):
        #Defining sections
        self["CURRENT"] = []
        self["PLANNING"] = []
        self["COMPLETED"] = []
        self["LOVED"] = []
        self["DROPPED"] = []
        
        if dc:
            self.update(dc)

    def __getattr__(self, name):
        if(name in self):
            return name
        else:
            return None

    def LoadJson(self, fp: str, fmt: str = "AniList"):
        with open(fp, "r", encoding="utf-8") as f:
            if fmt == "AniList":
                self.update(json.load(f))
            else:
                for anime in json.load(f):
                    for i, v in enumerate(self):
                        if i+1 == anime["list_id"]:
                            self[v].append(anime["title"].strip())

    def SaveJson(self, fp: str):
        with open(fp, "w+", encoding="utf-8") as f:
            json.dump(self, f, indent=4, sort_keys=True, ensure_ascii=False)

    def empty(self):
        return all(not(len(v)) for v in self.values())

class ShikimoriConverter:
    #Default list name
    rusTitles = "anime-list.json"

    #Shikimori client
    shiki = Shikimori()

    def __init__(self, rus: str = "anime-list.json"):
        #Shikimori api reference
        self.api = ShikimoriConverter.shiki.get_api()
        #Anime Collections for original and translated anime titles
        self.rus = AnimeCollection()
        self.eng = AnimeCollection()

        #Collection for unrecognized titles
        self.err = AnimeCollection()

        self.rus.LoadJson(rus, "YummyAnime")

    def GetAnimeInfo(self, tp: str, anime: str):
        try: #Try get anime info from shikimori
            self.eng[tp].append(self.api.animes.GET(search=anime)[0]["name"])  # type: ignore
        except HTTPError as herr:
            sleep(30)
            self.GetAnimeInfo(anime)  # type: ignore
        except Exception as ex:
            self.err[tp].append(anime)
            return False

        return True

    def Convert(self, progress):
        for tp, animes in self.rus.items():
            for i, anime in enumerate(animes):
                if self.GetAnimeInfo(tp, anime):
                    progress(tp, anime, self.eng[tp][-1])
                else:
                    progress(tp, anime, None)

                if i % 5 == 0: #Handle quota
                    sleep(1)
        return self

    def TryLoad(self):
        [name,ext] = os.path.splitext(self.rusTitles)

        eng = f"{name}-eng{ext}"
        if os.path.exists(eng):
            self.eng.LoadJson(eng)

        err = f"{name}-err{ext}"
        if os.path.exists(err):
            self.err.LoadJson(err)

        return self

    def EngFilename(self):
        [name,ext] = os.path.splitext(self.rusTitles)
        return f"{name}-eng{ext}"
    def ErrFilename(self):
        [name,ext] = os.path.splitext(self.rusTitles)
        return f"{name}-err{ext}"

    def Save(self):
        if not self.eng.empty():
            self.eng.SaveJson(self.EngFilename())

        if not self.err.empty():
            self.err.SaveJson(self.ErrFilename())
        
        return self

if __name__ == "__main__":
    ShikimoriConverter().TryLoad().Convert(print).Save()