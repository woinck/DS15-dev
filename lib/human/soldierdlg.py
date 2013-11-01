#-*- coding:UTF-8 -*-
#选择士兵dialog

from PyQt4.QtGui import QDialog, QPixmap, QPushButton
from PyQt4.QtCore import SIGNAL
import ui_soldierdlg
import qrc_resource

class GetSoldierTypeDlg(QDialog, ui_soldierdlg.Ui_GetSoldierTypeDialog):
	def __init__(self, number, soldier_ids ,parent = None):
		super(GetSoldierTypeDlg, self).__init__(parent)
		self.setupUi(self)
		
		self.buttons = [self.soldierButton0, self.soldierButton1, self.soldierButton2,
						self.soldierButton3, self.soldierButton4, self.soldierButton5]
		for button in self.buttons:
			button.setCheckable(True)
			pixmap = QPixmap(":soldier%d.png" %(self.buttons.index(button)))
			button.setIcon(QIcon(pixmap))
			button.setIconSize(button.size())
			self.connect(button, SIGNAL("toggled(bool)"), self.updateUi,Qt.QueuedConnection)
		self.number = number
		self.soldier_ids = soldier_ids
		self.choice = []
		self.setWindowTitle(QString.fromUtf8("选择士兵"))

	def updateUi(self, checked):
		button = self.sender()
		if isinstance(button, QPushButton):
			if checked:
				self.choice.append(self.buttons.index(button))
				if len(self.choice) > self.number:
					button_to_uncheck = self.buttons[self.choice[0]]
					#有更好的方法没
					button_to_uncheck.setChecked(False)
					self.choice.pop(0)
			else:
				if int(self.buttons.index(button)) in self.choice:
					self.choice.pop(self.choice.index(self.buttons.index(button) + 6))
					
		self.emit(SIGNAL("soldierChoosed"), self.soldier_ids, self.choice)
		
#test
if __name__ == "__main__":
	import sys
	from PyQt4.QtCore import *
	from PyQt4.QtGui import *
	app = QApplication(sys.argv)
	form = GetSoldierTypeDlg(2, [1, 2])
	form.exec_()
