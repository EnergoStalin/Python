#!/usr/bin/env python
import os, shutil


class Cleaner:
    def __init__(self,path = ""):
        self.path = path or os.path.join(os.environ["LOCALAPPDATA"], "osu!", "Songs")

    def DeletePath(self, path, callback = None):
        sz = os.stat(path).st_size
        if(callback):
            callback(path,sz)
        if(not os.path.isfile(path)):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return sz
    def clean(self, callback = None):
        size = 0
        for dr in os.listdir(self.path):
            pt = os.path.join(self.path,dr)
            if(os.path.isdir(pt)):
                for [dp,dn,fn] in os.walk(pt):
                    for f in [i for i in fn if os.path.splitext(i)[1] in [".mp4"]]:
                        size += self.DeletePath(os.path.join(dp, f), callback)
                    for d in dn:
                        size += self.DeletePath(os.path.join(dp, d), callback)
            else:
                if(os.path.splitext(pt)[1] in [".tmp"]):
                    size += self.DeletePath(pt, callback)
                        
        return size

if __name__ == "__main__":
    import utils
    def cl(pt,sz):
        print("Removing", pt, utils.sizeof_fmt(sz))
    print("Cleaned", utils.sizeof_fmt(Cleaner().clean(cl)))
    input()