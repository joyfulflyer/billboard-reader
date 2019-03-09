from flask import Flask
import billboardReader.songDatabase as db
import billboardReader.songSearch
from billboardReader.songDataSource import DataSource
import json
app = Flask(__name__)


@app.route("/partialSong/<input>")
def partialSong(input):
    data = DataSource().getSongsWithPartialName(input)
    return str(json.dumps(data))


def start():
    app.run()


# uncomment for flask
if __name__ == "__main__":
    app.run()
