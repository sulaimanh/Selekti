# from PyQt4.QtGui import QSlider
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QIcon, QPixmap
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def mouseInTickZone(position_on_bar):
    """ This is a hack because its totally depended on the current size of the 
    slider bar (700) and all the numbers are magic.."""
    if (
        position_on_bar < 25 or 
        (position_on_bar > 75 and position_on_bar < 85) or 
        (position_on_bar > 155 and position_on_bar < 165) or
        (position_on_bar > 225 and position_on_bar < 245) or
        (position_on_bar > 300 and position_on_bar < 315) or
        (position_on_bar > 375 and position_on_bar < 395) or
        (position_on_bar > 445 and position_on_bar < 475) or
        (position_on_bar > 530 and position_on_bar < 550) or
        (position_on_bar > 605 and position_on_bar < 625) or 
        position_on_bar > 680
       ):
        return True
    
    return False

class Slider(QSlider):
    """ This class will prevent the unpredictable behavior of clicking on
    the slider bar instead of the notch. 
    Adapted from ingvar's solution: https://stackoverflow.com/questions/52689047/moving-qslider-to-mouse-click-position"""

    def mousePressEvent(self, e):
        
        print("[INFO] **********************************************")
        x_bar_position = e.pos().x()
        print("[INFO] distance: {}".format(x_bar_position))

        interval_distance = 80

        interval_position = x_bar_position % interval_distance
        print("[INFO] interval_position: {}".format(interval_position))

        print("[INFO] **********************************************")

       # if intervalPos is less than 15 or greater than 65, snap to 

        if e.button() == Qt.LeftButton and mouseInTickZone(x_bar_position):
            e.accept()

            value = (self.maximum() - self.minimum()) * x_bar_position / self.width() + self.minimum()
            print("[INFO] value: {}".format(value))

            value_rounded = round(value, 1)
            print("[INFO] value_rounded: {}".format(value_rounded))

            self.setValue(value_rounded)

            # if x_bar_position < 25:
            #     self.setValue(value)

        else:
            return super(Slider, self).mousePressEvent(e)


        # if e.button() == Qt.LeftButton and (interval_position == 0):
        #     e.accept()
            
        #     value = (self.maximum() - self.minimum()) * x_bar_position / self.width() + self.minimum()
        #     self.setValue(value + 1)
        # else:
        #     return super(Slider, self).mousePressEvent(e)
