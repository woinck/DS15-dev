# -*- coding: utf8 -*-
#
#

from PyQt4 import QtGui, QtCore
import sys
import test_TestMode_rc
from Testbattle_Client import ConnectWithWebsite, ConnectWithLogic, CloseSocket, OpenSocket
import ui_TestWidget
import ui_ResultDialog
import ui_StartDialog
import ui_ScoreDialog
import ui_LogDialog

MAX_LEVEL_NUM = 10
AVAILABLE_LEVEL = [True, True, True, True, True, True, True, True, True, True]

def _tr(string): # decode characters into utf8
	return string.decode("utf8")

class Ui_TestModeWidget(QtGui.QWidget, ui_TestWidget.Ui_TestModeWidget):
	def __init__(self, parent = None):
		super(Ui_TestModeWidget, self).__init__(parent)
		self.setupUi(self)
		self.setAutoFillBackground(True)
		self.data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		# client
		self.resize(1024, 768)
		self.name = "LindexWindy"#for test

	def SetName(self, name):
		self.name = name
	def SetData(self, data):
		self.data = data

	def on_startBtn_pressed(self):
		ShowStartDialog(self.data, self)

	def on_scoreBtn_released(self):
		ShowScoreDialog(self.name, self.data, self)

	def on_exitBtn_released(self):
		self.close()

	def closeEvent(self, event):
		print "close!"#for test
		CloseSocket()
		QtGui.QWidget.closeEvent(self, event)

class Ui_LogDialog(QtGui.QDialog, ui_LogDialog.Ui_LogDialog):
	def __init__(self, parent, name = "", password = ""):
		super(Ui_LogDialog, self).__init__(parent)
		self.setupUi(self)
		self.nameEdit.setText(name)
		self.pwEdit.setText(password)

	def on_okBtn_released(self):
		Ui_LogDialog.name = str(self.nameEdit.text())
		Ui_LogDialog.password = str(self.pwEdit.text())
		self.close()

	def on_cancelBtn_released(self):
		self.close()

	name = ""
	password = ""

def LogIn(parent):
	dialog = Ui_LogDialog(parent)
	dialog.exec_()
	name = Ui_LogDialog.name
	Ui_LogDialog.name = ""
	password = Ui_LogDialog.password
	Ui_LogDialog.password = ""
	return name, password

def ShowTestModeWidget(parent = None):
	if (not OpenSocket()):
		return None
	widget = Ui_TestModeWidget(parent)
	name, password = LogIn(widget)
	print name, password#for test
	if (name=="" or password==""):
		return None
	ok, data = ConnectWithWebsite(name, password)
	print ok, data#for test
	if (ok):
		widget.SetName(name)
		widget.SetData(data)
		widget.show()
		return widget # connect succeed
	else:
		CloseSocket()
		return None

class Ui_ResultDialog(QtGui.QDialog, ui_ResultDialog.Ui_ResultDialog):
	def __init__(self, score, maxScore, parent = None):
		super(Ui_ResultDialog, self).__init__(parent)
		self.setupUi(self)
		self.scoreLabel.setText(str(score))
		self.maxLabel.setText(str(maxScore))

	def on_exitBtn_released(self):
		self.close()

def ShowResultDialog(score, maxScore, parent):
	dialog = Ui_ResultDialog(score, maxScore, parent)
	dialog.exec_()

class Ui_ScoreDialog(QtGui.QDialog, ui_ScoreDialog.Ui_ScoreDialog):
	def __init__(self, name, data, parent = None):
		super(Ui_ScoreDialog, self).__init__(parent)
		self.setupUi(self)
		self.scoreLabels = [self.label1, self.label2,
							self.label3, self.label4,
							self.label5, self.label6,
							self.label7, self.label8,
							self.label9, self.label10]
		for i in range(MAX_LEVEL_NUM):
			self.scoreLabels[i].setText(str(data[i]))
		self.label.setText(_tr("战士 ")+name+_tr(" 的战绩："))

	def on_okBtn_released(self):
		self.close()

def ShowScoreDialog(name, data, parent):
	dialog = Ui_ScoreDialog(name, data, parent)
	dialog.exec_()

class Ui_StartDialog(QtGui.QDialog, ui_StartDialog.Ui_StartDialog):
	def __init__(self, data, parent = None):# name?
		super(Ui_StartDialog, self).__init__(parent)
		self.setupUi(self)
		self.scoreLabels = [self.label1, self.label2,
							self.label3, self.label4,
							self.label5, self.label6,
							self.label7, self.label8,
							self.label9, self.label10]
		self.levelBtns = [self.button1, self.button2,
						  self.button3, self.button4,
						  self.button5, self.button6,
						  self.button7, self.button8,
						  self.button9, self.button10]
		for i in range(MAX_LEVEL_NUM):
			self.scoreLabels[i].setText(str(data[i]))
		self.lvBtnGroup = QtGui.QButtonGroup(self)
		for i in range(MAX_LEVEL_NUM):
			self.lvBtnGroup.addButton(self.levelBtns[i], i+1)
			self.levelBtns[i].setEnabled(AVAILABLE_LEVEL[i])
		self.connect(self.lvBtnGroup, QtCore.SIGNAL("buttonReleased(int)"),
					 self.on_lvBtnGroup_buttonReleased)

		#self.preText = ""
		#self.fileName = ""
		self.aiPathEdit.setText("")
		self.data = data

	def on_lvBtnGroup_buttonReleased(self, lv):
		winner, score = ConnectWithLogic(lv, str(self.aiPathEdit.text()))
		# link to platform
		if (winner!=0):
			self.data[lv-1] = max(self.data[lv-1], score)
		dialog = Ui_ResultDialog(score, self.data[lv-1], self)
		dialog.exec_()

	def on_loadAiBtn_released(self):
		self.aiPathEdit.setText(QtGui.QFileDialog.getOpenFileName(self, _tr("选择AI")))#for test

	def on_okBtn_released(self):
		self.close()

def ShowStartDialog(data, parent):# name?
	dialog = Ui_StartDialog(data, parent)
	dialog.exec_()

if __name__=="__main__":
	app = QtGui.QApplication(sys.argv)
#	testMode = Ui_TestModeWidget()
#	testMode.show()
	testMode = ShowTestModeWidget()
	testMode.showFullScreen()
	app.exec_()
