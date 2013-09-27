# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'part_replaymap.ui'
#
# Created: Wed Sep 25 15:47:08 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Replaymap(object):
    def setupUi(self, Replaymap):
        Replaymap.setObjectName(_fromUtf8("Replaymap"))
        Replaymap.setWindowModality(QtCore.Qt.NonModal)
        Replaymap.resize(831, 501)
        self.horizontalLayoutWidget = QtGui.QWidget(Replaymap)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(19, 19, 791, 471))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.replayLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.replayLayout.setMargin(0)
        self.replayLayout.setObjectName(_fromUtf8("replayLayout"))

        self.retranslateUi(Replaymap)
        QtCore.QMetaObject.connectSlotsByName(Replaymap)

    def retranslateUi(self, Replaymap):
        Replaymap.setWindowTitle(QtGui.QApplication.translate("Replaymap", "Form", None, QtGui.QApplication.UnicodeUTF8))

