# This file is just meant for testing the personalized model.

import config
from imutils import paths
import shutil
import os
from PIL import Image

# I have some test images. Import images to the images folder
p = os.path.sep.join([config.ORIG_INPUT_DATASET, "all-images"])
imagePaths = list(paths.list_images(p))

dstTest = "output/testing/"
dstTrain = "output/training/"
dstCSV = "output/csv"
if os.path.exists(dstTest):
	print("Directory exists")
else:
	os.mkdir(dstTest)
	os.mkdir(dstTrain)
	os.mkdir(dstCSV)


ratedImages = []  
scoreList = []
print("Please rate the following images from 1 - 10\nType 0 (zero) to exit\n")

for imagePath in imagePaths:

	score = int(input("{}:\t".format(imagePath)))

	if score == 0:
		break

	scoreList.append(score)
	ratedImages.append(imagePath)



# For training
size = len(ratedImages)
train = int((3/4) * size)
test = size - train

training = ratedImages[:train]
trainingScore = scoreList[:train]

csvPath = os.path.sep.join(["output", "csv", "training-personalized_features.csv"])
csv = open(csvPath, "w")
for (image,score) in zip(training,trainingScore):
	shutil.copy(image, dstTrain)
	csv.write("{},{}\n".format(score, image))
csv.close()


# For testing
testing = ratedImages[train:]
testingScore = scoreList[train:]

csvPath = os.path.sep.join(["output", "csv", "testing-personalized_features.csv"])
csv = open(csvPath, "w")
for (image,score) in zip(testing,testingScore):
	shutil.copy(image, dstTest)
	csv.write("{},{}\n".format(score, image))
csv.close()
