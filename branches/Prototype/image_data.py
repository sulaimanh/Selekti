class ImageData:
    """ Each line in AVA_dataset.txt contains an image ID and 
        the number of people who voted for each score (1 to 10)"""
    
    def setID(self, ID):
        self.ID = ID

    def setAvgScore(self, scores):
        assert len(scores) == 10
        
        sum = 0
        numScorersTotal = 0
        for (i, numScorers) in enumerate(scores):
            # score is a number between 1 and 10
            score = i + 1

            sum += score * numScorers
            numScorersTotal += numScorers

        self._avgScore = sum / numScorersTotal

    def getAvgScore(self):
        return self._avgScore
