# import the necessary packages
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import accuracy_score
import config
import numpy as np
import pickle
import os

# This function is responsible for loading all data and scores given the path of a data split CSV file
# 	(the splitPath parameter)
def load_data_split(splitPath):
	# initialize the data and scores
	data = []
	labels = []

	# loop over the rows in the data split file
	# We open the data split file(splitPath)
	for row in open(splitPath):
		# extract the class label and features from the row
		row = row.strip().split(",")
		# Here we get the label, which is at the first index
		label = row[0]
		# Here, we get the rest of the features.
		features = np.array(row[1:], dtype="float")

		# update the data and label lists
		data.append(features)
		labels.append(label)

	# convert the data and scores to NumPy arrays
	# We append the feature vector and label to the data and scores list.
	data = np.array(data)
	labels = np.array(labels)
	# return a tuple of the data and scores
	return (data, labels)

# derive the paths to the training and testing CSV files
# output/training.csv
trainingPath = os.path.sep.join([config.BASE_CSV_PATH, "csv",
	"{}-extract-features.csv".format(config.TRAIN)])
# output/testing.csv
testingPath = os.path.sep.join([config.BASE_CSV_PATH, "csv",
	"{}-extract-features.csv".format(config.TEST)])

# load the data from disk
print("[INFO] loading data...")

(trainX, trainY) = load_data_split(trainingPath)
(testX, testY) = load_data_split(testingPath)

# load the label encoder from disk
le = pickle.loads(open(config.LE_PATH, "rb").read())


# train the model
print("[INFO] training model...")
model = LogisticRegression(solver="lbfgs", multi_class="auto")
model.fit(trainX, trainY)

# evaluate the model
print("[INFO] evaluating...")
preds = model.predict(testX)
print(classification_report(testY, preds, target_names=le.classes_))
print("Accuracy: {}".format(accuracy_score(testY, preds)))

# serialize the model to disk
print("[INFO] saving model...")
f = open(config.MODEL_PATH, "wb")
f.write(pickle.dumps(model))
f.close()