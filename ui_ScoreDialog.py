# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ScoreDialog.ui'
#
# Created: Thu Oct 31 00:17:45 2013
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
        ScoreDialog.resize(502, 602)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ScoreDialog.sizePolicy().hasHeightForWidth())
        ScoreDialog.setSizePolicy(sizePolicy)
        ScoreDialog.setStyleSheet(_fromUtf8("QDialog#ScoreDialog{\n"
"    border-image: url(:/TestMode/start.png);}\n"
"QLabel{\n"
"font: 75 28pt \"Adobe Arabic\";\n"
"color: rgb(255, 0, 0);}\n"
""))
        self.label = QtGui.QLabel(ScoreDialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 411, 41))
        self.label.setStyleSheet(_fromUtf8("font: 20pt \"黑体\";\n"
"color: rgb(255, 255, 0);"))
        self.label.setObjectName(_fromUtf8("label"))
        self.okBtn = QtGui.QPushButton(ScoreDialog)
        self.okBtn.setGeometry(QtCore.QRect(430, 545, 50, 50))
        self.okBtn.setStyleSheet(_fromUtf8("QPushButton{\n"
"    border-image: url(:/TestMode/exit0.png);}\n"
"QPushButton:hover{\n"
"    border-image: url(:/TestMode/exit1.png);}"))
        self.okBtn.setText(_fromUtf8(""))
        self.okBtn.setObjectName(_fromUtf8("okBtn"))
        self.gridLayoutWidget = QtGui.QWidget(ScoreDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 60, 401, 486))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label1 = QtGui.QLabel(self.gridLayoutWidget)
        self.label1.setObjectName(_fromUtf8("label1"))
        self.gridLayout.addWidget(self.label1, 0, 1, 1, 1)
        self.label4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label4.setObjectName(_fromUtf8("label4"))
        self.gridLayout.addWidget(self.label4, 3, 1, 1, 1)
        self.label3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label3.setObjectName(_fromUtf8("label3"))
        self.gridLayout.addWidget(self.label3, 2, 1, 1, 1)
        self.label5 = QtGui.QLabel(self.gridLayoutWidget)
        self.label5.setObjectName(_fromUtf8("label5"))
        self.gridLayout.addWidget(self.label5, 4, 1, 1, 1)
        self.label2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label2.setObjectName(_fromUtf8("label2"))
        self.gridLayout.addWidget(self.label2, 1, 1, 1, 1)
        self.label6 = QtGui.QLabel(self.gridLayoutWidget)
        self.label6.setObjectName(_fromUtf8("label6"))
        self.gridLayout.addWidget(self.label6, 5, 1, 1, 1)
        self.label7 = QtGui.QLabel(self.gridLayoutWidget)
        self.label7.setObjectName(_fromUtf8("label7"))
        self.gridLayout.addWidget(self.label7, 6, 1, 1, 1)
        self.label8 = QtGui.QLabel(self.gridLayoutWidget)
        self.label8.setObjectName(_fromUtf8("label8"))
        self.gridLayout.addWidget(self.label8, 7, 1, 1, 1)
        self.label10 = QtGui.QLabel(self.gridLayoutWidget)
        self.label10.setObjectName(_fromUtf8("label10"))
        self.gridLayout.addWidget(self.label10, 9, 1, 1, 1)
        self.label9 = QtGui.QLabel(self.gridLayoutWidget)
        self.label9.setObjectName(_fromUtf8("label9"))
        self.gridLayout.addWidget(self.label9, 8, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(147, 43))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setMinimumSize(QtCore.QSize(147, 43))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4.setMinimumSize(QtCore.QSize(147, 43))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_5.setMinimumSize(QtCore.QSize(147, 43))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_6.setMinimumSize(QtCore.QSize(147, 43))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.label_7 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_7.setMinimumSize(QtCore.QSize(147, 43))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_8.setMinimumSize(QtCore.QSize(147, 43))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 6, 0, 1, 1)
        self.label_9 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_9.setMinimumSize(QtCore.QSize(147, 43))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 7, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_10.setMinimumSize(QtCore.QSize(147, 43))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 8, 0, 1, 1)
        self.label_11 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_11.setMinimumSize(QtCore.QSize(147, 43))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 9, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 5)

        self.retranslateUi(ScoreDialog)
        QtCore.QMetaObject.connectSlotsByName(ScoreDialog)

    def retranslateUi(self, ScoreDialog):
        ScoreDialog.setWindowTitle(_translate("ScoreDialog", "记录", None))
        self.label.setText(_translate("ScoreDialog", "TextLabel", None))
        self.okBtn.setToolTip(_translate("ScoreDialog", "退出", None))
        self.okBtn.setWhatsThis(_translate("ScoreDialog", "退出", None))
        self.label1.setText(_translate("ScoreDialog", "TextLabel", None))
        self.label4.setText(_translate("ScoreDialog", "TextLabel", None))
        self.label3.setText(_translate("ScoreDialog", "label3", None))
        self.label5.setText(_translate("ScoreDialog", "TextLabel", None))
        self.label2.setText(_translate("ScoreDialog", "TextLabel", None))
        self.label6.setText(_translate("ScoreDialog", "TextLabel", None))
        self.label7.setText(_translate("ScoreDialog", "TextLabel", None))
        self.label8.setText(_translate("ScoreDialog", "TextLabel", None))
        self.label10.setText(_translate("ScoreDialog", "TextLabel", None))
        self.label9.setText(_translate("ScoreDialog", "TextLabel", None))
        self.label_2.setText(_translate("ScoreDialog", "第一关", None))
        self.label_3.setText(_translate("ScoreDialog", "第二关", None))
        self.label_4.setText(_translate("ScoreDialog", "第三关", None))
        self.label_5.setText(_translate("ScoreDialog", "第四关", None))
        self.label_6.setText(_translate("ScoreDialog", "第五关", None))
        self.label_7.setText(_translate("ScoreDialog", "第六关", None))
        self.label_8.setText(_translate("ScoreDialog", "第七关", None))
        self.label_9.setText(_translate("ScoreDialog", "第八关", None))
        self.label_10.setText(_translate("ScoreDialog", "第九关", None))
        self.label_11.setText(_translate("ScoreDialog", "第十关", None))

import test_TestMode_rc
