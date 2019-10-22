
from sklearn.linear_model import SGDRegressor
import os
import pickle

class PersonalModel: 
    """ Use this class to load/save/train the user's personal model. """

    def __init__(self, fileName):
        self.modelPath = fileName


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

