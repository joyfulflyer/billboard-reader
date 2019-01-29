import argparse
import songDatabase
import printProgressBar

# This file loads data into the database for later use


# Grabs the data from the start year (largest) to end year (smallest) inclusive
def grabBetween(startYear, endYear):
    with songDatabase.connect() as conn:
        r = range(startYear, endYear - 1, -1)
        numYears = len(r)
        assumedMax = numYears * 52 + 1
        currentYear = 0
        printProgressBar.printProgressBar(0, assumedMax,
                                          prefix="Progress: ",
                                          suffix=" Complete")

        def onYearDone():
            nonlocal currentYear
            currentYear += 1
            printProgressBar.printProgressBar(currentYear, assumedMax,
                                              prefix="Progress: ",
                                              suffix=" Complete")
        for i, y in enumerate(r):
            songDatabase.scrapeDataForYear(y, conn, onYearDone)
    print("Complete")


# Makes sure that we always go from the biggest year to the smallest
def correctedGrabBetween(startYear, endYear):
    if startYear > endYear:
        grabBetween(startYear, endYear)
    else:
        grabBetween(endYear, startYear)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("startDate", type=int,
                        help="The year to start loading data from")
    parser.add_argument("endDate", type=int,
                        help="The year to end grabbing data")
    parser.add_argument("-v", "--verbose", action="count",
                        default=0, help="Increased output")

    args = parser.parse_args()
    grabBetween(args.startDate, args.endDate)
