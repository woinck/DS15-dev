# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'part_loginwidget.ui'
#
# Created: Thu Oct 31 03:56:50 2013
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

class Ui_loginWidget(object):
    def setupUi(self, loginWidget):
        loginWidget.setObjectName(_fromUtf8("loginWidget"))
        loginWidget.resize(1024, 768)
        self.frame = QtGui.QFrame(loginWidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1031, 771))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.backButton = QtGui.QPushButton(self.frame)
        self.backButton.setGeometry(QtCore.QRect(30, 20, 50, 50))
        self.backButton.setText(_fromUtf8(""))
        self.backButton.setObjectName(_fromUtf8("backButton"))
        self.userNameEdit = QtGui.QLineEdit(self.frame)
        self.userNameEdit.setGeometry(QtCore.QRect(430, 340, 131, 31))
        self.userNameEdit.setObjectName(_fromUtf8("userNameEdit"))
        self.passwordEdit = QtGui.QLineEdit(self.frame)
        self.passwordEdit.setGeometry(QtCore.QRect(430, 410, 131, 31))
        self.passwordEdit.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        self.passwordEdit.setObjectName(_fromUtf8("passwordEdit"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(320, 340, 100, 40))
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
        font.setFamily(_fromUtf8("Adobe Arabic"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(320, 410, 91, 41))
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
        self.label_2.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Adobe Arabic"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.loginButton = QtGui.QPushButton(self.frame)
        self.loginButton.setGeometry(QtCore.QRect(440, 500, 80, 30))
        self.loginButton.setObjectName(_fromUtf8("loginButton"))

        self.retranslateUi(loginWidget)
        QtCore.QMetaObject.connectSlotsByName(loginWidget)

    def retranslateUi(self, loginWidget):
        loginWidget.setWindowTitle(_translate("loginWidget", "Form", None))
        self.label.setText(_translate("loginWidget", "用户名", None))
        self.label_2.setText(_translate("loginWidget", "密码", None))
        self.loginButton.setText(_translate("loginWidget", "登陆", None))

