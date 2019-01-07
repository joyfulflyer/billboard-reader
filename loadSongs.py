import argparse
import songDatabase



# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

# 
# Sample Usage
# 

#  from time import sleep
#  
#  # A List of Items
#  items = list(range(0, 57))
#  l = len(items)
#  
#  # Initial call to print 0% progress
#  printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
#  for i, item in enumerate(items):
#      # Do stuff...
#      sleep(0.1)
#      # Update Progress Bar
#      printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
#  
#  # Sample Output
#  Progress: |█████████████████████████████████████████████-----| 90.0% Complete


# Grabs the data from the start year (largest) to end year (smallest) inclusive
def grabBetween(startYear, endYear):
	conn = songDatabase.connect()
	r = range(startYear, endYear-1, -1)
	numYears = len(r)
	printProgressBar(0, numYears, prefix="Progress: ", suffix=" Complete")
	for i, y in enumerate(r):
		songDatabase.scrapeDataForYear(y, conn)
		printProgressBar(i+1, numYears, prefix="Progress: ", suffix=" Complete")



# Makes sure that we always go from the biggest year to the smallest
def correctedGrabBetween(startYear, endYear):
	if startYear > endYear:
		grabBetween(startYear, endYear)
	else:
		grabBetween(endYear, startYear)



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("startDate", type=int, help="The year to start loading data from")
	parser.add_argument("endDate", type=int, help="The year to end grabbing data")
	parser.add_argument("-v", "--verbose", action="count", default=0, help="Increased output")

	args = parser.parse_args()
	grabBetween(args.startDate, args.endDate)