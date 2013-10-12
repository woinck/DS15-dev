# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'part_beginMenu.ui'
#
# Created: Wed Oct 09 23:12:11 2013
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_beginMenu(object):
    def setupUi(self, beginMenu):
        beginMenu.setObjectName(_fromUtf8("beginMenu"))
        beginMenu.resize(289, 411)
        self.frame = QtGui.QFrame(beginMenu)
        self.frame.setGeometry(QtCore.QRect(0, 0, 290, 411))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.singleGameButton = QtGui.QPushButton(self.frame)
        self.singleGameButton.setGeometry(QtCore.QRect(80, 30, 145, 50))
        self.singleGameButton.setText(_fromUtf8(""))
        self.singleGameButton.setObjectName(_fromUtf8("singleGameButton"))
        self.webGameButton = QtGui.QPushButton(self.frame)
        self.webGameButton.setGeometry(QtCore.QRect(80, 100, 145, 50))
        self.webGameButton.setText(_fromUtf8(""))
        self.webGameButton.setObjectName(_fromUtf8("webGameButton"))
        self.websiteButton = QtGui.QPushButton(self.frame)
        self.websiteButton.setGeometry(QtCore.QRect(80, 170, 145, 50))
        self.websiteButton.setText(_fromUtf8(""))
        self.websiteButton.setObjectName(_fromUtf8("websiteButton"))
        self.teamButton = QtGui.QPushButton(self.frame)
        self.teamButton.setGeometry(QtCore.QRect(80, 240, 145, 50))
        self.teamButton.setText(_fromUtf8(""))
        self.teamButton.setObjectName(_fromUtf8("teamButton"))
        self.exitGameButton = QtGui.QPushButton(self.frame)
        self.exitGameButton.setGeometry(QtCore.QRect(80, 310, 145, 50))
        self.exitGameButton.setText(_fromUtf8(""))
        self.exitGameButton.setObjectName(_fromUtf8("exitGameButton"))

        self.retranslateUi(beginMenu)
        QtCore.QMetaObject.connectSlotsByName(beginMenu)

    def retranslateUi(self, beginMenu):
        beginMenu.setWindowTitle(_translate("beginMenu", "Form", None))

