
from keras.applications import VGG16
from keras.applications import imagenet_utils
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from sklearn.linear_model import SGDRegressor
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
            self.model = SGDRegressor(loss='huber',		#TODO: Change to Ridge or SVR because we'll have less than 100K samples
                                penalty='l2', 
                                alpha=0.0001, 
                                fit_intercept=False, 
                                n_iter=5, 
                                shuffle=True, 
                                verbose=1, 
                                epsilon=0.1, 
                                random_state=42, 
                                learning_rate='invscaling', 
                                eta0=0.01, 
                                power_t=0.5)
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

    def feedModel(self, featVec, score):

        # model.fit usually works with batches but we're gonna train 
        # one sample at a time. So the data needs a little reshaping...
        featVec = np.array(featVec)
        score = np.array([score])

        self.model.fit(featVec, score)
