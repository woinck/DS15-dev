# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'musicCheck.ui'
#
# Created: Tue Aug 20 00:47:32 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_musicCheck(object):
    def setupUi(self, musicCheck):
        musicCheck.setObjectName(_fromUtf8("musicCheck"))
        musicCheck.resize(154, 68)
        self.checkBox = QtGui.QCheckBox(musicCheck)
        self.checkBox.setGeometry(QtCore.QRect(20, 20, 101, 16))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.checkBox.setPalette(palette)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))

        self.retranslateUi(musicCheck)
        QtCore.QMetaObject.connectSlotsByName(musicCheck)

    def retranslateUi(self, musicCheck):
        musicCheck.setWindowTitle(QtGui.QApplication.translate("musicCheck", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("musicCheck", "背景音乐", None, QtGui.QApplication.UnicodeUTF8))

