# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'part_herotypedlg.ui'
#
# Created: Wed Sep  4 16:04:06 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_HeroTypeDlg(object):
    def setupUi(self, HeroTypeDlg):
        HeroTypeDlg.setObjectName(_fromUtf8("HeroTypeDlg"))
        HeroTypeDlg.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(HeroTypeDlg)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.heroButton1 = QtGui.QPushButton(HeroTypeDlg)
        self.heroButton1.setGeometry(QtCore.QRect(20, 60, 80, 80))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.heroButton1.sizePolicy().hasHeightForWidth())
        self.heroButton1.setSizePolicy(sizePolicy)
        self.heroButton1.setText(_fromUtf8(""))
        self.heroButton1.setCheckable(True)
        self.heroButton1.setObjectName(_fromUtf8("heroButton1"))
        self.heroButton2 = QtGui.QPushButton(HeroTypeDlg)
        self.heroButton2.setGeometry(QtCore.QRect(150, 60, 80, 80))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.heroButton2.sizePolicy().hasHeightForWidth())
        self.heroButton2.setSizePolicy(sizePolicy)
        self.heroButton2.setText(_fromUtf8(""))
        self.heroButton2.setCheckable(True)
        self.heroButton2.setObjectName(_fromUtf8("heroButton2"))
        self.heroButton3 = QtGui.QPushButton(HeroTypeDlg)
        self.heroButton3.setGeometry(QtCore.QRect(290, 60, 80, 80))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.heroButton3.sizePolicy().hasHeightForWidth())
        self.heroButton3.setSizePolicy(sizePolicy)
        self.heroButton3.setText(_fromUtf8(""))
        self.heroButton3.setCheckable(True)
        self.heroButton3.setObjectName(_fromUtf8("heroButton3"))
        self.label = QtGui.QLabel(HeroTypeDlg)
        self.label.setGeometry(QtCore.QRect(30, 170, 60, 19))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Loma"))
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(HeroTypeDlg)
        self.label_2.setGeometry(QtCore.QRect(160, 170, 60, 19))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Loma"))
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(HeroTypeDlg)
        self.label_3.setGeometry(QtCore.QRect(300, 170, 60, 19))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Loma"))
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.nameEdit = QtGui.QLineEdit(HeroTypeDlg)
        self.nameEdit.setGeometry(QtCore.QRect(160, 20, 113, 29))
        self.nameEdit.setObjectName(_fromUtf8("nameEdit"))
        self.label_4 = QtGui.QLabel(HeroTypeDlg)
        self.label_4.setGeometry(QtCore.QRect(80, 20, 61, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))

        self.retranslateUi(HeroTypeDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), HeroTypeDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), HeroTypeDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(HeroTypeDlg)

    def retranslateUi(self, HeroTypeDlg):
        HeroTypeDlg.setWindowTitle(QtGui.QApplication.translate("HeroTypeDlg", "选择英雄", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("HeroTypeDlg", "英雄1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("HeroTypeDlg", "英雄2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("HeroTypeDlg", "英雄3", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("HeroTypeDlg", "尊姓大名:", None, QtGui.QApplication.UnicodeUTF8))

