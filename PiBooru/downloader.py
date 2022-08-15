#!/usr/bin/env python

import Danbooru.danbooru as danbooru
import Pixiv.pixiv as pixiv
from argparse import ArgumentParser
import glob, re, sys, subprocess
from urllib.parse import unquote

def main():
	#Loading modules
	import os, importlib
	dr = next(os.walk("."))[1]
	modules = []
	for d in dr:
		for f in next(os.walk(d))[2]:
			fn = os.path.splitext(f)[0]
			if(d.lower() == fn):
				print("Loaded", fn, "module.")
				modules.append(importlib.import_module(f"{d}.{fn}"))

	#Adding major arguments
	parser = ArgumentParser()
	parser.add_argument("-links", help="Links to works which should be downloaded.", type=str, nargs="+", default=None, required=False)
	parser.add_argument("-file", help="Text file containing links.", type=str, required=False)
	parser.add_argument("-root", help="Root folder for downloads.", type=str, required=True)

	#Adding argument required by modules for built in pixiv module its -ptoken
	for module in modules:
		module.Downloader.AddArguments(parser)

	#Try load args
	argv = sys.argv[1::]
	try:
		with open("sav.txt") as f:
			argv += f.read().split()
	except: pass

	args = parser.parse_args(argv)

	#Composing links
	links = None
	if(args.links):
		links = ",".join(args.links)
	elif(args.file):
		with open(args.file, encoding="utf-8") as f:
			links = f.read()
		
	#Download illustrations
	for module in modules:
		module.Downloader(args).Download(links)
		
	print("Finished.")

if __name__ == "__main__":
	main()
	input()