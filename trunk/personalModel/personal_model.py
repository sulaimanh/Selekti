
from sklearn.linear_model import SGDRegressor
import os
import pickle

def loadModel(fileName):

    if os.path.isfile(fileName):
        model_file = open(fileName, 'rb')
        model = pickle.load(model_file)
        model_file.close()
        print("[INFO] Using existing model.")
    else:
        model = SGDRegressor(loss='huber',		#TODO: Change to Ridge or SVR because we'll have less than 100K samples
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

    return model

def saveModel(fileName, model):
    # serialize the model to disk
    print("[INFO] saving model...")
    f = open(fileName, "wb")
    f.write(pickle.dumps(model))
    f.close()
    