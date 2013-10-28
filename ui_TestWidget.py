# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'temp_TestMode.ui'
#
# Created: Mon Oct 28 23:18:01 2013
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
        TestModeWidget.setMouseTracking(False)
        TestModeWidget.setStyleSheet(_fromUtf8("QWidget#frame{\n"
"background-image: url(:/TestMode/back.jpg);}\n"
"QWidget{background-color: rgba(0, 0, 0, 0);}"))
        self.frame = QtGui.QFrame(TestModeWidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1024, 768))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.scoreBtn = QtGui.QPushButton(self.frame)
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
        self.startBtn = QtGui.QPushButton(self.frame)
        self.startBtn.setGeometry(QtCore.QRect(140, 30, 80, 80))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startBtn.sizePolicy().hasHeightForWidth())
        self.startBtn.setSizePolicy(sizePolicy)
        self.startBtn.setMouseTracking(True)
        self.startBtn.setStyleSheet(_fromUtf8("QPushButton{\n"
"    border-image: url(:/TestMode/temp_start0.png);}\n"
"QPushButton:hover{\n"
"    border-image: url(:/TestMode/temp_start1.png);}"))
        self.startBtn.setText(_fromUtf8(""))
        self.startBtn.setObjectName(_fromUtf8("startBtn"))
        self.exitBtn = QtGui.QPushButton(self.frame)
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

        self.retranslateUi(TestModeWidget)
        QtCore.QMetaObject.connectSlotsByName(TestModeWidget)

    def retranslateUi(self, TestModeWidget):
        TestModeWidget.setWindowTitle(_translate("TestModeWidget", "Form", None))
        self.scoreBtn.setToolTip(_translate("TestModeWidget", "最高分", None))
        self.scoreBtn.setWhatsThis(_translate("TestModeWidget", "最高分", None))
        self.startBtn.setToolTip(_translate("TestModeWidget", "进入测试赛", None))
        self.startBtn.setWhatsThis(_translate("TestModeWidget", "进入测试赛", None))
        self.exitBtn.setToolTip(_translate("TestModeWidget", "退出", None))
        self.exitBtn.setWhatsThis(_translate("TestModeWidget", "退出", None))

import test_TestMode_rc
