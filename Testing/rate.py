# This file is just meant for testing the personalized model.

import config
from imutils import paths
import shutil
import os
from PIL import Image

# I have some test images. Import images to the images folder
p = os.path.sep.join([config.ORIG_INPUT_DATASET, "all-images"])
imagePaths = list(paths.list_images(p))

csvPath = os.path.sep.join(["output","personalized_features.csv"])
csv = open(csvPath, "w")

dstTest = "output/test/"
dstTrain = "output/train/"
if os.path.exists(dstTest):
	print("Directory exists")
else:
	os.mkdir(dstTest)
	os.mkdir(dstTrain)

ratedImages = []
for imagePath in imagePaths:
	img = Image.open(imagePath)
	# If you want to show the image
	# img.show()

	score = int(input("Please rate the image from 1 - 10\nType 0 (zero) to exit\n"))

	if score == 0:
		break
		
	csv.write("{}, {}\n".format(score, imagePath))

	ratedImages.append(imagePath)

csv.close()



size = len(ratedImages)
train = int((3/4) * size)
test = size - train
counter = 1
for image in ratedImages:
	# Separating the test and training images
	if counter > train:
		shutil.copy(image, dstTest)
	else:
		shutil.copy(image, dstTrain)
	counter = counter + 1
