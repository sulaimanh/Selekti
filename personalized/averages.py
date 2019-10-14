from imutils import paths
import os

class Score:
    """ Holds the dict of image IDs and average scores."""
    def __init__(self, method):
        personalized_features = open("output/csv/" + method + "-personalized-ratings.csv", "r")
        self._scores = {}
        for row in personalized_features:
            row = row.strip().split(",")
            score = row[0]
            filename = row[1].split(os.path.sep)[-1]
            ID = filename
            self._scores[ID] = score
        

        personalized_features.close()

    def getScores(self):
        return self._scores