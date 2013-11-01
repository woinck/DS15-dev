# customed button

from PyQt4 import QtGui, QtCore

class Ui_ButtonWithDisplay(QtGui.QPushButton):
    def __init__(self, parent = None):
        QtGui.QPushButton.__init__(self, parent)

    def leaveEvent(self, event):
        self.StopDisplay.emit()
        QtGui.QPushButton.leaveEvent(self, event)
    def enterEvent(self, event):
        self.StartDisplay.emit()
        QtGui.QPushButton.enterEvent(self, event)

    StartDisplay = QtCore.pyqtSignal()
    StopDisplay = QtCore.pyqtSignal()
