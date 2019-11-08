# import the necessary packages
# We use this import in order to concatenate paths properly.
import os

# initialize the path to the *original* input directory of images
# We will change this to the directory the user chose.
ORIG_INPUT_DATASET = "output"

# initialize the base path to the *new* directory that will contain
# our images after computing the training and testing split
# This will be where our dataset is organized. (The result of executing build_dataset.py)
BASE_PATH = "dataset"

# define the names of the training, testing, and validation
# directories
TRAIN = "training"
TEST = "testing"
VAL = "validation"
LE_PATH = os.path.sep.join(["output", "le.cpickle"])

CLASSES = ["happy", "surpised", "funny", "amazed","nostalgic", "disgust", "angry", "sad", "boring"]

# set the batch size
BATCH_SIZE = 32

BASE_CSV_PATH = "output"

# set the path to the serialized model after training
MODEL_PATH = os.path.sep.join(["output", "model.cpickle"])
