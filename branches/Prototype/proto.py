# Prototype for training/testing our interpretation of PAC-NET.
# Here is the relevant research paper:
#
# https://sigport.org/documents/pac-net-pairwise-aesthetic-comparison-network-image-aesthetic-assessment

from keras.applications.inception_resnet_v2 import InceptionResNetV2

iModel = InceptionResNetV2(weights='imagenet')
