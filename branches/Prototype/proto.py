# Prototype for training/testing our interpretation of PAC-NET.
# Here is the relevant research paper:
#
# https://sigport.org/documents/pac-net-pairwise-aesthetic-comparison-network-image-aesthetic-assessment
#
# This code draws heavily from this tutorial on Transfer Learning by Adrian Rosebrock:
# https://www.pyimagesearch.com/2019/05/20/transfer-learning-with-keras-and-deep-learning/
# He repurposes a network that was trained to distinguish 1000 objects into a network whose 
# only job is to extract image features. Then he couples each feature vector with a label of either
# food or non-food. We, on the other hand, want to couple each feature vector with a score (the aesthetic
# rating in the AVA Dataset). 

from keras.applications import VGG16
from keras.applications import imagenet_utils
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from imutils import paths
from averages import Score
import numpy as np
import os

model = VGG16(weights="imagenet", include_top=False)

# I extracted 1 of the 64 zipped AVA image files (containing 255508 images) and placed the images
# in the folder shown on line 22 which is relative to this proto.py file. ("proto.py" and the "training"
# folder are in the same directory.)
imagePaths = list(paths.list_images("training/images4AVA/images/"))

# The number of imagePaths should reflect how many images are in the folder specified above
print("Number of image paths: ", len(imagePaths))

s = Score()
scores = s.getScores()

csv = open("feature_vectors.csv", "w")

# A batch is a collection of training samples that are sent into a network
# to train it. The larger the batch size, the more memory is required, thus 
# the process is slower, however the gradient is more accurate. 
sampleSize = 32
BATCH_SIZE = 32
for (b,i) in enumerate(range(0, sampleSize, BATCH_SIZE)):
    print("[INFO] processing batch {}/{}".format(b + 1,
			int(np.ceil(sampleSize / float(BATCH_SIZE)))))

    batchPaths = imagePaths[i:i + BATCH_SIZE]
    batchImages = []

    # Here is where the features are extracted per image. 
    for imagePath in batchPaths:
        # Pre-processing steps I have yet to realize the importance of.
        image = load_img(imagePath, target_size=(224,224))
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = imagenet_utils.preprocess_input(image)

        batchImages.append(image)

    batchImages = np.vstack(batchImages)
    features = model.predict(batchImages, batch_size=BATCH_SIZE)
    features = features.reshape((features.shape[0], 7 * 7 * 512))

    # loop over the scores and extracted features
    for (score, vec) in zip(scores, features):
        # construct a row that exists of the average score and extracted features
        vec = ",".join([str(v) for v in vec])
        csv.write("{},{}\n".format(score, vec))

csv.close()
