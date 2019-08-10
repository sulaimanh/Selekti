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

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PhotoSelect(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_PhotoSelect, self).__init__(parent)
    def setupUi(self, PhotoSelect):
        PhotoSelect.setObjectName(_fromUtf8("PhotoSelect"))
        PhotoSelect.resize(900, 600)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.progressBar = QtGui.QProgressBar(self.dockWidgetContents)
        self.progressBar.setGeometry(QtCore.QRect(20, 520, 801, 21))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.unimportedFiles = []
        self.importedFiles = []

        self.start_Button = QtGui.QPushButton('Start', self.dockWidgetContents)
        self.start_Button.setGeometry(QtCore.QRect(290, 480, 97, 27))
        self.start_Button.clicked.connect(self.start_Button_clicked)
        
        self.train_Button = QtGui.QPushButton('Train', self.dockWidgetContents)
        self.train_Button.setGeometry(QtCore.QRect(440, 480, 97, 27))
        self.train_Button.clicked.connect(self.train_Button_clicked)
        
        self.browse_Button = QtGui.QPushButton('Browse', self.dockWidgetContents)
        self.browse_Button.setGeometry(QtCore.QRect(50, 10, 97, 27))
        self.browse_Button.clicked.connect(self.browse_Button_clicked) 

        self.instructions_Button = QtGui.QPushButton('Instructions', self.dockWidgetContents)
        self.instructions_Button.setGeometry(QtCore.QRect(690, 10, 97, 27))
        self.instructions_Button.clicked.connect(self.instructions_Button_clicked)
        
        self.warnings_Button = QtGui.QPushButton('Warnings', self.dockWidgetContents)
        self.warnings_Button.setGeometry(QtCore.QRect(580, 10, 97, 27))
        self.warnings_Button.clicked.connect(self.warnings_Button_clicked)

        self.UserImages = QtGui.QLabel(self.dockWidgetContents)
        self.UserImages.setGeometry(QtCore.QRect(100, 60, 701, 411))
        self.UserImages.setObjectName(_fromUtf8("UserImages"))
        PhotoSelect.setWidget(self.dockWidgetContents)

        self.retranslateUi(PhotoSelect)
        QtCore.QMetaObject.connectSlotsByName(PhotoSelect)
        
    def retranslateUi(self, PhotoSelect):
        PhotoSelect.setWindowTitle(_translate("PhotoSelect", "PhotoSelect", None))
        self.UserImages.setText(_translate("PhotoSelect", "Default photos here", None))
        self.UserImages.setPixmap(QPixmap("Slekit.png").scaled(701, 411, QtCore.Qt.KeepAspectRatio))
        self.UserImages.setAlignment(QtCore.Qt.AlignCenter)

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
        self.Train = QtGui.QDockWidget()
        self.ui1 = Ui_Train(self)
        self.ui1.setupUi(self.Train)
        self.Train.show()
 
    def instructions_Button_clicked(self):
        self.instructions_msg = QMessageBox()
        self.instructions_msg.setText("How to Get Started:")
        self.instructions_msg.setInformativeText("This software is used to compare images to distinguish which are more aesthetically pleasing to the user. \n\n1. To begin, start by selecting a directory filled with images you would like to use. These will be used to train the algorithm as well as sort out good images from the bad ones.\n\n2. Select 'Train' and begin training the algorithm by choosing which photo is better out of the two given. The more feedback you give, the more the algorithm learns.\n\n3. Once you are done, return to the main screen and press 'Start'. The algorithm will begin processing each photo and put the results in a new directory.")
        self.instructions_msg.setWindowTitle("How to Get Started")
        self.instructions_msg.setStandardButtons(QMessageBox.Ok)
        retval = self.instructions_msg.exec_()
             
    def browse_Button_clicked(self, firstImage):
        # Reads in the directory
        self.dir_ = QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        self.importedFiles = []
        self.unimportedFiles = []
        isMainImageUpdated = False;
        
        if not self.dir_:
            raise Exception('Exception in browse_Button_clicked: self.dir_ was read as an empty string: {}'.format(self.dir_))
        
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for filename in os.listdir(self.dir_):
            try:
                # Attempts to open image. May need to adjust to work with more image file types.
                im = Image.open(filename)
                self.importedFiles.append(self.dir_ + '/' + filename)
                if(isMainImageUpdated == False):
                    isMainImageUpdated = True 
                    self.updateMainImage(filename)

            except IOError:
                self.unimportedFiles.append(filename)
                print('The following file is not an image type:', filename)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    def start_Button_clicked(self):
        print('Start Button Clicked')

    def updateMainImage(self, image):
        self.UserImages.setPixmap(QPixmap(image).scaled(701, 411, QtCore.Qt.KeepAspectRatio))

    def Imported_Files(self, filenames):
        filenames = self.importedFiles
        for files in filenames:
            print files
        return filenames

