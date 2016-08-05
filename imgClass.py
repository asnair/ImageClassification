from PIL import Image
from operator import itemgetter
import imagehash
import argparse
import shelve
import glob
import os

# construct the argument parse and parse the arguments

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
    help = "path to input dataset of images")
ap.add_argument("-s", "--shelve", required = True,
    help = "output shelve database")
args = vars(ap.parse_args())

# open a temp shelve database to hold the first dictionary
db = shelve.open('storage.db', writeback = True)

# loop over the image dataset
for imagePath in glob.glob(args["dataset"] + "/*.png"):
	
	# load the image and compute the difference hash
	image = Image.open(imagePath)
	h = str(imagehash.dhash(image))
	
	# extract the filename from the path and update the database
	# using the hash as the key and the filename append to the
	# list of values
	
	filename = imagePath[imagePath.rfind("/") + 1:]
	db[h] = db.get(h, []) + [filename]
	
if (os.path.isfile(args["shelve"]) == True):
	print "\033[4m\033[91mWarning! %s already exists!\033[0m\033[93m\n Deleting..." % str(args["shelve"]) + '\033[0m'
	os.remove(args["shelve"])

# open the final shelve database to hold the second dictionary and the one results output to
db1 = shelve.open(args["shelve"], writeback = True)

# loop over the image dataset
for imagePath1 in glob.glob(args["dataset"] + "/*.png"):

        # load the image and compute the difference hash
        image = Image.open(imagePath1)
        h = str(imagehash.dhash(image))

        # extract the filename from the path and update the database
        # using the hash as the key and the filename append to the
        # list of values

        filename = imagePath1[imagePath1.rfind("/") + 1:]
        db1[h] = db1.get(h, []) + [filename]

# use img for db and matches for db1, don't confuse them
for img in db:
	for matches in db1:
		# len(db[img]) must be >2 because if matches==img then 2 files with the same dHash have already been found, 1 in db and 1 in db1. 
		if (matches == img) and ((len(db1[matches])) > 2) :
			print '\033[92m' + "Found %d matches in the second dataset" % ((len(db1[matches]))) + '\033[0m'
			
			print "Matched key with more than 1 picture mapped: \033[94m %s \033[0m" % img

			imgValue = db1[matches]
			db1[matches] = imgValue[0]

			print str(db1)

			#use this line to print a list of the keys if you just want the keys
			#print (list(db.keys()))
			

		else:
			print "NOTHING MATCHED or matched items have already been reduced to 1 mapped picture"

# close the temp database
db.close()


print '\033[92m' + "Image list: " + '\033[0m'

for match in db1:
	print '\033[93m' + str(db1[match]) + '\033[0m'

db1.close()
# remove the temp database
os.remove("storage.db")
