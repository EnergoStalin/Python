#!/usr/bin/env python

import os, ffmpeg, logging, argparse, sys, shutil, signal, time
from humanize import naturalsize

from translatesubs.language_manager import LanguageManager
from translatesubs.subs_manager import SubsManager
from translatesubs.constants import AVAILABLE_TRANSLATORS, TRANSLATORS_PRINT, DEFAULT_SEPS_PRINT, USE_DEFAULT_SEPS, DEFAULT_SEPS, \
    SEP_MAX_LENGTH, SUB_FORMATS
from translatesubs.translatesubs import *

SUPPORTED_FROMATS = [".ass", ".srt"]
MAX_SUBTITLE_SIZE = 2000000 # 2MB
loglevel = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

def findSubtitleStream(streams: list[dict], lang: str = "eng"):
	for stream in streams:
		if "." + stream["codec_name"] in SUPPORTED_FROMATS\
			and ((stream["tags"].get("language") == lang) or lang in stream["tags"].get("title", "").lower()):
			return stream
	return None

def translate_sub(sub: str):
	subs_manager = SubsManager(filename=sub, encoding=get_encoding("auto", sub))
	subs_manager.extract_line_styling()  
	language_manager = get_language_manager("ru", False, list(AVAILABLE_TRANSLATORS.values())[0]())

	language_manager.prep_for_trans(subs_manager.just_text())
	original, translated = translate(language_manager, DEFAULT_SEPS,
									False, False)

	if(original == translated):
		raise RuntimeError("Can't translate api returned the same subtitles.")

	subs_manager.update_subs(main_subs=translated, secondary_subs=original,
							merge=True, secondary_scale=80,
							char_limit=50)
	subs_manager.save_subs(sub)

def removeLonely(fl: list[str]) -> list[str]: #return deleted subs
	subs = []
	for f in fl:
		fn, ex = os.path.splitext(f)
		if not ex in SUPPORTED_FROMATS: continue

		fls = [fm for fm in fl if fm.startswith(fn)]
		if len(fls) == 1:
			subs.append(fls[0])
			os.remove(fls[0])
	return subs

def around(val1: int, val2: int, step: int):
	return val1 >= val2 - step or val1 <= val2 + step

def extract(fl: list[str]) -> str:
	for file in fl:
		exts = file.split(".")
		if(exts[-1] == "fail" and f".{exts[-2]}" in SUPPORTED_FROMATS and os.stat(file).st_size < MAX_SUBTITLE_SIZE):
			nfile = file.replace(".fail", "", 1)
			shutil.move(file, nfile)
			logging.info(f"Found unfinished {nfile} retrying.")
			yield nfile

	for file in filter(lambda x: x.endswith(".mkv"), fl):
		try:
			metadata = ffmpeg.probe(file)
		except Exception as e:
			logging.error(f"{file} corrupted.")
			continue

		subtitle_stream = findSubtitleStream(metadata["streams"], "eng")
		if(not subtitle_stream):
			logging.warning(f"{file} does not contain subtitles.")
			continue
		subtitle_tags = subtitle_stream["tags"]
		subtitle_fn = f'{os.path.splitext(file)[0]}.{subtitle_stream["codec_name"]}'
		subtitle_size = int(subtitle_tags.get(next(filter(lambda x: x.startswith("NUMBER_OF_BYTES"), subtitle_tags))))

		if(os.path.exists(subtitle_fn + ".fail")): subtitle_fn += ".fail"

		if(os.path.exists(subtitle_fn)):
			actual_size = os.stat(subtitle_fn).st_size
			if not around(actual_size, subtitle_size, 100000):
				logging.info(f"{subtitle_fn} {naturalsize(actual_size)} Does not match subtitle stream size {naturalsize(subtitle_size)}")
				os.remove(subtitle_fn)
			elif actual_size > MAX_SUBTITLE_SIZE or subtitle_size > MAX_SUBTITLE_SIZE:
				logging.warning(f"{subtitle_fn} {naturalsize(actual_size)} Too big.")
			else: logging.info(f"Skipping existing {subtitle_fn}")
		elif subtitle_size > MAX_SUBTITLE_SIZE:
			logging.info(f"Extracting {subtitle_fn} {naturalsize(subtitle_size)}")
			logging.warning(f"{subtitle_fn} {naturalsize(subtitle_size)} Too big.")
			ffmpeg.input(file).output(subtitle_fn + ".fail", f=subtitle_stream["codec_name"], map=f"0:{subtitle_stream['index']}").run(quiet=True)
		else:
			logging.info(f"Extracting {subtitle_fn} {naturalsize(subtitle_size)}")
			ffmpeg.input(file).output(subtitle_fn, map=f"0:{subtitle_stream['index']}").run(quiet=True)
			yield subtitle_fn

def main():
	files = next(os.walk("./"))[-1]

	lonely = removeLonely(files)
	if len(lonely): print("Removed lonely subs:")
	list(map(print, lonely))

	print("Extracting...")
	for sub in extract(files):
		if sub == None: continue
		print("Extracted", sub)

		print("Translating...")
		try:
			translate_sub(sub)
			print("Translated", sub)
		except Exception as ex:
			print("Translation failed", ex)
			shutil.move(sub, sub + ".fail")
		print("Extracting...")
		
	print("Finished.")

def exit_handle(s,f):
	exit(0)

if __name__ == "__main__":
	parser = argparse.ArgumentParser("subs")
	parser.add_argument("--log", choices=loglevel, default="WARNING", type=str)
	parser.add_argument("--logfile", default=None, type=str)
	args = parser.parse_args(sys.argv[1::])

	if(args.logfile):
		logging.basicConfig(filename=args.logfile, filemode="w", encoding="utf-8", level=getattr(logging, args.log))
	
	signal.signal(signal.SIGINT, exit_handle)

	main()
	input()
