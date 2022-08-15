from pybooru import Danbooru
from argparse import ArgumentParser
from prototype import DownloaderBase
import re, sys, requests, os

class Downloader(DownloaderBase):
    LINK_REGEX = "http.?:\/\/danbooru\.donmai\.us\/posts\/(\d+)"

    def __init__(self, args):
        self.root = args.root
        self.booru = Danbooru("danbooru")

    def DownloadIdList(self, list):
        for id in list:
            retries = 10
            while(retries):
                try:
                    data = self.booru.post_show(id)
                    r = requests.get(data['file_url'], stream=True, timeout=10)
                    if r.status_code == 200:
                        fname = f"{data['id']}_{data['md5']}{os.path.splitext(data['file_url'])[1]}"
                        path = os.path.join(self.root, fname)
                        if(os.path.exists(path)):
                            print("Allready downloaded", path)
                            retries = 0
                            continue

                        length = int(r.headers["Content-Length"])
                        downloaded = 0
                        print("Downloading", data['file_url'], "->", path)
                        try:
                            with open(path, "wb") as f:
                                for chunk in r:
                                    f.write(chunk)
                                    downloaded += len(chunk)
                                    print('\r'+str(int(100/length*downloaded))+"%",fname, end='')
                            print("Dwonloaded", path)
                            retries = 0
                        except:
                            retries -= 1
                            os.remove(path)
                            print("Download failed.")
                    else:
                        retries -= 1
                        print("Error", r.status_code)
                except Exception as ex:
                    retries -= 1
                    print(ex)
    def DownloadLinkList(booru, root, list):
        DownloadIdList(booru, root, [lnk.split('/')[-1].split('?')[0] for lnk in list])

    def ParseText(self, text):
        return re.findall(self.LINK_REGEX, text)

    def ParseFile(self, path):
        with open(path) as f:
            return ParseText(f.read())
    @classmethod
    def AddArguments(cls, parser):
        pass
    def Download(self, data):
        self.DownloadIdList(self.ParseText(data))