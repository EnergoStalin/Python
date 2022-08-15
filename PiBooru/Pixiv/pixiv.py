#!/usr/bin/env python3

import pixivpy3 as pxpy
import os, json, re
from prototype import DownloaderBase

class Downloader(DownloaderBase):
    LINK_REGEX = "http.?:\/\/www\.pixiv\.net\/en\/artworks\/\d+#?\w?"

    def __init__(self, args):
        self.api = pxpy.AppPixivAPI()
        self.api.auth(refresh_token=args.ptoken)
        self.root = args.root

    def downloadLinks(self, root, links):
        self.downloadIds(root, [link.split("/")[-1].split("#")[0] for link in links])

    def downloadEntry(self, root, id, i, urls):
        fname = f"{id}_p{i}{os.path.splitext(urls.original)[1]}"
        if os.path.exists(os.path.join(root, fname)):
            print("Allready downloaded:", fname)
            return
        print("Dwonloading:", urls.original)
        self.api.download(urls.original, path=root, fname=fname)

    def downloadIds(self, root, ids):
        for id in ids:
            print("Try download:", id)
            try:
                data = self.api.illust_detail(id).illust
                if(data.type == "ugoria"):
                    print("Ugoria currently not supported.")
                    continue
                elif(data.page_count == 1):
                    data.image_urls.original = data.meta_single_page.original_image_url
                    self.downloadEntry(root, id, 0, data.image_urls)
                    continue

                for i, img in enumerate(data.meta_pages):
                    self.downloadEntry(root, id, i, img.image_urls)
                print("Downloaded:", id)
            except Exception as ex:
                print("Failed: ", id)
                print(ex)
    def Download(self, data):
        self.downloadLinks(self.root, self.parseText(data))
    
    def download(self, args):
        if(args.links):
            self.downloadLinks(args.root, args.links)
        else:
            self.downloadIds(args.root, args.ids)

    def parseText(self, text):
        return re.findall(self.LINK_REGEX, text)
    def parseFile(self, file):
        with open(file, encoding="utf-8") as f:
            return self.parseText(f.read())
    @classmethod
    def AddArguments(cls, parser):
        parser.add_argument("-ptoken", help="Your pixiv refresh token", type=str, required=True)