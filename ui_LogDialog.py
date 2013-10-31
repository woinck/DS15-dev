# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LogDialog.ui'
#
# Created: Thu Oct 31 00:17:22 2013
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

class Ui_LogDialog(object):
    def setupUi(self, LogDialog):
        LogDialog.setObjectName(_fromUtf8("LogDialog"))
        LogDialog.resize(400, 300)
        LogDialog.setStyleSheet(_fromUtf8("QWidget{\n"
"    background-color: rgb(255, 255, 255);}"))
        self.gridLayoutWidget = QtGui.QWidget(LogDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(70, 80, 251, 111))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pwLabel = QtGui.QLabel(self.gridLayoutWidget)
        self.pwLabel.setObjectName(_fromUtf8("pwLabel"))
        self.gridLayout.addWidget(self.pwLabel, 1, 0, 1, 1)
        self.nameLabel = QtGui.QLabel(self.gridLayoutWidget)
        self.nameLabel.setObjectName(_fromUtf8("nameLabel"))
        self.gridLayout.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.nameEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.nameEdit.setObjectName(_fromUtf8("nameEdit"))
        self.gridLayout.addWidget(self.nameEdit, 0, 1, 1, 1)
        self.pwEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.pwEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.pwEdit.setObjectName(_fromUtf8("pwEdit"))
        self.gridLayout.addWidget(self.pwEdit, 1, 1, 1, 1)
        self.horizontalLayoutWidget = QtGui.QWidget(LogDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(200, 200, 160, 80))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.okBtn = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.okBtn.setObjectName(_fromUtf8("okBtn"))
        self.horizontalLayout.addWidget(self.okBtn)
        self.cancelBtn = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.cancelBtn.setObjectName(_fromUtf8("cancelBtn"))
        self.horizontalLayout.addWidget(self.cancelBtn)
        self.pwLabel.setBuddy(self.pwEdit)
        self.nameLabel.setBuddy(self.nameEdit)

        self.retranslateUi(LogDialog)
        QtCore.QMetaObject.connectSlotsByName(LogDialog)

    def retranslateUi(self, LogDialog):
        LogDialog.setWindowTitle(_translate("LogDialog", "LogIn", None))
        self.pwLabel.setText(_translate("LogDialog", "密码：", None))
        self.nameLabel.setText(_translate("LogDialog", "用户名：", None))
        self.okBtn.setText(_translate("LogDialog", "确认", None))
        self.cancelBtn.setText(_translate("LogDialog", "退出", None))

