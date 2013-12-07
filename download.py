import urllib2
import urllib
import sys
import os
import hashlib
from pymediainfo import MediaInfo

SDO_WEBSITE = "http://sdo.gsfc.nasa.gov"

LATEST_FOLDER = "/assets/img/latest"
MPEGS = ['0193.mpg', '0304.mpg', '0171.mpg', '0211.mpg', '0131.mpg', '0335.mpg', \
'0094.mpg', '1600.mpg', '1700.mpg', '4500.mpg', 'EVE_latest_rotation.mp4']

STANFORD_WEBSITE = "http://jsoc.stanford.edu/data/hmi/movies/latest"
HMIS = ['M_2d.mpg', 'M_color_2d.mpg', 'Ic_flat_2d.mpg']

SAVE_FOLDER = "/home/max/starburn_download"

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

def get_length(filepath):
	mi = MediaInfo.parse(filepath)
	for track in mi.tracks:
		if track.track_type == "Video":
			return track.duration
	return None

def download(url):
	print "Downloading: %s" % url

	basename = os.path.basename(url)
	extension = basename.split('.')[1]

	# try:
	filepath = os.path.join(SAVE_FOLDER, basename)
	urllib.urlretrieve(url, filepath)

	length = get_length(filepath)
	if not length:
		os.remove(filepath)
		return

	md5 = get_md5(filepath)
	
	os.rename(filepath, os.path.join(SAVE_FOLDER, "%s-%s.%s" % (md5, length, extension)))

	# except Exception as e:
	# 	print "Error downloading %s: %s" % (filepath, e)

if __name__ == "__main__":

	check_tmp()

	if not internet_on():
		print "Error connection to %s" % SDO_WEBSITE
		sys.exit(1)

	for mpeg in MPEGS:
		download(SDO_WEBSITE + LATEST_FOLDER + "/mpeg/latest_1024_" + mpeg)