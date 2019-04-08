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
from PyQt4 import QtGui
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

class Ui_PhotoSelect(object):
    def setupUi(self, PhotoSelect):
        PhotoSelect.setObjectName(_fromUtf8("PhotoSelect"))
        PhotoSelect.resize(400, 300)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.progressBar = QtGui.QProgressBar(self.dockWidgetContents)
        self.progressBar.setGeometry(QtCore.QRect(60, 240, 271, 21))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.pushButton = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton.setGeometry(QtCore.QRect(100, 200, 97, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 200, 97, 27))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 20, 97, 27))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_4.setGeometry(QtCore.QRect(290, 20, 97, 27))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.UserImages = QtGui.QLabel(self.dockWidgetContents)
        self.UserImages.setGeometry(QtCore.QRect(100, 60, 201, 91))
        self.UserImages.setObjectName(_fromUtf8("UserImages"))
        self.UserImages.setPixmap(QPixmap("python.jpg"))
        PhotoSelect.setWidget(self.dockWidgetContents)

        self.retranslateUi(PhotoSelect)
        QtCore.QMetaObject.connectSlotsByName(PhotoSelect)

    def retranslateUi(self, PhotoSelect):
        PhotoSelect.setWindowTitle(_translate("PhotoSelect", "DockWidget", None))
        self.pushButton.setText(_translate("PhotoSelect", "Start", None))
        self.pushButton_2.setText(_translate("PhotoSelect", "Train", None))
        self.pushButton_3.setText(_translate("PhotoSelect", "Browse", None))
        self.pushButton_4.setText(_translate("PhotoSelect", "Instructions", None))
        self.UserImages.setText(_translate("PhotoSelect", "Default photos here", None))
        self.UserImages.setPixmap(QPixmap("python.jpg"))

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PhotoSelect = QtGui.QDockWidget()
    ui = Ui_PhotoSelect()
    ui.setupUi(PhotoSelect)
    PhotoSelect.show()
    sys.exit(app.exec_())

