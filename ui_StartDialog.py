# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StartDialog_new.ui'
#
# Created: Fri Nov 01 21:25:55 2013
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

class Ui_StartDialog(object):
    def setupUi(self, StartDialog):
        StartDialog.setObjectName(_fromUtf8("StartDialog"))
        StartDialog.resize(803, 528)
        StartDialog.setStyleSheet(_fromUtf8(""))
        self.frame = QtGui.QFrame(StartDialog)
        self.frame.setEnabled(True)
        self.frame.setGeometry(QtCore.QRect(0, 0, 803, 528))
        self.frame.setMouseTracking(True)
        self.frame.setStyleSheet(_fromUtf8("QLabel{\n"
"    font: 75 14pt \"黑体\";\n"
"    color: rgb(255, 255, 0);\n"
"}\n"
"QPushButton{\n"
"    border-image: url(:/TestMode/level1.png);}\n"
"QPushButton:hover{\n"
"    border-image: url(:/TestMode/level2.png);}\n"
"QPushButton:disabled{\n"
"    border-image: url(:/TestMode/level0.png);}"))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.button1 = Ui_ButtonWithDisplay(self.frame)
        self.button1.setEnabled(True)
        self.button1.setGeometry(QtCore.QRect(405, 25, 57, 50))
        self.button1.setText(_fromUtf8(""))
        self.button1.setObjectName(_fromUtf8("button1"))
        self.button2 = Ui_ButtonWithDisplay(self.frame)
        self.button2.setEnabled(True)
        self.button2.setGeometry(QtCore.QRect(570, 160, 57, 50))
        self.button2.setText(_fromUtf8(""))
        self.button2.setObjectName(_fromUtf8("button2"))
        self.button3 = Ui_ButtonWithDisplay(self.frame)
        self.button3.setEnabled(True)
        self.button3.setGeometry(QtCore.QRect(690, 140, 57, 50))
        self.button3.setText(_fromUtf8(""))
        self.button3.setObjectName(_fromUtf8("button3"))
        self.button4 = Ui_ButtonWithDisplay(self.frame)
        self.button4.setEnabled(True)
        self.button4.setGeometry(QtCore.QRect(640, 340, 57, 50))
        self.button4.setText(_fromUtf8(""))
        self.button4.setObjectName(_fromUtf8("button4"))
        self.button5 = Ui_ButtonWithDisplay(self.frame)
        self.button5.setEnabled(True)
        self.button5.setGeometry(QtCore.QRect(290, 440, 57, 50))
        self.button5.setText(_fromUtf8(""))
        self.button5.setObjectName(_fromUtf8("button5"))
        self.button6 = Ui_ButtonWithDisplay(self.frame)
        self.button6.setEnabled(True)
        self.button6.setGeometry(QtCore.QRect(420, 350, 57, 50))
        self.button6.setText(_fromUtf8(""))
        self.button6.setObjectName(_fromUtf8("button6"))
        self.button7 = Ui_ButtonWithDisplay(self.frame)
        self.button7.setEnabled(True)
        self.button7.setGeometry(QtCore.QRect(30, 360, 57, 50))
        self.button7.setText(_fromUtf8(""))
        self.button7.setObjectName(_fromUtf8("button7"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(400, 60, 101, 51))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(550, 210, 91, 51))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(620, 110, 91, 51))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_5 = QtGui.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(510, 360, 101, 51))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(650, 380, 101, 51))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label6_2 = QtGui.QLabel(self.frame)
        self.label6_2.setGeometry(QtCore.QRect(220, 460, 101, 51))
        self.label6_2.setObjectName(_fromUtf8("label6_2"))
        self.label_9 = QtGui.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(30, 400, 111, 51))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label1 = QtGui.QLabel(self.frame)
        self.label1.setGeometry(QtCore.QRect(460, 20, 131, 41))
        self.label1.setObjectName(_fromUtf8("label1"))
        self.label2 = QtGui.QLabel(self.frame)
        self.label2.setGeometry(QtCore.QRect(520, 250, 131, 41))
        self.label2.setObjectName(_fromUtf8("label2"))
        self.label3 = QtGui.QLabel(self.frame)
        self.label3.setGeometry(QtCore.QRect(650, 90, 131, 41))
        self.label3.setObjectName(_fromUtf8("label3"))
        self.label6 = QtGui.QLabel(self.frame)
        self.label6.setGeometry(QtCore.QRect(500, 400, 131, 41))
        self.label6.setObjectName(_fromUtf8("label6"))
        self.label4 = QtGui.QLabel(self.frame)
        self.label4.setGeometry(QtCore.QRect(630, 410, 131, 41))
        self.label4.setObjectName(_fromUtf8("label4"))
        self.label7 = QtGui.QLabel(self.frame)
        self.label7.setGeometry(QtCore.QRect(30, 430, 131, 41))
        self.label7.setObjectName(_fromUtf8("label7"))
        self.label5 = QtGui.QLabel(self.frame)
        self.label5.setGeometry(QtCore.QRect(350, 460, 131, 41))
        self.label5.setObjectName(_fromUtf8("label5"))

        self.retranslateUi(StartDialog)
        QtCore.QMetaObject.connectSlotsByName(StartDialog)

    def retranslateUi(self, StartDialog):
        StartDialog.setWindowTitle(_translate("StartDialog", "Form", None))
        self.label.setText(_translate("StartDialog", "Level 1", None))
        self.label_2.setText(_translate("StartDialog", "Level 2", None))
        self.label_3.setText(_translate("StartDialog", "Level 3", None))
        self.label_5.setText(_translate("StartDialog", "Level 6", None))
        self.label_6.setText(_translate("StartDialog", "Level 4", None))
        self.label6_2.setText(_translate("StartDialog", "Level 5", None))
        self.label_9.setText(_translate("StartDialog", "Level 7", None))
        self.label1.setText(_translate("StartDialog", "最高分：", None))
        self.label2.setText(_translate("StartDialog", "最高分：", None))
        self.label3.setText(_translate("StartDialog", "最高分：", None))
        self.label6.setText(_translate("StartDialog", "最高分：", None))
        self.label4.setText(_translate("StartDialog", "最高分：", None))
        self.label7.setText(_translate("StartDialog", "最高分：", None))
        self.label5.setText(_translate("StartDialog", "最高分：", None))

from ui_buttonwithdisplay import Ui_ButtonWithDisplay
import test_TestMode_rc
