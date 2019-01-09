from flask import Flask
import songDatabase as db
import songSearch
app = Flask(__name__)

#chart = billboard.ChartData('hot-100', date='1965-03-25', fetch=True, timeout=30)

@app.route("/partialSong")
def partialSong(input):
	allSongs = db.getAllSavedSongs()
	potentials = filter(lambda s: input in s.name, allSongs)
	removeDupes = songSearch.removeDupes(potentials)
	turnInToTuples = map(removeDupes, lambda x: (x.name, x.artist))
	formatForReturn
	return str(newChart)



# uncomment for flask
#if __name__ == "__main__":
#	app.run()