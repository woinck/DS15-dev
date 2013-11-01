# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'temp_TestMode.ui'
#
# Created: Fri Nov 01 01:44:24 2013
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

class Ui_TestModeWidget(object):
    def setupUi(self, TestModeWidget):
        TestModeWidget.setObjectName(_fromUtf8("TestModeWidget"))
        TestModeWidget.resize(1024, 768)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TestModeWidget.sizePolicy().hasHeightForWidth())
        TestModeWidget.setSizePolicy(sizePolicy)
        TestModeWidget.setMouseTracking(False)
        TestModeWidget.setStyleSheet(_fromUtf8("QWidget#testModeFrame{\n"
"background-image: url(:/TestMode/back.jpg);}\n"
""))
        self.testModeFrame = QtGui.QFrame(TestModeWidget)
        self.testModeFrame.setGeometry(QtCore.QRect(0, 0, 1024, 768))
        self.testModeFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.testModeFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.testModeFrame.setObjectName(_fromUtf8("testModeFrame"))
        self.scoreBtn = QtGui.QPushButton(self.testModeFrame)
        self.scoreBtn.setGeometry(QtCore.QRect(40, 30, 80, 80))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scoreBtn.sizePolicy().hasHeightForWidth())
        self.scoreBtn.setSizePolicy(sizePolicy)
        self.scoreBtn.setSizeIncrement(QtCore.QSize(128, 128))
        self.scoreBtn.setBaseSize(QtCore.QSize(0, 0))
        self.scoreBtn.setMouseTracking(True)
        self.scoreBtn.setStyleSheet(_fromUtf8("QPushButton{border-image: url(:/TestMode/score0.png);}\n"
"QPushButton:hover{\n"
"border-image: url(:/TestMode/score1.png);}"))
        self.scoreBtn.setText(_fromUtf8(""))
        self.scoreBtn.setObjectName(_fromUtf8("scoreBtn"))
        self.logOutBtn = QtGui.QPushButton(self.testModeFrame)
        self.logOutBtn.setGeometry(QtCore.QRect(140, 30, 80, 80))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logOutBtn.sizePolicy().hasHeightForWidth())
        self.logOutBtn.setSizePolicy(sizePolicy)
        self.logOutBtn.setMouseTracking(True)
        self.logOutBtn.setStyleSheet(_fromUtf8("QPushButton{\n"
"border-image: url(:/TestMode/logout0.png);}\n"
"QPushButton:hover{\n"
"    border-image: url(:/TestMode/logout1.png);}"))
        self.logOutBtn.setText(_fromUtf8(""))
        self.logOutBtn.setObjectName(_fromUtf8("logOutBtn"))
        self.exitBtn = QtGui.QPushButton(self.testModeFrame)
        self.exitBtn.setGeometry(QtCore.QRect(240, 30, 80, 80))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exitBtn.sizePolicy().hasHeightForWidth())
        self.exitBtn.setSizePolicy(sizePolicy)
        self.exitBtn.setStyleSheet(_fromUtf8("QPushButton{border-image: url(:/TestMode/exit0.png);}\n"
"QPushButton:hover{\n"
"border-image: url(:/TestMode/exit1.png);}"))
        self.exitBtn.setText(_fromUtf8(""))
        self.exitBtn.setObjectName(_fromUtf8("exitBtn"))
        self.startFrame = QtGui.QFrame(self.testModeFrame)
        self.startFrame.setGeometry(QtCore.QRect(210, 110, 803, 528))
        self.startFrame.setStyleSheet(_fromUtf8("QFrame#startFrame{\n"
"border-image: url(:/TestMode/startBack.png);}"))
        self.startFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.startFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.startFrame.setObjectName(_fromUtf8("startFrame"))
        self.aiPathEdit = QtGui.QLineEdit(self.testModeFrame)
        self.aiPathEdit.setGeometry(QtCore.QRect(40, 670, 321, 41))
        self.aiPathEdit.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255, 200);"))
        self.aiPathEdit.setObjectName(_fromUtf8("aiPathEdit"))
        self.loadAiBtn = QtGui.QPushButton(self.testModeFrame)
        self.loadAiBtn.setGeometry(QtCore.QRect(410, 659, 61, 61))
        self.loadAiBtn.setStyleSheet(_fromUtf8("QPushButton{\n"
"border-image: url(:/TestMode/openAi0.png);}\n"
"QPushButton:hover{\n"
"border-image: url(:/TestMode/openAi1.png);}"))
        self.loadAiBtn.setText(_fromUtf8(""))
        self.loadAiBtn.setObjectName(_fromUtf8("loadAiBtn"))
        self.movieLabel = QtGui.QLabel(self.testModeFrame)
        self.movieLabel.setGeometry(QtCore.QRect(670, 30, 251, 80))
        self.movieLabel.setText(_fromUtf8(""))
        self.movieLabel.setObjectName(_fromUtf8("movieLabel"))

        self.retranslateUi(TestModeWidget)
        QtCore.QMetaObject.connectSlotsByName(TestModeWidget)

    def retranslateUi(self, TestModeWidget):
        TestModeWidget.setWindowTitle(_translate("TestModeWidget", "Form", None))
        self.scoreBtn.setToolTip(_translate("TestModeWidget", "最高分", None))
        self.scoreBtn.setWhatsThis(_translate("TestModeWidget", "最高分", None))
        self.logOutBtn.setToolTip(_translate("TestModeWidget", "注销并退出", None))
        self.logOutBtn.setWhatsThis(_translate("TestModeWidget", "注销并退出", None))
        self.exitBtn.setToolTip(_translate("TestModeWidget", "退出", None))
        self.exitBtn.setWhatsThis(_translate("TestModeWidget", "退出", None))
        self.loadAiBtn.setToolTip(_translate("TestModeWidget", "载入AI", None))
        self.loadAiBtn.setWhatsThis(_translate("TestModeWidget", "载入AI", None))

import test_TestMode_rc
