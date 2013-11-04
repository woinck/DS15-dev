#-*- coding:UTF-8 -*-
#网络对战大厅

import qrc_resource
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from functools import partial

import os,sys

if __name__ == "__main__":
	IMPORT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sys.path.append(IMPORT_PATH)
	import qrc_resource

class WebFightWidget(QWidget, ui_webfightwidget.Ui_Webfightwidget):
	def __init__(self, parent = None):
		super(WebFightWidget, self).__init__(parent)

		self.setupUi(self)
