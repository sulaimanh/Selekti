# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainApplication.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QIcon, QPixmap
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PIL import Image
from handlers.model_builder import Nima
from handlers.data_generator import TestDataGenerator
from utils.utils import calc_mean_score
<<<<<<< Updated upstream
from personalModel.personal_model import PersonalModel
=======
from utils.slider import Slider
>>>>>>> Stashed changes
import os, sys
from os import path
QtCore.QCoreApplication.addLibraryPath(path.join(path.dirname(QtCore.__file__), "plugins"))
QtGui.QImageReader.supportedImageFormats()
import random
import math
import glob
import json
import shutil

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

    unimportedFiles = []
    importedFiles = []
    selected_directory = ""
    isMainImageUpdated = False;

    def __init__(self, parent=None):
        super(Ui_Selekti, self).__init__(parent)
        self.setWindowTitle(("Selekti"))
        self.WINDOW_WIDTH = 900
        self.WINDOW_HEIGHT = 630
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        
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
        self.start_Button.clicked.connect(self.start_Button_clicked)
        
        self.train_Button = QtGui.QPushButton('Train', self)
        self.train_Button.setEnabled(False)
        self.train_Button.setGeometry(QtCore.QRect(500, 480, 97, 27))
        self.train_Button.clicked.connect(self.train_Button_clicked)            
        
        self.mainMenu = self.menuBar()

        # Actions which can be seen from the drop-down of each menu selection
        self.browseAction = QtGui.QAction("&Browse..", self)
        self.browseAction.triggered.connect(self.browse_Button_clicked)

        self.warningsAction = QtGui.QAction("&Warnings", self)
        self.warningsAction.triggered.connect(self.warnings_Button_clicked)

        self.instructionsAction = QtGui.QAction("&Instructions", self)
        self.instructionsAction.triggered.connect(self.instructions_Button_clicked)

        # Menu selections that show on the menubar on the Selekti screen
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(self.browseAction)

        self.warningsMenu = self.mainMenu.addMenu('&Warnings')
        self.warningsMenu.addAction(self.warningsAction)

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

        self.show()
        self.set_styles()
        self.first_time_use()

    def set_styles(self):
        self.mainMenu.setPalette(QPalette(Qt.white))
        self.current_directory_label.setStyleSheet("QLabel { color: white; }")
        self.sub_directories_label.setStyleSheet("QLabel { color: white; }")
        self.setStyleSheet("QMainWindow { background-color: rgb(53, 53, 53); }")      

    def first_time_use(self):
        # If the user has selected a directory before, then the text file will not be empty, and we can assume
        # the user has ran the program before. 
        if os.path.getsize("browse_cache.txt"):
            print("browse_cache.txt has a directory. Do not run first_time_use")
        else:
            print("browse_cache.txt is empty. Run first_time_use")
            self.instructions_Button_clicked()


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
        self.ui1 = Ui_Train(self)
 
    def instructions_Button_clicked(self):
        self.instructions_msg = QMessageBox()
        self.instructions_msg.setText("How to Get Started:")
        self.instructions_msg.setInformativeText("This software is used to compare images to distinguish which are more aesthetically pleasing to the user. \n\n1. To begin, start by going to the 'File' dropdown menu option on the top left and selecting 'Browse'. Choose a directory filled with images you would like to use to train the algorithm as well as sort out good images from the bad ones!\n\n2. Select 'Train' and begin training the algorithm by dragging the slider to rate the image. The more feedback you give, the more the algorithm learns.\n\n3. Once you are done, return to the main screen and press 'Start'. The algorithm will begin processing each photo and put the results in a new directory.")
        self.instructions_msg.setWindowTitle("How to Get Started")
        self.instructions_msg.setStandardButtons(QMessageBox.Ok)
        retval = self.instructions_msg.exec_()

    def browse_Button_clicked(self):

        # Reads in the directory
        if os.path.getsize("browse_cache.txt"):
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
            self.browsing_cache = open("browse_cache.txt","w")
            self.browsing_cache.writelines(self.selected_directory)
            self.browsing_cache.close() 
            
            self.train_Button.setEnabled(False)
            self.start_Button.setEnabled(False)
            self.current_directory_progressBar.setVisible(True)
            self.sub_directories_progressBar.setVisible(True)

        # clears the cache
        self.directory_contents = None
        self.importedFiles.clear()
        self.unimportedFiles.clear()

        self.directory_contents = os.listdir(self.selected_directory)
        self.isMainImageUpdated = False
        
        self.current_directory_progress = 0
        self.sub_directory_progress = 0
        self.current_directory_progressBar.setValue(self.current_directory_progress)
        self.sub_directories_progressBar.setValue(self.sub_directory_progress)
        
        self.current_directory_label.setText("Importing Files from " + self.selected_directory)
        self.current_directory_label.setVisible(True)
        self.size_of_selected_directory = len(os.listdir(self.selected_directory))
        
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        self.size_of_current_directory = 0
        self.all_files_in_directory = []
        # Go through and calculate the size of the directory for the progress bar
        for (root, directories, files) in os.walk(self.selected_directory, topdown=True):
            self.all_files_in_directory.append(files)

        self.size_of_current_directory = len(self.all_files_in_directory)
        self.num_images_uploaded = 0

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
            else:
                # If the user imported a directory before and updated the ui main image,
                # they shouldn't see the image from the last import
                self.mainImage = QPixmap("Selekti.png")
                self.main_imageLabel.setPixmap(self.mainImage)
                self.main_imageLabel.setAlignment(QtCore.Qt.AlignCenter)

            self.current_directory_label.setText("Completed Importing Files from: " + self.selected_directory)
            self.sub_directories_label.setText("Completed Importing Files from: " + root)
            self.current_directory_progressBar.setValue(math.ceil(100))
            self.sub_directories_progressBar.setValue(math.ceil(100))
        else:
            raise Exception('Exception in browse_Button_clicked: current directory progressBar value calculated incorrectly: {}'.format(math.ceil(round(self.current_directory_progress * 100, 3))))


    def start_Button_clicked(self):
        print('Start Button Clicked')
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

        # create new directory to hold top rated pics
        new_dir = os.path.sep.join([self.selected_directory, "Top_pic(k)s"])
        
        if os.path.exists(new_dir):
    	    shutil.rmtree(new_dir)

        os.mkdir(new_dir)

        # determine number of pics to copy into new dir
        # 20% for now
        num_to_pick = int(len(totalSamples) * 0.2)

        i = 0
        # since totalSamples is now sorted with the highest rated
        # pics first, the loop will only copy the first 'num_to_pick' images
        for sample in totalSamples:
            if i == num_to_pick:
                break
            shutil.copy(sample['image_path'], new_dir)
            i += 1

        print("[INFO] Done copying into new dir.")

        #TODO: Notify user of the new directory or open it for them 

    def updateMainImage(self, image):
        self.main_imageLabel.setPixmap(QPixmap(image))
        # if self.main_imageLabel.width() > self.WINDOW_WIDTH and self.main_imageLabel.height() > self.WINDOW_HEIGHT:
        #    self.resize(self.main_imageLabel.width(),self.main_imageLabel.height())

