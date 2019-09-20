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
import os, sys
from os import path
QtCore.QCoreApplication.addLibraryPath(path.join(path.dirname(QtCore.__file__), "plugins"))
QtGui.QImageReader.supportedImageFormats()
import random
import math


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
        self.setGeometry(200, 200, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        
        self.current_directory_label = QtGui.QLabel(self)
        self.current_directory_label.setGeometry(QtCore.QRect(20, 510, 801, 21))
        self.current_directory_label.setVisible(False)

        self.sub_directories_label = QtGui.QLabel(self)
        self.sub_directories_label.setText("Welcome To Python GUI sub")
        self.sub_directories_label.setGeometry(QtCore.QRect(20, 560, 801, 21))
        self.sub_directories_label.setVisible(False)

        self.current_directory_progressBar = QtGui.QProgressBar(self)
        self.current_directory_progressBar.setGeometry(QtCore.QRect(20, 530, 801, 21))
        self.current_directory_progressBar.setVisible(False)

        self.sub_directories_progressBar = QtGui.QProgressBar(self)
        self.sub_directories_progressBar.setGeometry(QtCore.QRect(20, 580, 801, 21))
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
        self.main_imageLabel.setObjectName(("main_imageLabel"))
        self.main_imageLabel.setPixmap(self.mainImage)
        # if self.mainImage.width() > self.WINDOW_WIDTH and self.mainImage.height() > self.WINDOW_HEIGHT:
        #     self.resize(self.mainImage.width(),self.mainImage.height())
        
        self.main_imageLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.show()

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
        self.instructions_msg.setInformativeText("This software is used to compare images to distinguish which are more aesthetically pleasing to the user. \n\n1. To begin, start by selecting a directory filled with images you would like to use. These will be used to train the algorithm as well as sort out good images from the bad ones.\n\n2. Select 'Train' and begin training the algorithm by choosing which photo is better out of the two given. The more feedback you give, the more the algorithm learns.\n\n3. Once you are done, return to the main screen and press 'Start'. The algorithm will begin processing each photo and put the results in a new directory.")
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
                    fullpath = root + '/' + filename
                    try:
                        # Attempts to open image. May need to adjust to work with more image file types.
                        im = Image.open(open(fullpath, 'rb'))
                        im.close()
                        self.importedFiles.append(fullpath)
                        self.num_images_uploaded += 1;

                        if(self.isMainImageUpdated == False):
                            print(self.isMainImageUpdated)
                            self.isMainImageUpdated = True 
                            self.updateMainImage(self.importedFiles[0])
                
                    except IOError:
                        self.unimportedFiles.append(fullpath)
                        # print('The following file is not an image type:', files)

                    self.sub_directory_progress += (1 / self.size_of_sub_directory)
                    self.sub_directories_progressBar.setValue(math.ceil(round(self.sub_directory_progress * 100, 3)))
                    self.sub_directories_label.setText("Importing Files from: " + root)
                    self.sub_directories_label.setVisible(True)
                    
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            self.current_directory_progress += (1 / self.size_of_current_directory)
            self.current_directory_progressBar.setValue(math.ceil(round(self.current_directory_progress * 100, 3)))
        
        if math.ceil(round(self.current_directory_progress * 100, 3)) == 100:
            self.train_Button.setEnabled(True)
            self.start_Button.setEnabled(True)
            self.current_directory_label.setText("Completed Importing Files from: " + self.selected_directory)
            self.sub_directories_label.setText("Completed Importing Files from: " + root)
            self.current_directory_progressBar.setValue(math.ceil(100))
            self.sub_directories_progressBar.setValue(math.ceil(100))
        else:
            raise Exception('Exception in browse_Button_clicked: current directory progressBar value calculated incorrectly: {}'.format(math.ceil(round(self.current_directory_progress * 100, 3))))


    def start_Button_clicked(self):
        print('Start Button Clicked')

    def updateMainImage(self, image):
        self.main_imageLabel.setPixmap(QPixmap(image))
        # if self.main_imageLabel.width() > self.WINDOW_WIDTH and self.main_imageLabel.height() > self.WINDOW_HEIGHT:
        #    self.resize(self.main_imageLabel.width(),self.main_imageLabel.height())

class Ui_Train(QtGui.QMainWindow):
    imgs = []

    def __init__(self, parent=None):
        super(Ui_Train, self).__init__(parent)
        self.setWindowTitle(("Train"))
        self.setGeometry(200, 200, 900, 600)
        self.WINDOW_WIDTH = 900
        self.WINDOW_HEIGHT = 600

        self.importedFiles = ImageData(self.imgs)

        self.mainMenu = self.menuBar()
        # Actions which can be seen from the drop-down of each menu selection
        self.instructionsAction = QtGui.QAction("&Instructions", self)
        self.instructionsAction.triggered.connect(self.instructions_Button_clicked)

        # Menu selections that show on the menubar on the Selekti screen
        self.helpMenu = self.mainMenu.addMenu('&Help')
        self.helpMenu.addAction(self.instructionsAction)

        self.left_Button = QtGui.QPushButton('Left is better', self)
        self.left_Button.setGeometry(QtCore.QRect(150, 400, 110, 30))
        self.left_Button.clicked.connect(self.left_Button_clicked)

        self.right_Button = QtGui.QPushButton('Right is better', self)
        self.right_Button.setGeometry(QtCore.QRect(600, 400, 110, 30))
        self.right_Button.clicked.connect(self.right_Button_clicked)
        
        self.finish_Button = QtGui.QPushButton('Finish', self)
        self.finish_Button.setGeometry(QtCore.QRect(395, 450, 97, 27))
        self.finish_Button.clicked.connect(self.close)
        
        self.left_imageLabel = QtGui.QLabel(self)
        self.leftImage = QPixmap(self.importedFiles.images[random.randint(0,len(self.importedFiles.images)-1)]).scaled(300, 300, QtCore.Qt.KeepAspectRatio)
        self.left_imageLabel.setGeometry(QtCore.QRect(25, 40, 400, 350))
        self.left_imageLabel.setObjectName(("left_imageLabel"))
        
        self.right_imageLabel = QtGui.QLabel(self)
        self.rightImage = QPixmap(self.importedFiles.images[random.randint(0,len(self.importedFiles.images)-1)]).scaled(300, 300, QtCore.Qt.KeepAspectRatio)
        self.right_imageLabel.setGeometry(QtCore.QRect(450, 40, 400, 350))
        self.right_imageLabel.setObjectName(("left_imageLabel"))

        # Initially display Train screen with two random pictures.
        self.left_imageLabel.setPixmap(self.leftImage)
        self.left_imageLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.right_imageLabel.setPixmap(self.rightImage)
        self.right_imageLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.show()
    
    def left_Button_clicked(self):
        print('Left Button Clicked') 
        self.updated_leftImage = self.importedFiles.images[random.randint(0,len(self.importedFiles.images)-1)]
        self.leftImage = QPixmap(self.updated_leftImage)
        im = Image.open(open(self.updated_leftImage, 'rb'))
        im.show()
        if self.leftImage.width() > self.WINDOW_WIDTH and self.leftImage.height() > self.WINDOW_HEIGHT:
            
            # If a file is too big to be seen, allow the user to open the image in a new screen. If they don't want to,
            # the image will be scaled anyway. However, some resolution will be lost.
            # im.show()
            self.leftImage = QPixmap(self.updated_leftImage).scaled(300, 300, QtCore.Qt.KeepAspectRatio)

        self.left_imageLabel.setPixmap(QPixmap(self.leftImage))
        self.left_imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        # print "Left Image is " + self.updated_leftImage
        # Some images are not printing. This is probably a PyQt error since they can be im.show() correctly.
        # Fix all image types
        # https://stackoverflow.com/questions/10477075/pyqt4-jpeg-jpg-unsupported-image-format


    def right_Button_clicked(self):
        print('Right Button Clicked')
        self.rightImage = QPixmap(self.importedFiles.images[random.randint(0,len(self.importedFiles.images)-1)]).scaled(300, 300, QtCore.Qt.KeepAspectRatio)
        self.right_imageLabel.setPixmap(QPixmap(self.rightImage))

        if self.rightImage.width() > self.WINDOW_WIDTH and self.rightImage.height() > self.WINDOW_HEIGHT:
           self.resize(self.rightImage.width(),self.rightImage.height())

        self.right_imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        # print "Right Image is " + self.rightImage
        # Some images are not printing. Fix all image types

    def finish_Button_clicked(self):
        print('Finish Button Clicked')
        self.close

    def instructions_Button_clicked(self):
        self.instructions_msg = QMessageBox()
        self.instructions_msg.setText("Training the Algorithm:")
        self.instructions_msg.setInformativeText("In order to improve the quality of the filtered images, the user can train the algorithm to give more desirable results. This can be done by comparing images and seeing which is aesthetically more pleasing to the user.\n\n1. Pick left if you think the photo on the left looks better.\n\n2. Pick right if you think the photo on the right looks better.\n\n3. Press finish when you are done training.")
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
    # Force the style to be the same on all OSs: https://stackoverflow.com/questions/48256772/dark-theme-for-in-qt-widgets
    # app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    # palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    ui = Ui_Selekti()
    sys.exit(app.exec_())

