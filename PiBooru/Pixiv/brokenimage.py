from PIL import Image
import os, argparse

IMG_EXT = ['.jpg','.png']

def FindBroken(path):
    _,_,fs = next(os.walk(path))
    broken = []
    for f in fs:
        if not os.path.splitext(f)[1] in IMG_EXT:
            continue
        try:
            Image.open(os.path.join(path, f)).close()
        except:
            broken.append(f)
    return broken

def ImgNamesToIDS(fnames):
    return [int(fn.split("_")[0]) for fn in fnames]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-path", type=str, required=True)
    args = parser.parse_args()
    for fn in FindBroken(args.path):
        os.remove(os.path.join(args.path,fn))
        print("Removing", fn)