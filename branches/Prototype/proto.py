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

from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.applications import imagenet_utils
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from imutils import paths
from image_data import ImageData
import numpy as np
import os

model = InceptionResNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# I extracted 1 of the 64 zipped AVA image files (containing 255508 images) and placed the images
# in the folder shown on line 22 which is relative to this proto.py file. ("proto.py" and the "training"
# folder are in the same directory.)
imagePaths = list(paths.list_images("training/images4AVA/images/"))

# The number of imagePaths should reflect how many images are in the folder specified above
print("Number of image paths: ", len(imagePaths))

images = []
AVA_dataset = open("AVA_dataset/AVA.txt", "r")

for imagePath in imagePaths:
    # imagePath = imagePaths[0]

    # File names are of the form 'X.jpg' where 'X' is the image ID.
    fileName = os.path.split(imagePath)[1]
    imageID = os.path.splitext(fileName)[0]

    imgData = ImageData()

    # Now that we have the image ID, we need to find out its corresponding score.
    # AVA.txt is organized by 15 columns. The second column of each line stores 
    # the image ID. Columns 3 through 12 store counts of "aesthetic ratings" (scores).
    # For example, column 3 has counts of score 1 and column 12 has counts of score 10.
    for line in AVA_dataset:
        dataFields = line.split(" ")
        ID = dataFields[1]

        if imageID == ID :
            imgData.setID(imageID)
            imgData.setAvgScore(list(map((int), dataFields[2:12])))
    
    images.append(imgData)

AVA_dataset.close()
print("Number of images matched in AVA.txt: ", len(images))

''' I commented this out for now so I could focus on matching the image ID's with their scores.

# Adrian uses a Label Encoder to specify if a feature vector represents either a food or non-food item.
# What we need to do is specify the aesthetic score a feature vector represents. 

# Keras works in batches. Why?
BATCH_SIZE = 32
for (b,i) in enumerate(range(0, len(imagePaths), BATCH_SIZE)):
    print("[INFO] processing batch {}/{}".format(b + 1,
			int(np.ceil(len(imagePaths) / float(BATCH_SIZE)))))
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

        # This doesn't work. Gotta do the math and figure out the right shape size..
        features = features.reshape((features.shape[0], 7 * 7 * 512))
'''
