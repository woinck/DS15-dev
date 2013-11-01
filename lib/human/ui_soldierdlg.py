# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'part_soldierdlg.ui'
#
# Created: Sat Nov 02 00:33:26 2013
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

class Ui_GetSoldierTypeDialog(object):
    def setupUi(self, GetSoldierTypeDialog):
        GetSoldierTypeDialog.setObjectName(_fromUtf8("GetSoldierTypeDialog"))
        GetSoldierTypeDialog.resize(435, 323)
        self.buttonBox = QtGui.QDialogButtonBox(GetSoldierTypeDialog)
        self.buttonBox.setGeometry(QtCore.QRect(80, 280, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.soldierButton0 = QtGui.QPushButton(GetSoldierTypeDialog)
        self.soldierButton0.setGeometry(QtCore.QRect(50, 20, 80, 80))
        self.soldierButton0.setText(_fromUtf8(""))
        self.soldierButton0.setObjectName(_fromUtf8("soldierButton0"))
        self.soldierButton1 = QtGui.QPushButton(GetSoldierTypeDialog)
        self.soldierButton1.setGeometry(QtCore.QRect(180, 20, 80, 80))
        self.soldierButton1.setText(_fromUtf8(""))
        self.soldierButton1.setObjectName(_fromUtf8("soldierButton1"))
        self.soldierButton2 = QtGui.QPushButton(GetSoldierTypeDialog)
        self.soldierButton2.setGeometry(QtCore.QRect(310, 20, 80, 80))
        self.soldierButton2.setText(_fromUtf8(""))
        self.soldierButton2.setObjectName(_fromUtf8("soldierButton2"))
        self.soldierButton4 = QtGui.QPushButton(GetSoldierTypeDialog)
        self.soldierButton4.setGeometry(QtCore.QRect(180, 150, 80, 80))
        self.soldierButton4.setText(_fromUtf8(""))
        self.soldierButton4.setObjectName(_fromUtf8("soldierButton4"))
        self.soldierButton5 = QtGui.QPushButton(GetSoldierTypeDialog)
        self.soldierButton5.setGeometry(QtCore.QRect(310, 150, 80, 80))
        self.soldierButton5.setText(_fromUtf8(""))
        self.soldierButton5.setObjectName(_fromUtf8("soldierButton5"))
        self.soldierButton3 = QtGui.QPushButton(GetSoldierTypeDialog)
        self.soldierButton3.setGeometry(QtCore.QRect(50, 150, 80, 80))
        self.soldierButton3.setText(_fromUtf8(""))
        self.soldierButton3.setObjectName(_fromUtf8("soldierButton3"))
        self.label = QtGui.QLabel(GetSoldierTypeDialog)
        self.label.setGeometry(QtCore.QRect(60, 110, 61, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(GetSoldierTypeDialog)
        self.label_2.setGeometry(QtCore.QRect(190, 110, 61, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(GetSoldierTypeDialog)
        self.label_3.setGeometry(QtCore.QRect(310, 110, 81, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(GetSoldierTypeDialog)
        self.label_4.setGeometry(QtCore.QRect(60, 240, 61, 20))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(GetSoldierTypeDialog)
        self.label_5.setGeometry(QtCore.QRect(190, 240, 61, 20))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(GetSoldierTypeDialog)
        self.label_6.setGeometry(QtCore.QRect(320, 240, 61, 20))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))

        self.retranslateUi(GetSoldierTypeDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), GetSoldierTypeDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), GetSoldierTypeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GetSoldierTypeDialog)

    def retranslateUi(self, GetSoldierTypeDialog):
        GetSoldierTypeDialog.setWindowTitle(_translate("GetSoldierTypeDialog", "Dialog", None))
        self.label.setText(_translate("GetSoldierTypeDialog", "能量剑士", None))
        self.label_2.setText(_translate("GetSoldierTypeDialog", "生化突击手", None))
        self.label_3.setText(_translate("GetSoldierTypeDialog", "等离子狙击手", None))
        self.label_4.setText(_translate("GetSoldierTypeDialog", "战机", None))
        self.label_5.setText(_translate("GetSoldierTypeDialog", "坦克", None))
        self.label_6.setText(_translate("GetSoldierTypeDialog", "治疗师", None))

