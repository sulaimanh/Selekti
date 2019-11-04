# This file is just meant for testing the personalized model.
import config
from imutils import paths
import shutil
import os
from PIL import Image
import random


# I have some test images. Import images to the images folder
p = os.path.sep.join([config.ORIG_INPUT_DATASET, "all-images"])
imagePaths = list(paths.list_images(p))

dstTest = "output/testing/"
dstTrain = "output/training/"
dstCSV = "output/csv"

# When training a new set of images in the all-images folder,
# its necessary to discard the previous images
if os.path.exists(dstTest):
	shutil.rmtree(dstTest)
	shutil.rmtree(dstTrain)
	shutil.rmtree(dstCSV)

os.mkdir(dstTest)
os.mkdir(dstTrain)
os.mkdir(dstCSV)

feelings = ["happy", "excited", "nostalgic", "disgust", "angry", "sad"]


ratedImages = []
scoreList = []
print("Please rate the images on this scale \n{}".format(feelings))
for imagePath in imagePaths:
	# ran = random.randint(0,5)
	# score = feelings[ran]
	# print(score)
	score = input("{}:\t".format(imagePath))

	scoreList.append(score)
	ratedImages.append(imagePath)

size = len(ratedImages)
train = int((3/4) * size)
test = size - train

# For training
training = ratedImages[:train]
trainingScore = scoreList[:train]

csvPath = os.path.sep.join([config.BASE_CSV_PATH, "csv", "training-personalized-ratings.csv"])
csv = open(csvPath, "w")
for (image,score) in zip(training,trainingScore):
	shutil.copy(image, dstTrain)
	csv.write("{},{}\n".format(score, image))
csv.close()


# For testing
testing = ratedImages[train:]
testingScore = scoreList[train:]

csvPath = os.path.sep.join([config.BASE_CSV_PATH, "csv", "testing-personalized-ratings.csv"])
csv = open(csvPath, "w")
for (image,score) in zip(testing,testingScore):
	shutil.copy(image, dstTest)
	csv.write("{},{}\n".format(score, image))
csv.close()
