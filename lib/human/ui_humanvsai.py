# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'part_humanvsai.ui'
#
# Created: Tue Oct 01 00:19:18 2013
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

class Ui_HumanvsAi(object):
    def setupUi(self, HumanvsAi):
        HumanvsAi.setObjectName(_fromUtf8("HumanvsAi"))
        HumanvsAi.resize(1024, 684)
        self.aiButton = QtGui.QPushButton(HumanvsAi)
        self.aiButton.setGeometry(QtCore.QRect(10, 490, 40, 40))
        self.aiButton.setText(_fromUtf8(""))
        self.aiButton.setObjectName(_fromUtf8("aiButton"))
        self.info_ai = QtGui.QLineEdit(HumanvsAi)
        self.info_ai.setGeometry(QtCore.QRect(70, 500, 141, 30))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_ai.sizePolicy().hasHeightForWidth())
        self.info_ai.setSizePolicy(sizePolicy)
        self.info_ai.setAutoFillBackground(False)
        self.info_ai.setReadOnly(True)
        self.info_ai.setObjectName(_fromUtf8("info_ai"))
        self.mapButton = QtGui.QPushButton(HumanvsAi)
        self.mapButton.setGeometry(QtCore.QRect(10, 550, 40, 40))
        self.mapButton.setText(_fromUtf8(""))
        self.mapButton.setObjectName(_fromUtf8("mapButton"))
        self.info_map = QtGui.QLineEdit(HumanvsAi)
        self.info_map.setGeometry(QtCore.QRect(70, 560, 141, 30))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_map.sizePolicy().hasHeightForWidth())
        self.info_map.setSizePolicy(sizePolicy)
        self.info_map.setObjectName(_fromUtf8("info_map"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(HumanvsAi)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(830, 140, 181, 431))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.startButton = QtGui.QPushButton(HumanvsAi)
        self.startButton.setGeometry(QtCore.QRect(10, 610, 40, 40))
        self.startButton.setText(_fromUtf8(""))
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.returnButton = QtGui.QPushButton(HumanvsAi)
        self.returnButton.setGeometry(QtCore.QRect(40, 20, 40, 40))
        self.returnButton.setText(_fromUtf8(""))
        self.returnButton.setObjectName(_fromUtf8("returnButton"))
        self.verticalLayoutWidget_3 = QtGui.QWidget(HumanvsAi)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(230, 80, 591, 531))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.helpButton = QtGui.QPushButton(HumanvsAi)
        self.helpButton.setGeometry(QtCore.QRect(120, 20, 40, 40))
        self.helpButton.setText(_fromUtf8(""))
        self.helpButton.setObjectName(_fromUtf8("helpButton"))
        self.label = QtGui.QLabel(HumanvsAi)
        self.label.setGeometry(QtCore.QRect(60, 80, 101, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("SimHei"))
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.playerLabel = QtGui.QLabel(HumanvsAi)
        self.playerLabel.setGeometry(QtCore.QRect(830, 80, 161, 41))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.playerLabel.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("SimHei"))
        font.setPointSize(20)
        self.playerLabel.setFont(font)
        self.playerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.playerLabel.setObjectName(_fromUtf8("playerLabel"))

        self.retranslateUi(HumanvsAi)
        QtCore.QMetaObject.connectSlotsByName(HumanvsAi)

    def retranslateUi(self, HumanvsAi):
        HumanvsAi.setWindowTitle(_translate("HumanvsAi", "Form", None))
        self.label.setText(_translate("HumanvsAi", "AI", None))
        self.playerLabel.setText(_translate("HumanvsAi", "Player", None))

