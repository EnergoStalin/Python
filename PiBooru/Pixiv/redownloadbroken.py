from main import *
from brokenimage import *

PATH = r"C:\Users\Alex\Pictures\Share\Hentai"
TOKEN = ""

dwl = Downloader(TOKEN)
broken = FindBroken(PATH)
ids = set(ImgNamesToIDS(broken))
for fn in broken:
    os.remove(os.path.join(PATH, fn))
dwl.downloadIds(PATH,ids)
