from imutils import paths
import os

imagePaths = list(paths.list_images("training/images4AVA/images/"))

# Careful: not every image was rated by the same number of people. 
# This could skew the model during training. Say 5 people vote on an
# image and give it a high score. Say these people have shitty taste. 
# If anyone else scored it, they'd give it a low score. But no one but 
# the people with shitty taste scored it, so the model will think its 
# a good pic. 
# TODO: Implement a system that gives more weight to photos that were
# rated by more people. 
def computeAverage(scores):
    assert len(scores) == 10
        
    sum = 0
    numScorersTotal = 0
    for (i, numScorers) in enumerate(scores):
        # score is an integer between 1 and 10
        score = i + 1

        sum += score * numScorers
        numScorersTotal += numScorers

    return sum / numScorersTotal

class Score:
    """ Holds the dict of image IDs and average scores."""
    def __init__(self):
        AVA_dataset = open("AVA_dataset/AVA.txt", "r")

        self._scores = {}
        for line in AVA_dataset:
            dataFields = line.split(" ")

            # AVA.txt is organized by 15 columns (delimited by spaces). The second column of each line
            # stores the image ID. Columns 3 through 12 store counts of "aesthetic ratings" (scores).
            # For example, column 3 has counts of score 1 and column 12 has counts of score 10.
            ID = dataFields[1]
            avg = computeAverage(list(map((int), dataFields[2:12])))

            self._scores[ID] = avg

        AVA_dataset.close()

    def getScores(self):
        return self._scores
