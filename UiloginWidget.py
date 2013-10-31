#-*- coding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import qrc_resource
import ui_loginwidget
from Testbattle_Client import *

class LoginWidget(QWidget, ui_loginwidget.Ui_loginWidget):
	loginS = pyqtSignal()
	def __init__(self, widget, parent = None):
		super(LoginWidget, self).__init__(parent)
		
		self.setupUi(self)
		self.widget = widget
		self.setStyleSheet("#frame{border-image:url(:login_back.png);}"
							"#backButton{border-image:url(:return0.png);}"
							"#backButton:hover{border-image:url(:return1.png);}")
		self.userNameEdit.setText(QString.fromUtf8("这里是肥脸猪"))
		self.passwordEdit.setText("feilianfeilian")
		self.connect(self.loginButton, SIGNAL("clicked()"), self.testLogin)
		#QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))
		self.passwordEdit.setEchoMode(QLineEdit.Password)
		
	def testLogin(self):
		if not OpenSocket():
			QMessageBox.warning(self, QString.fromUtf8("连接错误"), QString.fromUtf8("平台连接错误，请反馈bug，谢谢。"),
						QMessageBox.Ok, QMessageBox.NoButton)
			return
		name = unicode(self.userNameEdit.text().toUtf8())#.encode('utf-8')
		pwd = unicode(self.passwordEdit.text().toUtf8())
		
	#	gbk = QTextCodec.codecForName("GB18030")
	#	name = gbk.toUnicode(gbk.fromUnicode(name))
		if name == "" or pwd == "":
			return
		ok, data = ConnectWithWebsite(name, pwd)
		if ok:
			self.widget.SetName(name)
			self.widget.SetData(data)
			self.loginS.emit()
		else:
			CloseSocket()
			QMessageBox.warning(self, QString.fromUtf8("连接错误"), QString.fromUtf8("检查您的账户与密码，如果没有错可能是未连接到网站，请检查网络连接"),
						QMessageBox.Ok, QMessageBox.NoButton)

		