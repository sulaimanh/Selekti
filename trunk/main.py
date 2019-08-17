# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainApplication.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PIL import Image
import os, sys
import random


# try:
#     _encoding = QtGui.QApplication.UnicodeUTF8
#     def _translate(context, text, disambig):
#         return QtGui.QApplication.translate(context, text, disambig, _encoding)
# except AttributeError:
#     def _translate(context, text, disambig):
#         return QtGui.QApplication.translate(context, text, disambig)

class Ui_PhotoSelect(QtGui.QMainWindow):

    unimportedFiles = []
    importedFiles = []
    isMainImageUpdated = False;

    def __init__(self, parent=None):
        super(Ui_PhotoSelect, self).__init__(parent)
        self.setWindowTitle(("PhotoSelect"))
        self.setGeometry(200, 200, 900, 600)
        
        self.progressBar = QtGui.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(20, 520, 801, 21))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(("progressBar"))

        self.start_Button = QtGui.QPushButton('Start', self)
        self.start_Button.setEnabled(False)
        self.start_Button.setGeometry(QtCore.QRect(290, 480, 97, 27))
        self.start_Button.clicked.connect(self.start_Button_clicked)
        
        self.train_Button = QtGui.QPushButton('Train', self)
        self.train_Button.setEnabled(False)
        self.train_Button.setGeometry(QtCore.QRect(440, 480, 97, 27))
        self.train_Button.clicked.connect(self.train_Button_clicked)            
        
        self.mainMenu = self.menuBar()

        # Actions which can be seen from the drop-down of each menu selection
        self.browseAction = QtGui.QAction("&Browse..", self)
        self.browseAction.triggered.connect(self.browse_Button_clicked)

        self.warningsAction = QtGui.QAction("&Warnings", self)
        self.warningsAction.triggered.connect(self.warnings_Button_clicked)

        self.instructionsAction = QtGui.QAction("&Instructions", self)
        self.instructionsAction.triggered.connect(self.instructions_Button_clicked)

        # Menu selections that show on the menubar on the PhotoSelect screen
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(self.browseAction)

        self.warningsMenu = self.mainMenu.addMenu('&Warnings')
        self.warningsMenu.addAction(self.warningsAction)

        self.helpMenu = self.mainMenu.addMenu('&Help')
        self.helpMenu.addAction(self.instructionsAction)

        # Main image on the PhotoSelect screen
        self.UserImages = QtGui.QLabel(self)
        self.UserImages.setGeometry(QtCore.QRect(100, 60, 700, 400))
        self.UserImages.setObjectName(("UserImages"))
        self.UserImages.setPixmap(QPixmap("Slekit.png").scaled(700, 400, QtCore.Qt.KeepAspectRatio))
        self.UserImages.setAlignment(QtCore.Qt.AlignCenter)

        self.show()

    def warnings_Button_clicked(self, qmodelindex):
        self.warning_msg = QMessageBox()
        self.warning_msg.setText("The following files were not imported:")
        self.warning_msgText = ""

        for filename in self.unimportedFiles:
            self.warning_msgText += '- ' + filename + '\n'

        self.warning_msg.setInformativeText(self.warning_msgText)
        self.warning_msg.setWindowTitle("Warning")
        self.warning_msg.setStandardButtons(QMessageBox.Ok)
        retval = self.warning_msg.exec_()

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
             
    def browse_Button_clicked(self, firstImage):
        # Reads in the directory
        self.selected_directory = QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtGui.QFileDialog.ShowDirsOnly)

        
        if not self.selected_directory:
            raise Exception('Exception in browse_Button_clicked: self.selected_directory was read as an empty string: {}'.format(self.selected_directory))
        
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for filename in os.listdir(self.selected_directory):
            fullpath = self.selected_directory + '/' + filename
            
            try:
                # Attempts to open image. May need to adjust to work with more image file types.
                im = Image.open(open(fullpath, 'rb'))
                im.close()
                self.importedFiles.append(fullpath)

                if(self.isMainImageUpdated == False):
                    self.isMainImageUpdated = True 
                    self.updateMainImage(fullpath)
                    self.train_Button.setEnabled(True)
                    self.start_Button.setEnabled(True)

            except IOError:
                self.unimportedFiles.append(filename)
                print('The following file is not an image type:', filename)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    def start_Button_clicked(self):
        print('Start Button Clicked')

    def updateMainImage(self, image):
        self.UserImages.setPixmap(QPixmap(image).scaled(701, 411, QtCore.Qt.KeepAspectRatio))

class Ui_Train(QtGui.QMainWindow):
    imgs = []

    def __init__(self, parent=None):
        super(Ui_Train, self).__init__(parent)
        self.setWindowTitle(("Train"))
        self.setGeometry(200, 200, 900, 600)

        self.importedFiles = ImageData(self.imgs)

        self.mainMenu = self.menuBar()
        # Actions which can be seen from the drop-down of each menu selection
        self.instructionsAction = QtGui.QAction("&Instructions", self)
        self.instructionsAction.triggered.connect(self.instructions_Button_clicked)

        # Menu selections that show on the menubar on the PhotoSelect screen
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
        
        self.left_UserImages = QtGui.QLabel(self)
        self.left_UserImages.setGeometry(QtCore.QRect(25, 40, 400, 350))
        self.left_UserImages.setObjectName(("left_UserImages"))
        
        self.right_UserImages = QtGui.QLabel(self)
        self.right_UserImages.setGeometry(QtCore.QRect(450, 40, 400, 350))
        self.right_UserImages.setObjectName(("left_UserImages"))

        # Initially display Train screen with two random pictures.
        self.left_UserImages.setPixmap(QPixmap(self.importedFiles.images[random.randint(0,len(self.importedFiles.images)-1)]).scaled(300, 300, QtCore.Qt.KeepAspectRatio))
        self.left_UserImages.setAlignment(QtCore.Qt.AlignCenter)

        self.right_UserImages.setPixmap(QPixmap(self.importedFiles.images[random.randint(0,len(self.importedFiles.images)-1)]).scaled(300, 300, QtCore.Qt.KeepAspectRatio))
        self.right_UserImages.setAlignment(QtCore.Qt.AlignCenter)

        self.show()
    
    def left_Button_clicked(self):
        print('Left Button Clicked') 
        self.leftImage = self.importedFiles.images[random.randint(0,len(self.importedFiles.images)-1)]
        self.left_UserImages.setPixmap(QPixmap(self.leftImage).scaled(300, 300, QtCore.Qt.KeepAspectRatio))
        self.left_UserImages.setAlignment(QtCore.Qt.AlignCenter)
        print "Left Image is " + self.leftImage
        # Some images are not printing. Fix all image types


    def right_Button_clicked(self):
        print('Right Button Clicked')
        self.rightImage = self.importedFiles.images[random.randint(0,len(self.importedFiles.images)-1)]
        self.right_UserImages.setPixmap(QPixmap(self.rightImage).scaled(300, 300, QtCore.Qt.KeepAspectRatio))
        self.right_UserImages.setAlignment(QtCore.Qt.AlignCenter)
        print "Right Image is " + self.rightImage
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
        retrievePhotos = Ui_PhotoSelect()
        self.images = retrievePhotos.importedFiles

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    # Force the style to be the same on all OSs: https://stackoverflow.com/questions/48256772/dark-theme-for-in-qt-widgets
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    ui = Ui_PhotoSelect()
    sys.exit(app.exec_())

