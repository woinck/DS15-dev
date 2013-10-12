# -*-coding: UTF-8 -*-
#主界面背景界面
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt
import qrc_resource
class BackWidget(QWidget):
	def __init__(self, parent = None):
		super(BackWidget, self).__init__(parent)
		self.setAutoFillBackground(True)
		self.resize(1024, 768)
		palette = QPalette()
		palette.setBrush(QPalette.Window,
						 QBrush(QPixmap(":mainWindow.jpg").scaled(self.size(), Qt.KeepAspectRatio)))
		self.setPalette(palette)
