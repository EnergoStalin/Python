import sys
import os
from os import path as pt
import ffmpeg, logging, shutil

FORMATS = ["ass", "srt"]

def findSubtitle(root, fm, depth = 1):
	dp = 0
	for p,_,fs in os.walk(root):
		if dp <= depth:
			for fsn in fs:
				if(any([fsn.endswith("." + format) for format in FORMATS]) and fsn.startswith(pt.splitext(fm)[0])):
					return pt.join(p, fsn)
		dp += 1
	return None
					
if(len(sys.argv) != 2):
	print("Specify folder.")
	exit(1)

logging.basicConfig(filename="bs.log", filemode="a", level=logging.INFO, format="%(asctime)s [%(levelname)s] - %(message)s")

r, _, fs = next(os.walk(sys.argv[1]))
for fn in fs:
	if(not fn.endswith(".mkv")): continue

	sub = findSubtitle(r, fn, 2)
	if(not sub): continue

	nfn = pt.join(r, "." + fn)
	fn = pt.join(r, fn)
	inss = ffmpeg.input(sub)["s"]
	inf = ffmpeg.input(fn)

	logging.info(f"Adding {sub} -> {fn}")
	print(f"Adding {sub} -> {fn}")

	output = ffmpeg.output(inf.video, inf.audio, inss, nfn, c="copy")
	try:
		ffmpeg.run(output, overwrite_output=True, quiet=True)
		shutil.move(nfn, fn)
	except ffmpeg.Error as ex:
		logging.critical("Error:\n%s\nCmd: %s", ex.stderr.decode("utf-8"), ffmpeg.compile(output, overwrite_output=True))
		print("Critical error occured see log for details.")
		exit(1)

print("Finished.")	