from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
import numpy as np
import pickle
import os

sampleSize = 32

def load_data(file):

	features_train = []
	features_test = []
	scores_train = []
	scores_test = []

	midpoint = sampleSize / 2
	i = 0 

	for row in open(file):
		# extract the class label and features from the row
		row = row.strip().split(",")
		score = row[0]
		features = np.array(row[1:], dtype="float")

		if i < midpoint:
			features_train.append(features)
			scores_train.append(score)
			# print("TRAINING SCORE: {}".format(score))
		else:
			features_test.append(features)
			scores_test.append(score)
			# print("TESTING SCORE: {}".format(score))

		i += 1

	# return a tuple of the data and scores
	return (features_train, scores_train, features_test, scores_test)

(trainX, trainY, testX, testY) = load_data("feature_vectors.csv")

# train the model
print("[INFO] training model...")
model = Ridge()
model.fit(trainX, trainY)

# evaluate the model
print("[INFO] evaluating...")
preds = model.predict(testX)

# sklearn metrics wouldn't work on lists
testY = np.array(testY, dtype=np.float64)
preds = np.array(preds, dtype=np.float64)

print("[INFO] Mean absolute error: {}".format(mean_absolute_error(testY, preds)))

# serialize the model to disk
print("[INFO] saving model...")
f = open("model.cpickle", "wb")
f.write(pickle.dumps(model))
f.close()
