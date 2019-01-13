import billboard
from flask import Flask
app = Flask(__name__)

# chart = billboard.ChartData('hot-100', date='1965-03-25', fetch=True, timeout=30)


@app.route("/seeChart/<chosenDate>")
def seeChart(chosenDate):
    newChart = billboard.ChartData('hot-100', date=chosenDate,
                                   fetch=True, timeout=30)
    return str(newChart)

# uncomment for flask
# if __name__ == "__main__":
#    app.run()
