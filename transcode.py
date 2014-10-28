import subprocess
import os

SAVE_FOLDER = "/home/pi/download"
TRANSCODE_FOLDER = "/home/pi/transcoded"

files = os.listdir(SAVE_FOLDER)

for fname in files:

	outName = TRANSCODE_FOLDER + "/" + fname
	ffmpeg = subprocess.call(['ffmpeg', '-i', SAVE_FOLDER + "/" + fname, '-vf', "crop=1024:720,scale=320:240", '-y', outName])

