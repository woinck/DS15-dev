# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'part_replaymap.ui'
#
# Created: Mon Oct 07 20:25:24 2013
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

class Ui_Replaymap(object):
    def setupUi(self, Replaymap):
        Replaymap.setObjectName(_fromUtf8("Replaymap"))
        Replaymap.setWindowModality(QtCore.Qt.NonModal)
        Replaymap.resize(669, 520)
        self.horizontalLayoutWidget = QtGui.QWidget(Replaymap)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 621, 481))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.replayLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.replayLayout.setMargin(0)
        self.replayLayout.setObjectName(_fromUtf8("replayLayout"))

        self.retranslateUi(Replaymap)
        QtCore.QMetaObject.connectSlotsByName(Replaymap)

    def retranslateUi(self, Replaymap):
        Replaymap.setWindowTitle(_translate("Replaymap", "Form", None))

