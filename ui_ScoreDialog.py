# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ScoreDialog.ui'
#
# Created: Fri Nov 01 21:33:26 2013
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

class Ui_ScoreDialog(object):
    def setupUi(self, ScoreDialog):
        ScoreDialog.setObjectName(_fromUtf8("ScoreDialog"))
        ScoreDialog.resize(501, 469)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ScoreDialog.sizePolicy().hasHeightForWidth())
        ScoreDialog.setSizePolicy(sizePolicy)
        ScoreDialog.setStyleSheet(_fromUtf8("QDialog#ScoreDialog{\n"
"    border-image: url(:/TestMode/scoreBack.png);}\n"
"QLabel#label1, #label2, #label3, #label4, #label5, #label6, #label7, #label8, #label9, #label10{\n"
"    font: 30pt \"Adobe Arabic\";\n"
"color: rgb(255, 0, 0);}\n"
"QLabel#label_2, #label_3, #label_4, #label_5, #label_6, #label_7, #label_8, #label_9, #label_10, #label_11{\n"
"    font: 20pt \"黑体\";\n"
"color: rgb(255, 0, 0);}\n"
"\n"
""))
        self.label = QtGui.QLabel(ScoreDialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 491, 41))
        self.label.setStyleSheet(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.okBtn = QtGui.QPushButton(ScoreDialog)
        self.okBtn.setGeometry(QtCore.QRect(420, 410, 50, 50))
        self.okBtn.setStyleSheet(_fromUtf8("QPushButton{\n"
"    border-image: url(:/TestMode/exit0.png);}\n"
"QPushButton:hover{\n"
"    border-image: url(:/TestMode/exit1.png);}"))
        self.okBtn.setText(_fromUtf8(""))
        self.okBtn.setObjectName(_fromUtf8("okBtn"))
        self.label5 = QtGui.QLabel(ScoreDialog)
        self.label5.setGeometry(QtCore.QRect(194, 257, 171, 40))
        self.label5.setObjectName(_fromUtf8("label5"))
        self.label2 = QtGui.QLabel(ScoreDialog)
        self.label2.setGeometry(QtCore.QRect(194, 110, 181, 40))
        self.label2.setObjectName(_fromUtf8("label2"))
        self.label6 = QtGui.QLabel(ScoreDialog)
        self.label6.setGeometry(QtCore.QRect(194, 306, 171, 40))
        self.label6.setObjectName(_fromUtf8("label6"))
        self.label1 = QtGui.QLabel(ScoreDialog)
        self.label1.setGeometry(QtCore.QRect(194, 61, 181, 40))
        self.label1.setObjectName(_fromUtf8("label1"))
        self.label_3 = QtGui.QLabel(ScoreDialog)
        self.label_3.setGeometry(QtCore.QRect(41, 110, 147, 43))
        self.label_3.setMinimumSize(QtCore.QSize(147, 43))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label7 = QtGui.QLabel(ScoreDialog)
        self.label7.setGeometry(QtCore.QRect(194, 355, 171, 40))
        self.label7.setObjectName(_fromUtf8("label7"))
        self.label4 = QtGui.QLabel(ScoreDialog)
        self.label4.setGeometry(QtCore.QRect(194, 208, 171, 40))
        self.label4.setIndent(-4)
        self.label4.setObjectName(_fromUtf8("label4"))
        self.label3 = QtGui.QLabel(ScoreDialog)
        self.label3.setGeometry(QtCore.QRect(194, 159, 181, 40))
        self.label3.setObjectName(_fromUtf8("label3"))
        self.label_2 = QtGui.QLabel(ScoreDialog)
        self.label_2.setGeometry(QtCore.QRect(41, 61, 147, 43))
        self.label_2.setMinimumSize(QtCore.QSize(147, 43))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_6 = QtGui.QLabel(ScoreDialog)
        self.label_6.setGeometry(QtCore.QRect(41, 257, 147, 43))
        self.label_6.setMinimumSize(QtCore.QSize(147, 43))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(ScoreDialog)
        self.label_7.setGeometry(QtCore.QRect(41, 306, 147, 43))
        self.label_7.setMinimumSize(QtCore.QSize(147, 43))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(ScoreDialog)
        self.label_8.setGeometry(QtCore.QRect(41, 355, 147, 43))
        self.label_8.setMinimumSize(QtCore.QSize(147, 43))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_4 = QtGui.QLabel(ScoreDialog)
        self.label_4.setGeometry(QtCore.QRect(41, 159, 147, 43))
        self.label_4.setMinimumSize(QtCore.QSize(147, 43))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(ScoreDialog)
        self.label_5.setGeometry(QtCore.QRect(41, 208, 147, 43))
        self.label_5.setMinimumSize(QtCore.QSize(147, 43))
        self.label_5.setObjectName(_fromUtf8("label_5"))

        self.retranslateUi(ScoreDialog)
        QtCore.QMetaObject.connectSlotsByName(ScoreDialog)

    def retranslateUi(self, ScoreDialog):
        ScoreDialog.setWindowTitle(_translate("ScoreDialog", "记录", None))
        self.label.setText(_translate("ScoreDialog", "战士 朴大神哈哈 的战绩：", None))
        self.okBtn.setToolTip(_translate("ScoreDialog", "退出", None))
        self.okBtn.setWhatsThis(_translate("ScoreDialog", "退出", None))
        self.label5.setText(_translate("ScoreDialog", "TextLabel", None))
        self.label2.setText(_translate("ScoreDialog", "3000000000000", None))
        self.label6.setText(_translate("ScoreDialog", "TextLabel", None))
        self.label1.setText(_translate("ScoreDialog", "20", None))
        self.label_3.setText(_translate("ScoreDialog", "第二关", None))
        self.label7.setText(_translate("ScoreDialog", "TextLabel", None))
        self.label4.setText(_translate("ScoreDialog", "800820", None))
        self.label3.setText(_translate("ScoreDialog", "582", None))
        self.label_2.setText(_translate("ScoreDialog", "第一关", None))
        self.label_6.setText(_translate("ScoreDialog", "第五关", None))
        self.label_7.setText(_translate("ScoreDialog", "第六关", None))
        self.label_8.setText(_translate("ScoreDialog", "第七关", None))
        self.label_4.setText(_translate("ScoreDialog", "第三关", None))
        self.label_5.setText(_translate("ScoreDialog", "第四关", None))

import test_TestMode_rc
