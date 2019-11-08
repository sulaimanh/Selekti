# from PyQt4.QtGui import QSlider
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QIcon, QPixmap
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def mouseInTickZone(position_on_bar):
    """ This is a hack because its totally depended on the current size of the 
    slider bar (700) and all the numbers are magic.."""

    if (position_on_bar < 25):
        return 1
    if(position_on_bar > 75 and position_on_bar < 85):
        return 2
    if(position_on_bar > 155 and position_on_bar < 165):
        return 3
    if(position_on_bar > 225 and position_on_bar < 245):
        return 4
    if(position_on_bar > 300 and position_on_bar < 315):
        return 5
    if(position_on_bar > 375 and position_on_bar < 395):
        return 6
    if(position_on_bar > 445 and position_on_bar < 475):
        return 7
    if(position_on_bar > 530 and position_on_bar < 550):
        return 8
    if(position_on_bar > 605 and position_on_bar < 625):
        return 9
    if(position_on_bar > 670):
        return 10
    
    return -1

class Slider(QSlider):
    """ This class will prevent the unpredictable behavior of clicking on
    the slider bar instead of the notch. 
    Adapted from ingvar's solution: https://stackoverflow.com/questions/52689047/moving-qslider-to-mouse-click-position"""

    def mousePressEvent(self, e):
        
        x_bar_position = e.pos().x()
        interval_distance = 80

        interval_position = x_bar_position % interval_distance

        mouse_tick_zone = mouseInTickZone(x_bar_position)

        if e.button() != Qt.LeftButton or mouse_tick_zone < 1:
            return

        # grab the current position of the notch 
        notch_value = self.value()

        # if mouse is in tick zone and notch is on the same tick, allow the drag 
        if mouse_tick_zone == notch_value:
            return super(Slider, self).mousePressEvent(e)
        # mouse in tick zone and the notch isn't on the same tick, jump to that tick
        else: 
            e.accept()
            self.setValue(mouse_tick_zone)
