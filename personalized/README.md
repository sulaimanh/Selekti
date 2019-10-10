How to run a testing procedure where you rate images
and see how precise the PM's predictions are:

1. Put your images in personalized/output/all-images/


2. Run rate.py. The following directories will be made:
	output/testing
	output/training
	output/csv
	
	These files will be made too:
	output/csv/training-personalized_features.csv
	output/csv/testing-personalized_features.csv
	
	Each line in the csv files will consist of an image score
	followed by the path to the image. 
	
	
	
3. Run extract_features.py. The following files will be made:
	output/training_features.csv
	output/testing_features.csv	
	
	Each line in the csv files will consist of an image score
	followed by a feature vector. 
	
	
4. Run train.py. Statistics on the PM will be shown in the console.
