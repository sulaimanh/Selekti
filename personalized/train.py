# import the necessary packages
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import config
import numpy as np
import pickle
import os

# This function is responsible for loading all data and scores given the path of a data split CSV file
# 	(the splitPath parameter)
def load_data_split(splitPath):
	# initialize the data and scores
	data = []
	scores = []

	# loop over the rows in the data split file
	# We open the data split file(splitPath)
	for row in open(splitPath):
		# extract the class label and features from the row
		row = row.strip().split(",")
		# Here we get the label, which is at the first index
		score = row[0]
		# Here, we get the rest of the features.
		features = np.array(row[1:], dtype="float")

		# update the data and label lists
		data.append(features)
		scores.append(score)

	# convert the data and scores to NumPy arrays
	# We append the feature vector and label to the data and scores list.
	data = np.array(data)
	scores = [float(s) for s in scores]

	# return a tuple of the data and scores
	return (data, scores)

# derive the paths to the training and testing CSV files
# output/training.csv
trainingPath = os.path.sep.join([config.BASE_CSV_PATH,
	"{}".format(config.TRAIN) + "_features.csv"])
# output/testing.csv
testingPath = os.path.sep.join([config.BASE_CSV_PATH,
	"{}".format(config.TEST) + "_features.csv"])

# load the data from disk
print("[INFO] loading data...")
(trainX, trainY) = load_data_split(trainingPath)
(testX, testY) = load_data_split(testingPath)

# train the model
print("[INFO] training model...")

if os.path.isfile(config.MODEL_PATH):
	model_file = open(config.MODEL_PATH, 'rb')
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

sc = StandardScaler()

trainX = sc.fit_transform(trainX)
testX = sc.transform(testX)

model.fit(trainX, trainY)

# evaluate the model
print("[INFO] evaluating...")
preds = model.predict(testX)

# Some predictions came out negative... How do we tell the model to predict within the 1 - 10 range?

# Verify the data types inside these babies
# print("[INFO] testY: {}".format(testY))
# print("[INFO] preds: {}".format(preds))

print("[INFO] Mean absolute error: {}".format(mean_squared_error(testY, preds)))
print("[INFO] Explained variance score: {}".format(explained_variance_score(testY, preds)))
# TODO: Update model based on error



# serialize the model to disk
print("[INFO] saving model...")
f = open(config.MODEL_PATH, "wb")
f.write(pickle.dumps(model))
f.close()