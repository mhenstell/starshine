import urllib2
import urllib
import sys
import os
import hashlib
import subprocess


SDO_WEBSITE = "http://sdo.gsfc.nasa.gov/assets/img/latest"
SDO_MOVIES = ['0193.mp4', '0304.mp4', '0171.mp4', '0211.mp4', '0131.mp4', '0335.mp4', \
'0094.mp4', '1600.mp4', '1700.mp4', '4500.mp4', 'EVE_latest_rotation.mp4']

STANFORD_WEBSITE = "http://jsoc.stanford.edu/data/hmi/movies/latest"
STANFORD_MOVIES = ['M_2d.mp4', 'M_color_2d.mp4', 'Ic_flat_2d.mp4']

SAVE_FOLDER = "/home/pi/download"

def check_tmp():
	if not os.path.exists(SAVE_FOLDER):
		os.mkdir(SAVE_FOLDER)

def internet_on():
	try:
		response=urllib2.urlopen(SDO_WEBSITE, timeout=5)
		return True
	except urllib2.URLError as err: pass
	return False


def get_md5(filepath, blocksize=8192):
	file_object = open(filepath, 'rb')
	md5 = hashlib.md5()
	while True:
		data = file_object.read(blocksize)
		if not data: break

		md5.update(data)
	return md5.hexdigest()	

# def get_length(filepath):
# 	mi = MediaInfo.parse(filepath)
# 	for track in mi.tracks:
# 		if track.track_type == "Video":
# 			print "\tGot Length: %s" % track.duration
# 			return track.duration
# 	return None

def download(url):
	print "Downloading: %s" % url

	basename = os.path.basename(url)
	extension = basename.split('.')[1]

	try:
		filepath = os.path.join(SAVE_FOLDER, basename)
		urllib.urlretrieve(url, filepath)

		# length = get_length(filepath)
		# if not length:
		# 	os.remove(filepath)
		# 	return

		md5 = get_md5(filepath)
		
		newFilename = "%s.%s" % (md5, extension)
		print "\tRenaming: %s" % newFilename
		os.rename(filepath, os.path.join(SAVE_FOLDER, newFilename))
		return newFilename

	except Exception as e:
		print "Error downloading %s: %s" % (filepath, e)

if __name__ == "__main__":

	check_tmp()

	if not internet_on():
		print "Error connection to %s" % SDO_WEBSITE
		sys.exit(1)

	downloadedFiles = []

	for movie in SDO_MOVIES:
		filename = download(SDO_WEBSITE + "/mpeg/latest_1024_" + movie)
		downloadedFiles.append(filename)

	for movie in STANFORD_MOVIES:
		filename = download(STANFORD_WEBSITE + "/" + movie)
		downloadedFiles.append(filename)
	
	print "Done downloading."
