# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'part_aivsai.ui'
#
# Created: Wed Oct 09 18:29:34 2013
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

class Ui_AIvsAI(object):
    def setupUi(self, AIvsAI):
        AIvsAI.setObjectName(_fromUtf8("AIvsAI"))
        AIvsAI.resize(1024, 768)
        self.frame = QtGui.QFrame(AIvsAI)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1031, 771))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.AiButton1 = QtGui.QPushButton(self.frame)
        self.AiButton1.setGeometry(QtCore.QRect(40, 330, 40, 40))
        self.AiButton1.setText(_fromUtf8(""))
        self.AiButton1.setObjectName(_fromUtf8("AiButton1"))
        self.AiCombo1 = QtGui.QComboBox(self.frame)
        self.AiCombo1.setGeometry(QtCore.QRect(140, 340, 250, 27))
        self.AiCombo1.setObjectName(_fromUtf8("AiCombo1"))
        self.AiButton2 = QtGui.QPushButton(self.frame)
        self.AiButton2.setGeometry(QtCore.QRect(40, 420, 40, 40))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AiButton2.sizePolicy().hasHeightForWidth())
        self.AiButton2.setSizePolicy(sizePolicy)
        self.AiButton2.setText(_fromUtf8(""))
        self.AiButton2.setObjectName(_fromUtf8("AiButton2"))
        self.AiCombo2 = QtGui.QComboBox(self.frame)
        self.AiCombo2.setGeometry(QtCore.QRect(140, 430, 250, 27))
        self.AiCombo2.setObjectName(_fromUtf8("AiCombo2"))
        self.mapCombo = QtGui.QComboBox(self.frame)
        self.mapCombo.setGeometry(QtCore.QRect(140, 520, 250, 27))
        self.mapCombo.setObjectName(_fromUtf8("mapCombo"))
        self.mapButton = QtGui.QPushButton(self.frame)
        self.mapButton.setGeometry(QtCore.QRect(40, 510, 40, 40))
        self.mapButton.setText(_fromUtf8(""))
        self.mapButton.setObjectName(_fromUtf8("mapButton"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(60, 660, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.roundLCD = QtGui.QLCDNumber(self.frame)
        self.roundLCD.setGeometry(QtCore.QRect(180, 650, 91, 41))
        self.roundLCD.setObjectName(_fromUtf8("roundLCD"))
        self.startButton = QtGui.QPushButton(self.frame)
        self.startButton.setGeometry(QtCore.QRect(180, 30, 40, 40))
        self.startButton.setText(_fromUtf8(""))
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.returnButton = QtGui.QPushButton(self.frame)
        self.returnButton.setGeometry(QtCore.QRect(40, 30, 40, 40))
        self.returnButton.setText(_fromUtf8(""))
        self.returnButton.setObjectName(_fromUtf8("returnButton"))
        self.exitButton = QtGui.QPushButton(self.frame)
        self.exitButton.setGeometry(QtCore.QRect(110, 30, 40, 40))
        self.exitButton.setText(_fromUtf8(""))
        self.exitButton.setObjectName(_fromUtf8("exitButton"))

        self.retranslateUi(AIvsAI)
        QtCore.QMetaObject.connectSlotsByName(AIvsAI)

    def retranslateUi(self, AIvsAI):
        AIvsAI.setWindowTitle(_translate("AIvsAI", "Form", None))
        self.label.setText(_translate("AIvsAI", " 回合数：", None))

