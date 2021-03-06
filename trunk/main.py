# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainApplication.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from datetime import date
from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtGui import QIcon, QPixmap
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PIL import Image
from handlers.model_builder import Nima
from handlers.data_generator import TestDataGenerator
from utils.utils import calc_mean_score
from personalModel.personal_model import PersonalModel
from utils.slider import Slider
from utils.star_btn import StarButton
from utils.self_destructing_box import SelfDestructingBox
import os, sys
from os import path
from imagededup.methods import DHash
QtCore.QCoreApplication.addLibraryPath(path.join(path.dirname(QtCore.__file__), "plugins"))
QtGui.QImageReader.supportedImageFormats()
import random
import math
import glob
import json
import shutil
import pickle
import numpy as np

# try:
#     _fromUtf8 = QtCore.QString.fromUtf8
# except AttributeError:
#     def _fromUtf8(s):
#         return s

# try:
#     _encoding = QtGui.QApplication.UnicodeUTF8
#     def _translate(context, text, disambig):
#         return QtGui.QApplication.translate(context, text, disambig, _encoding)
# except AttributeError:
#     def _translate(context, text, disambig):
#         return QtGui.QApplication.translate(context, text, disambig)

class Ui_Selekti(QtGui.QMainWindow):
    temp = []
    unimportedFiles = []
    importedFiles = []
    selected_directory = ""
    isMainImageUpdated = False;
    isTrainWindowShown = True

    def __init__(self, parent=None):
        super(Ui_Selekti, self).__init__(parent)
        self.setWindowTitle(("Selekti"))
        self.setWindowIcon(QtGui.QIcon('the-icon.ico'))
        self.WINDOW_WIDTH = 900
        self.WINDOW_HEIGHT = 630
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        self.isTrainWindowShown = False

        self.current_directory_label = QtGui.QLabel(self)
        self.current_directory_label.setGeometry(QtCore.QRect(20, 510, 801, 21))
        self.current_directory_label.setVisible(False)

        self.sub_directories_label = QtGui.QLabel(self)
        self.sub_directories_label.setText("Welcome To Python GUI sub")
        self.sub_directories_label.setGeometry(QtCore.QRect(20, 560, 801, 21))
        self.sub_directories_label.setVisible(False)

        self.current_directory_progressBar = QtGui.QProgressBar(self)
        self.current_directory_progressBar.setGeometry(QtCore.QRect(20, 530, 801, 21))
        self.current_directory_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.current_directory_progressBar.setVisible(False)

        self.sub_directories_progressBar = QtGui.QProgressBar(self)
        self.sub_directories_progressBar.setGeometry(QtCore.QRect(20, 580, 801, 21))
        self.sub_directories_progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.sub_directories_progressBar.setVisible(False)

        self.start_Button = QtGui.QPushButton('Start', self)
        self.start_Button.setEnabled(False)
        self.start_Button.setGeometry(QtCore.QRect(300, 480, 97, 27))
        self.start_Button.setToolTip("Choose a directory to use this!")
        self.start_Button.clicked.connect(self.start_Button_clicked)
        
        self.train_Button = QtGui.QPushButton('Train', self)
        self.train_Button.setEnabled(False)
        self.train_Button.setGeometry(QtCore.QRect(500, 480, 97, 27))
        self.train_Button.setToolTip("Choose a directory to use this!")
        self.train_Button.clicked.connect(self.train_Button_clicked)         
           
        self.mainMenu = self.menuBar()

        # Actions which can be seen from the drop-down of each menu selection
        self.browseAction = QtGui.QAction("&Browse..", self)
        self.browseAction.triggered.connect(self.browse_Button_clicked)

        self.instructionsAction = QtGui.QAction("&Instructions", self)
        self.instructionsAction.triggered.connect(self.instructions_Button_clicked)

        # Menu selections that show on the menubar on the Selekti screen
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(self.browseAction)

        self.helpMenu = self.mainMenu.addMenu('&Help')
        self.helpMenu.addAction(self.instructionsAction)

        # Main image on the Selekti screen
        self.main_imageLabel = QtGui.QLabel(self)
        self.mainImage = QPixmap("Selekti.png")
        self.main_imageLabel.setGeometry(QtCore.QRect(100, 60, 700, 400))
        self.main_imageLabel.setPixmap(self.mainImage)
        # if self.mainImage.width() > self.WINDOW_WIDTH and self.mainImage.height() > self.WINDOW_HEIGHT:
        #     self.resize(self.mainImage.width(),self.mainImage.height())
        
        self.main_imageLabel.setAlignment(QtCore.Qt.AlignCenter)

        # print(self.isTrainWindowShown)
        self.show()
        self.set_styles()

        if self.is_first_time_use():
            print("User's first time using application")
            self.instructions_Button_clicked()
        else:
            print("User revisiting. Copy imported images from file")
            with open("imported_files_cache.txt") as f:
                self.importedFiles = f.read().splitlines()

    def set_styles(self):
        self.mainMenu.setPalette(QPalette(Qt.white))
        self.current_directory_label.setStyleSheet("QLabel { color: white; }")
        self.sub_directories_label.setStyleSheet("QLabel { color: white; }")
        self.setStyleSheet("QMainWindow { background-color: rgb(53, 53, 53); }")      

    def warnings_Button_clicked(self, qmodelindex):
        
        if not self.unimportedFiles:
            self.warning_message_msg = QMessageBox()
            self.warning_message_msg.setText("The following files were not imported:")
            self.warning_msgText = "All files were imported. No errors"
            self.warning_message_msg.setInformativeText(self.warning_msgText)
            self.warning_message_msg.setStandardButtons(QMessageBox.Ok)
            self.warning_message_msg.setWindowTitle("Warning")
            retval = self.warning_message_msg.exec_()
        else:
            self.warning_msg = QListWidget()
            self.warning_msg.addItems(self.unimportedFiles)
            self.warning_msg.setWindowTitle("Unimported Files")
            self.warning_msg.show()

    @QtCore.pyqtSlot()   
    def train_Button_clicked(self):

        print(self.importedFiles)
        self.text = ImageData(None, self.isTrainWindowShown)

        if self.text.isTrainWinShown == False:
            self.text.isTrainWinShown = True
            self.hide()
            self.ui1 = Ui_Train(self)
            self.ui1.show()
        else:
            self.show()
        
    def instructions_Button_clicked(self):
        QMessageBox.information(self,
        "How to Get Started", 
        "In the top left corner, click File then Browse. Choose a directory full of JPG images. \n\nClick Start if you want to get the top photos from your chosen directory copied into a new directory.\n\nClick Train if you want to improve the algorithm. You’ll be prompted to rate your photos from 1 to 5.",
        )

    def is_first_time_use(self):
        # Reads in the directory
        if os.path.getsize("browse_cache.txt") == 0:

            # File is empty. User has not chosen one before. 
            return True 
        else:
            # Revisit previous directory
            self.browsing_cache = open("browse_cache.txt","r+")
            self.previous_directory = self.browsing_cache.readline()  
            self.browsing_cache.close()

            return False 

    def browse_Button_clicked(self):

        # Reads in the directory
        if not self.is_first_time_use():
            # Revisit previous directory
            self.browsing_cache = open("browse_cache.txt","r+")
            self.previous_directory = self.browsing_cache.readline()
            self.selected_directory = QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', self.previous_directory, QtGui.QFileDialog.ShowDirsOnly)     
            print(self.selected_directory)       
            self.browsing_cache.close()
        else:
            # This is the user's first time choosing a directory
            self.selected_directory = QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtGui.QFileDialog.ShowDirsOnly)

        if not self.selected_directory:
            raise Exception('Exception in browse_Button_clicked: self.selected_directory was read as an empty string. This may be because you did not select a directory.')
        else:
            # Store browsing information for next session
            self.browsing_cache = open("browse_cache.txt","w")
            self.browsing_cache.writelines(self.selected_directory)
            self.browsing_cache.close() 
            
            # self.current_directory_progressBar.setVisible(True)
            self.sub_directories_progressBar.setVisible(True)

        # clears the cache
        self.directory_contents = None
        self.importedFiles.clear()
        self.unimportedFiles.clear()

        self.directory_contents = os.listdir(self.selected_directory)
        self.isMainImageUpdated = False
        
        # Initialize progress bars' status
        self.current_directory_progress = 0
        self.sub_directory_progress = 0
        self.current_directory_progressBar.setValue(self.current_directory_progress)
        self.sub_directories_progressBar.setValue(self.sub_directory_progress)
        
        # self.current_directory_label.setText("Importing Files from " + self.selected_directory)
        # self.current_directory_label.setVisible(True)
        self.size_of_selected_directory = len(os.listdir(self.selected_directory))
        

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        self.size_of_current_directory = 0
        self.all_files_in_directory = []
        # Go through and calculate the size of the entire directory for the progress bar. This has to be done to get an 
        # accurate calculation
        for (root, directories, files) in os.walk(self.selected_directory, topdown=True):
            self.all_files_in_directory.append(files)

        self.size_of_current_directory = len(self.all_files_in_directory)
        self.num_images_uploaded = 0

        # Start reading through the current directory + all of its subdirectories, reading in all the valid
        # image files and storing them in a list. Update the progress bar as it goes along.
        for (root, directories, files) in os.walk(self.selected_directory, topdown=True):
            
            # Value resets since we are searching through a new directory each time
            self.sub_directory_progress = 0
            self.size_of_sub_directory = len(os.listdir(root))
            self.sub_directories_progressBar.setValue(self.sub_directory_progress)
 
            # Go through all subdirectories and import files
            if self.size_of_sub_directory == 0:
                print('Sub-directory chosen is empty. Moving on to the next one: ' + root)
            else:
                for filename in files:
                    fullpath = os.path.sep.join([root, filename])
                    try:
                        # Attempts to open image. May need to adjust to work with more image file types.
                        im = Image.open(open(fullpath, 'rb'))
                        im.close()
                        self.importedFiles.append(fullpath)
                        self.num_images_uploaded += 1;

                        if(self.isMainImageUpdated == False):
                            self.isMainImageUpdated = True 
                            self.updateMainImage(self.importedFiles[0])
                
                    except IOError:
                        self.unimportedFiles.append(fullpath)
                        print('\nThe following file(s) is not an image type: ', files)
                    
                    # Update progress bar information and value 
                    self.sub_directory_progress += (1 / self.size_of_sub_directory)
                    self.sub_directories_progressBar.setValue(math.ceil(round(self.sub_directory_progress * 100, 3)))
                    self.sub_directories_label.setText("Importing Files from: " + root)
                    self.sub_directories_label.setVisible(True)
                    
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            self.current_directory_progress += (1 / self.size_of_current_directory)
            self.current_directory_progressBar.setValue(math.ceil(round(self.current_directory_progress * 100, 3)))
        
        if math.ceil(round(self.current_directory_progress * 100, 3)) == 100:
            if len(self.importedFiles) != 0:
                # Only enables the train and start button if there are any images imported
                self.train_Button.setEnabled(True)
                self.start_Button.setEnabled(True)
                self.train_Button.setToolTip("Rate your photos to improve the selection algortihm.")
                self.start_Button.setToolTip("Starts analyzing photos from your chosen directory.")
            else:
                # If the user imported a directory before and updated the ui main image,
                # they shouldn't see the image from the last import
                self.mainImage = QPixmap("Selekti.png")
                self.main_imageLabel.setPixmap(self.mainImage)
                self.main_imageLabel.setAlignment(QtCore.Qt.AlignCenter)


            self.imported_files_cache=open("imported_files_cache.txt",'w')
            for element in self.importedFiles:
                self.imported_files_cache.write(element)
                self.imported_files_cache.write('\n')
            self.imported_files_cache.close()

            # self.current_directory_label.setText("Completed Importing Files from: " + self.selected_directory)
            self.sub_directories_label.setText("Completed Importing Files from: " + root)
            self.current_directory_progressBar.setValue(math.ceil(100))
            self.sub_directories_progressBar.setValue(math.ceil(100))
        else:
            raise Exception('Exception in browse_Button_clicked: current directory progressBar value calculated incorrectly: {}'.format(math.ceil(round(self.current_directory_progress * 100, 3))))

    def start_Button_clicked(self):
        print('Start Button Clicked')

        SelfDestructingBox.showWithTimeout(10, "Please wait while your images are analyzed.\nAnother message will appear when the process is complete.", "In progress")

        QApplication.processEvents()

        # build model and load weights
        nima = Nima("MobileNet", weights=None)
        nima.build()
        nima.nima_model.load_weights("weights_mobilenet_aesthetic_0.07.hdf5")

        totalSamples = []
        j = 0
        
        for (root, directories, files) in os.walk(self.selected_directory, topdown=True):
            print("[INFO] ROOT: " + root)

            self.samples = []

            # Only grab the jpg images
            img_paths = glob.glob(os.path.join(root, '*.jpg'))

            for img_path in img_paths:
                print("[INFO] IMG PATH IN ROOT: " + img_path)
                totalSamples.append({'image_path': img_path})

                self.importedFiles_id = os.path.basename(img_path).split('.')[0]
                self.samples.append({'image_id': self.importedFiles_id})

            # initialize data generator
            data_generator = TestDataGenerator(self.samples, root, 64, 10, nima.preprocessing_function(), img_format='jpg')

            # TODO: Circumvent multiprocessing error on Windows
            predictions = nima.nima_model.predict_generator(data_generator, workers=1, use_multiprocessing=False, verbose=1)
            # print(predictions)

            # calc mean scores and add to samples
            for i, sample in enumerate(self.samples):
                sample['mean_score_prediction'] = calc_mean_score(predictions[i])
                totalSamples[j]['mean_score_prediction'] = calc_mean_score(predictions[i])
                j += 1

            print("[INFO] Directory specific samples:")
            print(json.dumps(self.samples, indent=2))

        # sort totalSamples by score
        print("[INFO] Sorted (descending) Total samples:")
        totalSamples.sort(key=lambda i: i['mean_score_prediction'], reverse=True)
        print(json.dumps(totalSamples, indent=2))

        modelPath = os.path.sep.join(["personalModel", "model.cpickle"])
        
        bUsePM = False
        paths_with_scores = []

        if os.path.exists(modelPath):
            print("[INFO] MODEL PATH EXISTS: {}".format(modelPath))
            bUsePM = True
            # Initialize model to use its feature extraction method
            personal_model = PersonalModel(modelPath)

            # Grab top 50% of General Model's output
            top_half = totalSamples[:len(totalSamples)//2]

            feat_vecs = []
            img_paths = []
            for datum in top_half:
                feat_vecs.append(personal_model.getFeatureVector(datum['image_path']))
                img_paths.append(datum['image_path'])


            feat_vecs_np = np.array(feat_vecs)
            feat_vecs_np = np.squeeze(feat_vecs_np)

            predictions = personal_model.model.predict(feat_vecs_np)
            print("[INFO] Number of samples for PM: {}".format(len(top_half)))
            print("[INFO] Predictions: {}".format(predictions))

            paths_with_scores = list(zip(img_paths, predictions))
            # sort (descending) by the second tuple value (the score)
            paths_with_scores.sort(key=lambda x: x[1], reverse=True)

            print("[INFO] ***paths with scores***")
            for tup in paths_with_scores:
                print("[INFO] {}, {}".format(tup[0], tup[1]))
            

        
        # Creates new directory name. Checks if previous directory exists.
        self.new_dir_title = self.create_directory_name()

        # create new directory to hold top rated pics
        self.new_dir = os.path.sep.join([self.selected_directory, self.new_dir_title])
        
        if os.path.exists(self.new_dir):
    	    shutil.rmtree(self.new_dir)

        os.mkdir(self.new_dir)

        # determine number of pics to copy into new dir
        # 20% for now
        num_to_pick = int(len(totalSamples) * 0.2)

        # so before copying pics into new dir, see if we need to use the PM
        # if so, pass 40% of PM's picks into 

        if bUsePM:
            print("[INFO] PM Used")
            for i, sample in enumerate(paths_with_scores):
                if i == num_to_pick:
                    break
                shutil.copy(sample[0], self.new_dir)
        else:
        # since totalSamples is now sorted with the highest rated
        # pics first, the loop will only copy the first 'num_to_pick' images
            print("[INFO] GENERAL used")
            for i, sample in enumerate(totalSamples):
                if i == num_to_pick:
                    break
                shutil.copy(sample['image_path'], self.new_dir)

        self.done_msg = QtGui.QMessageBox()
        self.done_msg.setWindowTitle("Processing Complete!")
        self.done_msg.setText("The best photos were copied into a new directory.\nYou can find this new directory inside of the directory you initially chose.")
        self.done_msg.setIcon(QMessageBox.Information)
        self.done_msg.exec_()

        
        print("[INFO] Done copying into new dir.")

        #TODO: Notify user of the new directory or open it for them 

    def create_directory_name(self):

        # Get today's date
        today = date.today()
        today = today.strftime("%B %d, %Y")
        # Check if directory name already exists in current directory
        i = 1
        self.new_dir_title = "Top_Picks_" + today
        while os.path.isdir(os.path.sep.join([self.selected_directory, self.new_dir_title])):
            self.new_dir_title = "Top_Picks_" + today + "(" + str(i) + ")"
            i = i+1
        
        return self.new_dir_title

    def updateMainImage(self, image):
        pixmap = QPixmap(image)
        if pixmap.width() == 0 or pixmap.width() > self.width() or pixmap.height() > self.height():
            QMessageBox.critical(self, "Uh oh!", "Could not display:\n {}".format(image))
        else:
            self.main_imageLabel.setPixmap(pixmap)
        # if self.main_imageLabel.width() > self.WINDOW_WIDTH and self.main_imageLabel.height() > self.WINDOW_HEIGHT:
        #    self.resize(self.main_imageLabel.width(),self.main_imageLabel.height())

class Ui_Train(QtGui.QMainWindow):
    imgs = []
    imgs_scored = []
    imgs_unscored = []
    isTrainWindowShown = True

    # initialize personal model
    modelPath = os.path.sep.join(["personalModel", "model.cpickle"])
    model = PersonalModel(modelPath)


    def __init__(self, parent=None):
        super(Ui_Train, self).__init__(parent)

        self.setWindowTitle(("Train"))   
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.isTrainWindowShown = True
        self.importedFiles = ImageData(self.imgs, self.isTrainWindowShown)

        # Random images will be taken from imgs_unscored
        for imgPath in self.importedFiles.images:
            self.imgs_unscored.append({'imgPath': imgPath})
        
        # print("[INFO] imgs_unscored:")
        # print(json.dumps(self.imgs_unscored, indent=2))

        self.mainMenu = self.menuBar()

        # Actions which can be seen from the drop-down of each menu selection	
        self.instructionsAction = QtGui.QAction("&Instructions", self)	
        self.instructionsAction.triggered.connect(self.instructions_Button_clicked)	

        # Menu selections that show on the menubar on the Selekti screen	
        self.helpMenu = self.mainMenu.addMenu('&Help')	
        self.helpMenu.addAction(self.instructionsAction)

        self.rate_label = QtGui.QLabel(self)
        self.rate_label.setText("What do you think of this photo?")
        self.rate_label.setStyleSheet("QLabel { color: white; font: 18px; }")
        self.rate_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        star_empty = QPixmap("star_empty.png")
        star_filled = QPixmap("star_filled.png")
        star_size = star_empty.rect().size()

        stars = []

        # Make the stars
        self.star_1 = StarButton('', self)
        self.star_2 = StarButton('', self)
        self.star_3 = StarButton('', self)
        self.star_4 = StarButton('', self)
        self.star_5 = StarButton('', self)

        stars.append(self.star_1)
        stars.append(self.star_2)
        stars.append(self.star_3)
        stars.append(self.star_4)
        stars.append(self.star_5)

        # Ideally all this stuff would go into StarButton's constructor but I couldn't find out how to override it properly
        for btn in stars:
            btn.initStarList()
            btn.setIcon(QIcon(star_empty))
            btn.setDefaultIcon(QIcon(star_empty))
            btn.setOnHoverIcon(QIcon(star_filled))
            btn.setFixedSize(star_size)
            btn.setIconSize(QSize(50,50))
            btn.setStyleSheet("QPushButton { border: none; }")
            btn.setEnabled(True)

        # Clicking a star will rate the image with the level of the star
        self.star_1.clicked.connect(lambda: self.rate_Button_clicked(1))
        self.star_2.clicked.connect(lambda: self.rate_Button_clicked(2))
        self.star_3.clicked.connect(lambda: self.rate_Button_clicked(3))
        self.star_4.clicked.connect(lambda: self.rate_Button_clicked(4))
        self.star_5.clicked.connect(lambda: self.rate_Button_clicked(5))

        # when the current star is hovered over, all the stars to its left
        # should also be highlighted 
        self.star_2.addDependentStar(self.star_1)

        self.star_3.addDependentStar(self.star_1)
        self.star_3.addDependentStar(self.star_2)

        self.star_4.addDependentStar(self.star_1)
        self.star_4.addDependentStar(self.star_2)
        self.star_4.addDependentStar(self.star_3)

        self.star_5.addDependentStar(self.star_1)
        self.star_5.addDependentStar(self.star_2)
        self.star_5.addDependentStar(self.star_3)
        self.star_5.addDependentStar(self.star_4)


        self.finish_Button = QtGui.QPushButton('Finish', self)
        self.finish_Button.clicked.connect(self.finish_Button_clicked)

        self.train_imageLabel = QtGui.QLabel(self)
        self.train_imageLabel.setAlignment(QtCore.Qt.AlignCenter)

        # need to show the win before trying to access its size below
        self.show()

        # prevent window minimization
        self.setFixedSize(self.width(), self.height())

        self.rate_label.setGeometry(QtCore.QRect((self.width()*0.40), (self.height()*0.065), 400, 30))
        self.finish_Button.setGeometry(QtCore.QRect((self.width()*0.70), (self.height()*0.95), 100, 30))

        self.star_1.setGeometry(QtCore.QRect((self.width()*0.40), (self.height()*0.88), 97, 27))
        self.star_2.setGeometry(QtCore.QRect((self.width()*0.45), (self.height()*0.88), 97, 27))
        self.star_3.setGeometry(QtCore.QRect((self.width()*0.50), (self.height()*0.88), 97, 27))
        self.star_4.setGeometry(QtCore.QRect((self.width()*0.55), (self.height()*0.88), 97, 27))
        self.star_5.setGeometry(QtCore.QRect((self.width()*0.60), (self.height()*0.88), 97, 27))


        self.current_img = self.get_next_image(self.imgs_unscored)
        if  self.current_img == None:
            print("[INFO] No images to score.")
        else:
            # click on the train image
            pixmap = QPixmap(self.current_img['imgPath'])

            # sometimes the pixmap is null
            if pixmap.width() == 0 or pixmap.width() > self.width() or pixmap.height() > self.height():
                QMessageBox.critical(self, "Uh oh!", "Could not display:\n {}\n\nYou can still rate it by clicking on a star.".format(self.current_img['imgPath']))

            else:
                print("[INFO] displaying a pixmap")
                self.train_imageLabel.setPixmap(pixmap)
                self.train_imageLabel.setGeometry(QtCore.QRect((self.width()/2) - (pixmap.width()/2), (self.height()/2) - (pixmap.height()/2), pixmap.width(), pixmap.height()))

            self.train_imageLabel.setObjectName('train_imageLabel')
            self.train_imageLabel.mousePressEvent = self.train_image_clicked
            print("[INFO] Starting image was set.")

        # Feedback consists of the user's score for an image along with that image's feature vector
        # It's stored in a dictionary where the feat vectors are the keys and the scores are the values
        self.feedback_path = "feedback.cpickle"
        if os.path.isfile(self.feedback_path):
            feedback_file = open(self.feedback_path, "rb")
            self.feedback = pickle.load(feedback_file)
            # print("[INFO] feedback on OPEN: {}".format(self.feedback))
            feedback_file.close()
        else:
            self.feedback = {}


    def get_next_image(self, imageList):
        if not imageList:

            self.all_images_rated_msg = QtGui.QMessageBox()
            self.all_images_rated_msg.setWindowIcon(QtGui.QIcon('the-icon.ico'))
            self.all_images_rated_msg.setWindowTitle("Amazing!")
            self.all_images_rated_msg.setText("You rated all the images!")
            finish_button = self.all_images_rated_msg.addButton('Finish', QtGui.QMessageBox.YesRole)

            self.all_images_rated_msg.exec_()

            if self.all_images_rated_msg.clickedButton() == finish_button:
                self.all_images_rated_msg = self.finish_Button_clicked()

            return None

        return imageList[0]

    def train_image_clicked(self, event):

        self.image_win = ImageWin(self)
        self.image_win.setImage(self.current_img['imgPath'])
        self.image_win.show()

    def rate_Button_clicked(self, starNumber): 

        if self.current_img == None:
            print("[INFO] No image to rate.")
            return
        # Before this btn is clicked, the user has already chosen the score on the slider
        # Therefore we can remove the current img from the unscored list
        print("[INFO] Removing {} from imgs_unscored".format(self.current_img))
        self.imgs_unscored.remove(self.current_img)

        # Add the scored image to imgs_scored
        imgScored = {'imgPath': self.current_img['imgPath'],
                     'imgScore': starNumber }
        self.imgs_scored.append(imgScored)


        # Compute hash for the image to prevent duplicates 
        # If the user has already rated this image, the new score overwrites the old one
        dhasher = DHash()
        difference_hash = dhasher.encode_image(image_file = self.current_img['imgPath'])

        f_vec = self.model.getFeatureVector(self.current_img['imgPath'])  

        self.feedback[difference_hash] = (starNumber, f_vec)


        # print("[INFO] List of scored images:")
        # print(json.dumps(self.imgs_scored, indent=2))

        # Move on to next pic
        self.current_img = self.get_next_image(self.imgs_unscored)
        if  self.current_img == None:
            print("[INFO] No image to rate.")
            # TODO: Produce dialog informing user end of list acheived
        else:
            pixmap = QPixmap(self.current_img['imgPath'])
            self.train_imageLabel.setPixmap(pixmap)
            self.train_imageLabel.setGeometry(QtCore.QRect((self.width()/2) - (pixmap.width()/2), (self.height()/2) - (pixmap.height()/2), pixmap.width(), pixmap.height()))

            print("[INFO] RATE btn clicked. Next image should be visible.")

    def on_rate_value_changed(self, value):
        # Change the label
        if value == 1:
            self.rate_label.setText("Worst photo I have ever seen")
        elif value == 2:
            self.rate_label.setText("This photo made me turn the computer off")
        elif value == 3:
            self.rate_label.setText("There is definitely room for improvement")
        elif value == 4:
            self.rate_label.setText("Not very good but not terrible")
        elif value == 5:
            self.rate_label.setText("Undecided. It could go either way")
        elif value == 6:
            self.rate_label.setText("Decent")
        elif value == 7:
            self.rate_label.setText("Good aesthetic qualities. Not too shabby")
        elif value == 8:
            self.rate_label.setText("Great photo. Would probably show a friend")
        elif value == 9:
            self.rate_label.setText("Absolutely stunning. Brought a tear to your eye")
        elif value == 10:
            self.rate_label.setText("The pinnacle of beauty")
        self.rate_label.setVisible(True)

    def finish_Button_clicked(self):
        print('Finish Button Clicked')

        self.text = ImageData(None, self.isTrainWindowShown)
        self.text.isTrainWinShown = True
        if self.text.isTrainWinShown == True:
            self.text.isTrainWinShown = False
            self.hide()
            self.ui2 = Ui_Selekti(self)
            self.ui2.show()
        else:
            self.show()

        featvecs = []
        scores = []

        for dhash,datum in self.feedback.items():
            scores.append(datum[0])
            featvecs.append(datum[1])
            print("[INFO] datum[1]: {}".format(datum[1]))
        
        print("[INFO] PM training commenced.")
        self.model.trainModel(featvecs, scores)

        self.model.saveModel()

        # Save the feedback dict    
        f = open(self.feedback_path, "wb")
        f.write(pickle.dumps(self.feedback))
        f.close()
        # print("[INFO] feedback on FINISH: {}".format(self.feedback))

    def instructions_Button_clicked(self):
        QMessageBox.information(self,
        "Training", 
        "To help us better understand your tastes, rate your photos on a scale of 1 to 5! \n\nClick on a star to indicate how much you like each photo. \n\nClick on an image to view its actual size.\n\nWhen you’re done (or tired of) rating, click Finish.\nIf you exit without clicking Finish, your feedback will not be saved.",
        )

class ImageWin(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(ImageWin, self).__init__(parent)

        self.setWindowTitle(("Actual Size"))


    def setImage(self, imgPath):

        print("[INFO] ImageWin's cur img path: {}".format(imgPath))

        pixmap = QPixmap(imgPath)
        width = pixmap.width()
        height = pixmap.height()

        self.setFixedSize(width, height)

        self.main_imageLabel = QtGui.QLabel(self)
        self.main_imageLabel.setGeometry(QtCore.QRect(0, 0, pixmap.width(), pixmap.height()))
        self.main_imageLabel.setPixmap(pixmap)
        self.main_imageLabel.setAlignment(Qt.AlignVCenter)



# Keep track of all successfully imported images.
class ImageData:
    images = []
    isTrainWinShown = False
    def __init__(self, retrievePhotos, retrieveIsTrainWindowShown):
        retrievePhotos = Ui_Selekti()
        retrieveIsTrainWindowShown = Ui_Selekti()
        self.images = retrievePhotos.importedFiles
        self.isTrainWinShown = retrieveIsTrainWindowShown.isTrainWindowShown


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    ui = Ui_Selekti()

    sys.exit(app.exec_())