class Ui_Train(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_Train, self).__init__(parent)

    def setupUi(self, Train):
        Train.setObjectName(_fromUtf8("Train"))
        Train.resize(900, 600)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))

        self.instructions_Button = QtGui.QPushButton('Instructions', self.dockWidgetContents)
        self.instructions_Button.setGeometry(QtCore.QRect(775, 10, 97, 27))
        self.instructions_Button.clicked.connect(self.instructions_Button_clicked)

        self.left_Button = QtGui.QPushButton('Left is better', self.dockWidgetContents)
        self.left_Button.setGeometry(QtCore.QRect(150, 400, 110, 30))
        self.left_Button.clicked.connect(self.left_Button_clicked)

        self.right_Button = QtGui.QPushButton('Right is better', self.dockWidgetContents)
        self.right_Button.setGeometry(QtCore.QRect(600, 400, 110, 30))
        self.right_Button.clicked.connect(self.right_Button_clicked)
        
        self.finish_Button = QtGui.QPushButton('Finish', self.dockWidgetContents)
        self.finish_Button.setGeometry(QtCore.QRect(395, 450, 97, 27))
        self.finish_Button.clicked.connect(self.finish_Button_clicked)
        
        self.left_UserImages = QtGui.QLabel(self.dockWidgetContents)
        self.left_UserImages.setGeometry(QtCore.QRect(25, 40, 400, 350))
        self.left_UserImages.setObjectName(_fromUtf8("left_UserImages"))
        
        self.right_UserImages = QtGui.QLabel(self.dockWidgetContents)
        self.right_UserImages.setGeometry(QtCore.QRect(450, 40, 400, 350))
        self.right_UserImages.setObjectName(_fromUtf8("left_UserImages"))
        
        Train.setWidget(self.dockWidgetContents)

        self.retranslateUi(Train)
        QtCore.QMetaObject.connectSlotsByName(Train)

    def retranslateUi(self, Train):
        Train.setWindowTitle(_translate("Train", "Train", None))
        
        self.left_UserImages.setText(_translate("PhotoSelect", "Default photos here", None))
        self.left_UserImages.setPixmap(QPixmap("left.png").scaled(300, 300, QtCore.Qt.KeepAspectRatio))
        self.left_UserImages.setAlignment(QtCore.Qt.AlignCenter)

        self.right_UserImages.setText(_translate("PhotoSelect", "Default photos here", None))
        self.right_UserImages.setPixmap(QPixmap("right.png").scaled(300, 300, QtCore.Qt.KeepAspectRatio))
        self.right_UserImages.setAlignment(QtCore.Qt.AlignCenter)
    
    def left_Button_clicked(self):
        print('Left Button Clicked')

    def right_Button_clicked(self):
        print('Right Button Clicked')

    def finish_Button_clicked(self):
        print('Finish Button Clicked')

    def instructions_Button_clicked(self):
        self.instructions_msg = QMessageBox()
        self.instructions_msg.setText("Training the Algorithm:")
        self.instructions_msg.setInformativeText("In order to improve the quality of the filtered images, the user can train the algorithm to give more desirable results. This can be done by comparing images and seeing which is aesthetically more pleasing to the user.\n\n1. Pick left if you think the photo on the left looks better.\n\n2. Pick right if you think the photo on the right looks better.\n\n3. Press finish when you are done training.")
        self.instructions_msg.setWindowTitle("Training")
        self.instructions_msg.setStandardButtons(QMessageBox.Ok)
        retval = self.instructions_msg.exec_()

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

    PhotoSelect = QtGui.QDockWidget()
    ui = Ui_PhotoSelect()
    ui.setupUi(PhotoSelect)
    PhotoSelect.show()
    sys.exit(app.exec_())

