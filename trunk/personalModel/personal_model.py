
from keras.applications import VGG16
from keras.applications import imagenet_utils
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from sklearn.linear_model import LogisticRegression
import os
import pickle
import numpy as np

class PersonalModel: 
    """ Use this class to load/save/train the user's personal model. """

    def __init__(self, fileName):
        self.modelPath = fileName
        self.featureExtractor = VGG16(weights="imagenet", include_top=False)

        self.loadModel()

    def loadModel(self):

        if os.path.isfile(self.modelPath):
            model_file = open(self.modelPath, 'rb')
            self.model = pickle.load(model_file)
            model_file.close()
            print("[INFO] Using existing model.")
        else:
            self.model = LogisticRegression(solver="newton-cg", multi_class="multinomial")
            print("[INFO] Using new model.")

    def saveModel(self):
        # serialize the model to disk
        print("[INFO] saving model...")
        f = open(self.modelPath, "wb")
        f.write(pickle.dumps(self.model))
        f.close()

    def getFeatureVector(self, imgPath):

        image = load_img(imgPath, target_size=(224, 224))
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = imagenet_utils.preprocess_input(image)

        feature_vec = self.featureExtractor.predict(image)
        feature_vec = feature_vec.reshape((feature_vec.shape[0], 7 * 7 * 512))

        return feature_vec

    def trainModel(self, featVecs, scores):

        featVecs = np.array(featVecs)
        featVecs = np.squeeze(featVecs)
        scores = np.array(scores)

        self.model.fit(featVecs, scores)
