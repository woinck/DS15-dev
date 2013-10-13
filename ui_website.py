# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'part_website.ui'
#
# Created: Mon Oct 14 01:01:10 2013
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

class Ui_webWidget(object):
    def setupUi(self, webWidget):
        webWidget.setObjectName(_fromUtf8("webWidget"))
        webWidget.resize(1024, 768)
        self.verticalLayoutWidget = QtGui.QWidget(webWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1021, 711))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.returnButton = QtGui.QPushButton(webWidget)
        self.returnButton.setGeometry(QtCore.QRect(480, 720, 50, 50))
        self.returnButton.setText(_fromUtf8(""))
        self.returnButton.setObjectName(_fromUtf8("returnButton"))

        self.retranslateUi(webWidget)
        QtCore.QMetaObject.connectSlotsByName(webWidget)

    def retranslateUi(self, webWidget):
        webWidget.setWindowTitle(_translate("webWidget", "Form", None))

