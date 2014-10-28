from pymediainfo import MediaInfo
import os

TRANSCODE_FOLDER = "/home/pi/starshine_transcoded"
#TRANSCODE_FOLDER = "/Users/max/repos/starshine/transcoded"

#PLAYLIST_FILE = "/Users/max/repos/starshine/playlist.txt"
PLAYLIST_FILE = "/home/pi/playlist.txt"

movies = []

def getLength(filepath):
	mi = MediaInfo.parse(filepath)
	for track in mi.tracks:
		if track.track_type == "Video":
			#print "\t%s Got Length: %s" % (track.duration)
			return track.duration



def generatePlaylist(files):
	
	with open(PLAYLIST_FILE, 'w') as playlist:
		for filepath in files:
			playlist.write(filepath + "\n")


if __name__ == "__main__":
	
	for dirpath, dnames, fnames in os.walk(TRANSCODE_FOLDER):
		for fname in fnames:
			if fname.endswith(".mp4"):
				movies.append(os.path.join(dirpath, fname))

	lengths = {}

#	for movie in movies:
#		print movie
#		lengths[movie] = getLength(movie)

	generatePlaylist(movies * 1000)
