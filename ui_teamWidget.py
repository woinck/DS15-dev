# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'part_teamWidget.ui'
#
# Created: Wed Oct 09 23:13:43 2013
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

class Ui_TeamWidget(object):
    def setupUi(self, TeamWidget):
        TeamWidget.setObjectName(_fromUtf8("TeamWidget"))
        TeamWidget.resize(1024, 768)
        self.horizontalLayoutWidget = QtGui.QWidget(TeamWidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 450, 1031, 131))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.titleLabel = QtGui.QLabel(TeamWidget)
        self.titleLabel.setGeometry(QtCore.QRect(430, 350, 150, 50))
        self.titleLabel.setText(_fromUtf8(""))
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.returnButton = QtGui.QPushButton(TeamWidget)
        self.returnButton.setGeometry(QtCore.QRect(430, 630, 145, 50))
        self.returnButton.setText(_fromUtf8(""))
        self.returnButton.setObjectName(_fromUtf8("returnButton"))

        self.retranslateUi(TeamWidget)
        QtCore.QMetaObject.connectSlotsByName(TeamWidget)

    def retranslateUi(self, TeamWidget):
        TeamWidget.setWindowTitle(_translate("TeamWidget", "Form", None))

