# This file is just meant for testing the personalized model.
import config
from imutils import paths
import shutil
import os
from PIL import Image
import random
import pathlib


# I have some test images. Import images to the images folder
p = os.path.sep.join([config.ORIG_INPUT_DATASET, "all-images"])
imagePaths = list(paths.list_images(p))

ratedFolder = "output/ratedImages/"
dstTest = "output/testing/"
dstTrain = "output/training/"
dstCSV = "output/csv"

# When training a new set of images in the all-images folder,
# its necessary to discard the previous images
if os.path.exists(dstTest):
	shutil.rmtree(dstTest)
	shutil.rmtree(dstTrain)
	shutil.rmtree(dstCSV)
	shutil.rmtree(ratedFolder)

os.mkdir(dstTest)
os.mkdir(dstTrain)
os.mkdir(dstCSV)
os.mkdir(ratedFolder)


ratedImages = []
scoreList = []

for imagePath in imagePaths:
	# ran = random.randint(0,6)
	# score = feelings[ran]
	# print(score)
	print("\n----------------------------------------------------------------------------------------------")
	print("Please rate the images on this scale \n 1 - 5")
	im = Image.open(imagePath)
	im.show()
	score = int(input("{}:\t".format(imagePath)))
	if score not in (1,2,3,4,5):
		break
	im.close()
	shutil.copy(imagePath, ratedFolder)
	os.remove(imagePath)
	print("----------------------------------------------------------------------------------------------\n")
	scoreList.append(score)
	imageName = imagePath[18:]
	ratedImages.append(ratedFolder+imageName)

size = len(ratedImages)
train = int((3/4) * size)
test = size - train

# For training
training = ratedImages[:train]
trainingScore = scoreList[:train]

csvPath = os.path.sep.join([config.BASE_CSV_PATH, "csv", "training-personalized-ratings.csv"])
if os.path.exists(csvPath):
	csv = open(csvPath, "+a")
else:
	csv = open(csvPath, "w")

for (image,score) in zip(training,trainingScore):
	print(image)
	shutil.copy(image, dstTrain)
	csv.write("{},{}\n".format(score, image))
csv.close()


# For testing
testing = ratedImages[train:]
testingScore = scoreList[train:]

csvPath = os.path.sep.join([config.BASE_CSV_PATH, "csv", "testing-personalized-ratings.csv"])
if os.path.exists(csvPath):
	csv = open(csvPath, "+a")	
else:
	csv = open(csvPath, "w")
for (image,score) in zip(testing,testingScore):
	shutil.copy(image, dstTest)
	csv.write("{},{}\n".format(score, image))
csv.close()
