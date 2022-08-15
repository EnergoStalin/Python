import ffmpeg

PATH = r"./bttn1.wav"

if __name__ == "__main__":
	process = (ffmpeg.input('pipe:', format='wav') \
		.output('pipe:', format='mp3', buffer="100k") \
		.overwrite_output() \
		.run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True, quiet=True)
	)
	out, err = process.communicate(input=open(PATH, "rb").read(), timeout=15)

	open("bttn1.mp3", "wb").write(out)
	