class Ui_Train(QtGui.QMainWindow):
    imgs = []
    imgs_scored = []
    imgs_unscored = []

    # initialize personal model
    modelPath = os.path.sep.join(["personalModel", "model.cpickle"])
    model = PersonalModel(modelPath)

    def getRandomImage(self, imageList):
        if not imageList:
            return None
        
        return imageList[random.randint(0,len(imageList)-1)]

    def __init__(self, parent=None):
        super(Ui_Train, self).__init__(parent)

        self.setWindowTitle(("Train"))   
        self.WINDOW_WIDTH = 900
        self.WINDOW_HEIGHT = 630
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        self.importedFiles = ImageData(self.imgs)

        # Random images will be taken from imgs_unscored
        for imgPath in self.importedFiles.images:
            self.imgs_unscored.append({'imgPath': imgPath})
        
        print("[INFO] imgs_unscored:")
        print(json.dumps(self.imgs_unscored, indent=2))

        self.mainMenu = self.menuBar()
        # Actions which can be seen from the drop-down of each menu selection
        self.instructionsAction = QtGui.QAction("&Instructions", self)
        self.instructionsAction.triggered.connect(self.instructions_Button_clicked)

        # Menu selections that show on the menubar on the Selekti screen
        self.helpMenu = self.mainMenu.addMenu('&Help')
        self.helpMenu.addAction(self.instructionsAction)
        
        self.rate_Button = QtGui.QPushButton('Rate', self)
        self.rate_Button.setGeometry(QtCore.QRect(400, 510, 100, 30))
        self.rate_Button.clicked.connect(self.rate_Button_clicked)

        self.skip_Button = QtGui.QPushButton('Skip', self)
        self.skip_Button.setGeometry(QtCore.QRect(250, 510, 100, 30))
        self.skip_Button.clicked.connect(self.skip_Button_clicked)

        self.rate_label = QtGui.QLabel(self)
        self.rate_label.setText("What do you think of this photo?")
        self.rate_label.setStyleSheet("QLabel { color: white; font: 18px; }")
        self.rate_label.setGeometry(QtCore.QRect(250, 460, 400, 30))
        self.rate_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.rate_Slider = Slider(Qt.Horizontal, self)
        self.rate_Slider.setGeometry(QtCore.QRect(100, 480, 700, 30))
        self.rate_Slider.setMinimum(1)
        self.rate_Slider.setMaximum(10)
        self.rate_Slider.setValue(0)
        self.rate_Slider.setTickPosition(QSlider.TicksBelow)
        self.rate_Slider.setTickInterval(1)
        self.rate_Slider.valueChanged[int].connect(self.on_rate_value_changed)

        self.finish_Button = QtGui.QPushButton('Finish', self)
        self.finish_Button.setGeometry(QtCore.QRect(400, 560, 100, 30))
        self.finish_Button.clicked.connect(self.finish_Button_clicked)

        self.train_imageLabel = QtGui.QLabel(self)
        self.train_imageLabel.setGeometry(QtCore.QRect(100, 60, 700, 400))
        self.train_imageLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.current_img = self.getRandomImage(self.imgs_unscored)
        if  self.current_img == None:
            print("[INFO] No images to score.")
        else:
            self.train_imageLabel.setPixmap(QPixmap(self.current_img['imgPath']))
            self.train_imageLabel.setObjectName('train_imageLabel')
            self.train_imageLabel.mousePressEvent = self.train_image_clicked
            print("[INFO] Starting image was set.")

        self.show()

    def train_image_clicked(self, event):
        self.maximized_window = QWidget()
        self.maximized_image_label = QLabel()
        self.maximized_image_label.setPixmap(QPixmap(self.current_img['imgPath']))
        self.maximized_vbox = QVBoxLayout()
        self.maximized_vbox.addWidget(self.maximized_image_label)
        self.maximized_window.setLayout(self.maximized_vbox)
        self.maximized_window.show()

    def skip_Button_clicked(self):
        self.current_img = self.getRandomImage(self.imgs_unscored)
        if  self.current_img == None:
            print("[INFO] No image to skip.")
        else:
            im = Image.open(open(self.current_img['imgPath'], 'rb'))

            self.train_imageLabel.setPixmap(QPixmap(self.current_img['imgPath']))
            self.train_imageLabel.setAlignment(QtCore.Qt.AlignCenter)

            print("[INFO] SKIP btn clicked. Next image should be visible.")

    def rate_Button_clicked(self): 

        if self.current_img == None:
            print("[INFO] No image to rate.")
            return
        # Before this btn is clicked, the user has already chosen the score on the slider
        # Therefore we can remove the current img from the unscored list
        print("[INFO] Removing {} from imgs_unscored".format(self.current_img))
        self.imgs_unscored.remove(self.current_img)

        # Add the scored image to imgs_scored
        imgScored = {'imgPath': self.current_img['imgPath'],
                     'imgScore': self.rate_Slider.value()}
        self.imgs_scored.append(imgScored)


        # Train the user's personal model by feeding it the feature vector
        # of the image the user just scored, along with the score.
        f_vec = self.model.getFeatureVector(self.current_img['imgPath'])        
        self.model.feedModel(f_vec, imgScored['imgScore'])


        print("[INFO] List of scored images:")
        print(json.dumps(self.imgs_scored, indent=2))

        # Move on to next pic
        self.current_img = self.getRandomImage(self.imgs_unscored)
        if  self.current_img == None:
            print("[INFO] No image to rate.")
            # TODO: Produce dialog informing user end of list acheived
        else:
            im = Image.open(open(self.current_img['imgPath'], 'rb'))

            self.train_imageLabel.setPixmap(QPixmap(self.current_img['imgPath']))
            self.train_imageLabel.setAlignment(QtCore.Qt.AlignCenter)

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

        self.model.saveModel()
        print("[INFO] Model finished saving")

        self.deleteLater()

    def instructions_Button_clicked(self):
        self.instructions_msg = QMessageBox()
        self.instructions_msg.setText("Training the Algorithm:")
        self.instructions_msg.setInformativeText("In order to improve the quality of the filtered images, the user can train the algorithm to give more desirable results. This can be done by dragging the slider to rate the image according to the user's preference.\n\n1. Drag the slider left or right depending on how much you like/dislike the photo.\n\n2. Press the 'Rate' button to confirm your choice. If you are unsure about a certain photo, press 'Skip' to display a new photo.\n\n3. Press finish when you are done training.")
        self.instructions_msg.setWindowTitle("Training")
        self.instructions_msg.setStandardButtons(QMessageBox.Ok)
        retval = self.instructions_msg.exec_()

# Keep track of all successfully imported images.
class ImageData:
    images = []
    def __init__(self, retrievePhotos):
        retrievePhotos = Ui_Selekti()
        self.images = retrievePhotos.importedFiles

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    ui = Ui_Selekti()

    sys.exit(app.exec_())

