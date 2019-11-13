from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QIcon, QPixmap
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtCore import QEvent


class StarButton(QPushButton):
    """ A star is empty (gray) by defualt. When the mouse hovers over a star,
    the star is filled with a juicy yellow color. All the stars to the left of this
    star will also be filled."""

    def initStarList(self):
        """ each star to the left of the current star will share its state"""
        self.dependentStars = []

    def setDefaultIcon(self, icon):
        self.star_empty = icon

    def setOnHoverIcon(self, icon):
        self.star_filled = icon

    def addDependentStar(self, star):
        self.dependentStars.append(star)

    def enterEvent(self, e):

        # print("[INFO] entered")
        self.setIcon(self.star_filled)

        for star in self.dependentStars:
            star.setIcon(self.star_filled)

    def leaveEvent(self, e):

        # print("[INFO] LEFT")
        self.setIcon(self.star_empty)

        for star in self.dependentStars:
            star.setIcon(self.star_empty)
