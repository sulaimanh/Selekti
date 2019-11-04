# import the necessary packages
from sklearn.preprocessing import LabelEncoder
from keras.applications import VGG16
from keras.applications import imagenet_utils
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
import config
from imutils import paths
from averages import Score
import numpy as np
import pickle
import random
import os

from sklearn.feature_extraction import DictVectorizer

# load the VGG16 network and initialize the label encoder
print("[INFO] loading network...")
model = VGG16(weights="imagenet", include_top=False)
le = None
# loop over the data splits
for split in (config.TRAIN, config.TEST):
	# grab all image paths in the current split
	print("[INFO] processing '{} split'...".format(split))
	p = os.path.sep.join(["output", split])
	imagePaths = list(paths.list_images(p))


	# randomly shuffle the image paths and then extract the class
	# labels from the file paths
	# random.shuffle(imagePaths)

	# This represents the scores of each image.
	s = Score(split)
	labels_and_id = s.getScores()
	labels = []
	for image in imagePaths:
		image = image.split(os.path.sep)[-1]
		labels.append(labels_and_id.get(image))

	# if the label encoder is None, create it
	if le is None:
		le = LabelEncoder()
		le.fit(labels)

	# open the output CSV file for writing
	# We are going to extract the features and write them in here
	csvPath = os.path.sep.join([config.BASE_CSV_PATH, "csv",
		"{}-extract-features.csv".format(split)])
	csv = open(csvPath, "w")

	# loop over the images in batches
	# range() accepts 3 arguments: start, stop, and step.
	# enumerate() adds a counter to an iterable and returns it in a form of enumerate object.
	for (b, i) in enumerate(range(0, len(imagePaths), config.BATCH_SIZE)):
		# extract the batch of images and labels, then initialize the
		# list of actual images that will be passed through the network
		# for feature extraction
		# np.ceil will return the ceiling of the input.
		print("[INFO] processing batch {}/{}".format(b + 1,
			int(np.ceil(len(imagePaths) / float(config.BATCH_SIZE)))))

		# This will get the paths of every image in batches. Utilizing array slicing
		batchPaths = imagePaths[i:i + config.BATCH_SIZE]
		batchLabels = le.transform(labels[i:i + config.BATCH_SIZE])
		batchImages = []
		print(batchLabels)

		# loop over the images and labels in the current batch
		for imagePath in batchPaths:
			# load the input image using the Keras helper utility
			# while ensuring the image is resized to 224x224 pixels
			image = load_img(imagePath, target_size=(224, 224))
			image = img_to_array(image)

			# preprocess the image by (1) expanding the dimensions and
			# (2) subtracting the mean RGB pixel intensity from the
			# ImageNet dataset
			# expand_dim() This will expand the shape of an array. 
			# Insert a new axis that will appear at the axis position in the expanded array shape
			# Keras works with batches of images. So, the first dimension is used for the number of 
			# 	samples (or images) you have.
			image = np.expand_dims(image, axis=0)
			# This function is meant to adequate your image to the format the model requires.
			image = imagenet_utils.preprocess_input(image)

			# add the image to the batch
			batchImages.append(image)

		# pass the images through the network and use the outputs as
		# our actual features, then reshape the features into a
		# flattened volume
		# np.vstack() function to stack so as to make a single array vertically
		batchImages = np.vstack(batchImages)
		features = model.predict(batchImages, batch_size=config.BATCH_SIZE)
		features = features.reshape((features.shape[0], 7 * 7 * 512))

		# loop over the class labels and extracted features
		# We write to our CSV file.
		for (label, vec) in zip(batchLabels, features):
			# construct a row that exists of the class label and
			# extracted features
			vec = ",".join([str(v) for v in vec])
			csv.write("{}, {}\n".format(label, vec))

	# close the CSV file
	# We will have one CSV file per data split.
	csv.close()

# serialize the label encoder to disk
f = open(config.LE_PATH, "wb")
f.write(pickle.dumps(le))
f.close()