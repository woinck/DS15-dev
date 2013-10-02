#-*- coding: UTF-8 -*-

import ui_helpdlg
import qrc_resource
from PyQt4.QtGui import QDialog,QIcon,QPixmap
class HelpDlg(QDialog, ui_helpdlg.Ui_Dialog):
	def __init__(self, parent):
		super(HelpDlg, self).__init__(parent)
		self.setupUi(self)
		
		self.setWindowIcon(QIcon(QPixmap(":help1.png")))

		
		