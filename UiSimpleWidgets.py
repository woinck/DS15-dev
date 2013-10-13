# -*- coding:UTF-8 -*-
import ui_beginMenu
import ui_widgetssingle
import ui_musicCheck, ui_website
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
import qrc_resource

class BeginMenu(QWidget,ui_beginMenu.Ui_beginMenu):
	def __init__(self, parent = None):
		super(BeginMenu,self).__init__(parent)
#		self.setAutoFillBackground(True)
		self.setupUi(self)
		#pal = self.palette()
		#pal.setBrush(QPalette.Window, QBrush(QPixmap(":mainWindow.jpg")))
		#self.setPalette(pal)
	#	self.setStyleSheet("#frame{background-image:url(:mainWindow.jpg);}"
	#					"QPushButton{border-style:flat;border:0;}")
		pal = self.palette()
		pal.setBrush(QPalette.Window, QBrush(Qt.NoBrush))
		self.setPalette(pal)
		self.singleGameButton.setStyleSheet("#singleGameButton{border-image:url(:singleGameButton0.png);}"
											"#singleGameButton:hover{border-image:url(:singleGameButton1.png);}")
		self.webGameButton.setStyleSheet("#webGameButton{border-image:url(:webGameButton0.png);}"
										 "#webGameButton:hover{border-image:url(:webGameButton1.png);}")
		self.websiteButton.setStyleSheet("#websiteButton{border-image:url(:websiteButton0.png);}"
										 "#websiteButton:hover{border-image:url(:websiteButton1.png);}")
		self.teamButton.setStyleSheet("#teamButton{border-image:url(:teamButton0.png);}"
									  "#teamButton:hover{border-image:url(:teamButton1.png);}")
		self.exitGameButton.setStyleSheet("#exitGameButton{border-image:url(:exitGameButton0.png);}"
									  "#exitGameButton:hover{border-image:url(:exitGameButton1.png);}")
class SingleMenu(QWidget,ui_widgetssingle.Ui_widgetssingle):
	def __init__(self, parent = None):
		super(SingleMenu, self).__init__(parent)
		self.setupUi(self)

		#self.setStyleSheet("#frame{border-image:url(:singleWindow.jpg);}"
		#					"QPushButton{border-style:flat;border:0;}")
		pal = self.palette()
		pal.setBrush(QPalette.Window, QBrush(Qt.NoBrush))
		self.setPalette(pal)
		self.aivsai.setStyleSheet("#aivsai{border-image:url(:aivsaiButton0.png);}"
											"#aivsai:hover{border-image:url(:aivsaiButton1.png);}")
		self.playervsai.setStyleSheet("#playervsai{border-image:url(:playervsaiButton0.png);}"
										 "#playervsai:hover{border-image:url(:playervsaiButton1.png);}")
		self.levelmode.setStyleSheet("#levelmode{border-image:url(:levelmodeButton0.png);}"
										 "#levelmode:hover{border-image:url(:levelmodeButton1.png);}")
		self.replay.setStyleSheet("#replay{border-image:url(:replayButton0.png);}"
									  "#replay:hover{border-image:url(:replayButton1.png);}")
		self.mapedit.setStyleSheet("#mapedit{border-image:url(:mapeditButton0.png);}"
									  "#mapedit:hover{border-image:url(:mapeditButton1.png);}")
		#self.returnpre.setIcon(QIcon(QPixmap(":return0.png")))
		#self.returnpre.setIconSize(self.returnpre.size())
		self.returnpre.setStyleSheet("*{border-image:url(:returnPre0.png);}"
								  "*:hover{border-image:url(:returnPre1.png);}")
class MusicCheck(QWidget, ui_musicCheck.Ui_musicCheck):
	def __init__(self, parent = None):
		super(MusicCheck, self).__init__(parent)
#		self.setAutoFillBackground(True)
		self.setupUi(self)
		pal = self.palette()
		pal.setBrush(QPalette.Window, QBrush(Qt.NoBrush))
		self.setPalette(pal)

#可不可以加外部应用程序链接

class WebWidget(QWidget, ui_website.Ui_webWidget):
	def __init__(self, parent = None):
		super(WebWidget, self).__init__(parent)
		self.setupUi(self)
		pal = self.palette()
		pal.setBrush(QPalette.Window, QBrush(QColor(Qt.white)))
		self.setPalette(pal)
		self.webWidget = QWebView()
		self.webWidget.load(QUrl("http://duishi.eekexie.org"))
		self.verticalLayout.addWidget(self.webWidget)
		self.returnButton.setStyleSheet("*{border-image: url(:return0.png);}"
										"*:hover{border-image: url(:return1.png);}")

class TestWidget(QWidget):
	pass
class LogInWidget(QWidget):
	pass
