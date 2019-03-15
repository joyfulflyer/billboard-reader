import billboard
import os
import time
from . import database_connection
from . import saver

Session = database_connection.connect(os.environ['DATABASE'])


def scrape_for_year(year):
    yearString = str(year)
    firstChart = billboard.ChartData('hot-100', date=yearString + '-01-01',
                                     fetch=True)
    chart = firstChart
    while yearString in chart.date:
        print("Saving date" + chart.date)
        saver.save_chart(chart, Session)
        time.sleep(10)  # robots.txt requests 10 seconds per request
        try:
            chart = billboard.ChartData('hot-100', chart.nextDate)
        except AttributeError:
            return
