# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ResultDialog.ui'
#
# Created: Fri Nov 01 20:57:51 2013
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

class Ui_ResultDialog(object):
    def setupUi(self, ResultDialog):
        ResultDialog.setObjectName(_fromUtf8("ResultDialog"))
        ResultDialog.setWindowModality(QtCore.Qt.WindowModal)
        ResultDialog.resize(400, 300)
        ResultDialog.setStyleSheet(_fromUtf8("QDialog#ResultDialog{\n"
"    border-image: url(:/TestMode/resultback.png);}"))
        self.label = QtGui.QLabel(ResultDialog)
        self.label.setGeometry(QtCore.QRect(50, 30, 101, 41))
        self.label.setStyleSheet(_fromUtf8("color: rgb(255, 170, 0);"))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(ResultDialog)
        self.label_2.setGeometry(QtCore.QRect(60, 180, 101, 41))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.scoreLabel = QtGui.QLabel(ResultDialog)
        self.scoreLabel.setGeometry(QtCore.QRect(80, 80, 281, 91))
        self.scoreLabel.setStyleSheet(_fromUtf8("color: rgb(255, 0, 0);\n"
"font: 72pt \"Adobe Arabic\";"))
        self.scoreLabel.setObjectName(_fromUtf8("scoreLabel"))
        self.maxLabel = QtGui.QLabel(ResultDialog)
        self.maxLabel.setGeometry(QtCore.QRect(180, 180, 161, 51))
        self.maxLabel.setStyleSheet(_fromUtf8("color: rgb(255, 0, 0);\n"
"font: 36pt \"Adobe Arabic\";"))
        self.maxLabel.setObjectName(_fromUtf8("maxLabel"))
        self.exitBtn = QtGui.QPushButton(ResultDialog)
        self.exitBtn.setGeometry(QtCore.QRect(320, 230, 50, 50))
        self.exitBtn.setStyleSheet(_fromUtf8("QPushButton{\n"
"    border-image: url(:/TestMode/exit0.png);}\n"
"QPushButton:hover{\n"
"    border-image: url(:/TestMode/exit1.png);}"))
        self.exitBtn.setText(_fromUtf8(""))
        self.exitBtn.setObjectName(_fromUtf8("exitBtn"))
        self.loseLabel = QtGui.QLabel(ResultDialog)
        self.loseLabel.setGeometry(QtCore.QRect(220, 30, 141, 131))
        self.loseLabel.setText(_fromUtf8(""))
        self.loseLabel.setObjectName(_fromUtf8("loseLabel"))

        self.retranslateUi(ResultDialog)
        QtCore.QMetaObject.connectSlotsByName(ResultDialog)

    def retranslateUi(self, ResultDialog):
        ResultDialog.setWindowTitle(_translate("ResultDialog", "结果", None))
        self.label.setText(_translate("ResultDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'黑体\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600; color:#55aaff;\">您的分数：</span></p></body></html>", None))
        self.label_2.setText(_translate("ResultDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'黑体\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600; color:#55aaff;\">最高分：</span></p></body></html>", None))
        self.scoreLabel.setText(_translate("ResultDialog", "800", None))
        self.maxLabel.setText(_translate("ResultDialog", "2000", None))

import test_TestMode_rc
