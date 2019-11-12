from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QIcon, QPixmap
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtCore import QEvent


class StarButton(QPushButton):
    """ """

    def setDefaultIcon(self, icon):
        self.star_empty = icon

    def setOnHoverIcon(self, icon):
        self.star_filled = icon

    def enterEvent(self, e):

        # print("[INFO] entered")
        self.setIcon(self.star_filled)

    def leaveEvent(self, e):

        # print("[INFO] LEFT")
        self.setIcon(self.star_empty)
