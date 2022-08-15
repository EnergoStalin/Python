from pygelbooru import Gelbooru
from prototype import DownloaderBase
import re, asyncio, requests, humanize, os

class Downloader(DownloaderBase):
    LINK_REGEX = "https?:\/\/gelbooru\.com\/index\.php\?(?:.+?&|.*?&)id=(\d+)"
    def __init__(self, args):
        self.root = args.root
        self.gelbooru = Gelbooru()

    def ParseText(self, text):
        return re.findall(self.LINK_REGEX, text)

    async def download(self, ids):
        for id in ids:
            retries = 10
            while(retries):
                post = None
                try:
                    post = await self.gelbooru.get_post(id)
                except Exception as ex:
                    print("Request failed try to enable vpn.")
                    print(ex)
                    break
                try:
                    r = requests.get(str(post), stream=True, timeout=10)
                    if r.status_code == 200:
                        fname = f"{id}_{post.filename}"
                        path = os.path.join(self.root, fname)
                        if(os.path.exists(path)):
                            print("Allready downloaded", path)
                            break

                        length = int(r.headers["Content-Length"])
                        downloaded = 0
                        print("Downloading", post, "->", path, humanize.naturalsize(length))
                        try:
                            with open(path, "wb") as f:
                                for chunk in r:
                                    f.write(chunk)
                                    downloaded += len(chunk)
                                    print('\r'+str(int(100/length*downloaded))+"%", fname, end='')
                            print("Dwonloaded", path)
                            break
                        except:
                            retries -= 1
                            os.remove(path)
                            print("Download failed.")
                    else:
                        retries -= 1
                        print("Error", r.status_code)
                except Exception as ex:
                    retries -= 1
                    print("Timeout reached", ex)

    @classmethod
    def AddArguments(cls, parser):
        pass

    def Download(self, data):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.download(self.ParseText(data)))