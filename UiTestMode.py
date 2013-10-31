# -*- coding: utf8 -*-
#
#

from PyQt4 import QtGui, QtCore
from ui_buttonwithdisplay import *
import sys
import test_TestMode_rc
from Testbattle_Client import ConnectWithWebsite, ConnectWithLogic, CloseSocket, OpenSocket, ConnectionError
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
		self.startWidget = Ui_StartDialog(self.data, self)
		self.startWidget.setParent(self.startFrame)
		self.connect(self.logOutBtn, QtCore.SIGNAL("clicked()"), self.on_logOutBtn_pressed)

	def SetName(self, name):
		self.name = name
	def SetData(self, data):
		print len(data)
		for i in range(MAX_LEVEL_NUM):
			self.data[i] = int(data[i])
		self.startWidget.initialize(self.data)

	def on_scoreBtn_released(self):
		ShowScoreDialog(self.name, self.data, self)
	
	def on_logOutBtn_pressed(self):
		CloseSocket()
		self.emit(QtCore.SIGNAL("logOut()"))

	def on_loadAiBtn_released(self):
		self.aiPathEdit.setText(QtGui.QFileDialog.getOpenFileName(self, _tr("选择AI"),".","Ai files(*.exe)"))#for test


class Ui_ResultDialog(QtGui.QDialog, ui_ResultDialog.Ui_ResultDialog):
	def __init__(self, winner, score, maxScore, parent = None):
		super(Ui_ResultDialog, self).__init__(parent)
		self.setupUi(self)
		if (winner!=0):
			self.loseLabel.setWindowOpacity(0)
		self.scoreLabel.setText(str(score))
		self.maxLabel.setText(str(maxScore))

	def on_exitBtn_released(self):
		self.close()

def ShowResultDialog(winner, score, maxScore, parent): # winner?
	dialog = Ui_ResultDialog(winner, score, maxScore, parent)
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
		self.label.setText(_tr("战士 ")+_tr(name)+_tr(" 的战绩："))

	def on_okBtn_released(self):
		self.close()

def ShowScoreDialog(name, data, parent):
	dialog = Ui_ScoreDialog(name, data, parent)
	dialog.exec_()

class Ui_StartDialog(QtGui.QWidget, ui_StartDialog.Ui_StartDialog):
	def __init__(self, data, parent):# name?
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
			self.scoreLabels[i].setText(_tr("最高分")+str(data[i]))
			self.scoreLabels[i].hide()
		self.lvBtnGroup = QtGui.QButtonGroup(self)
		for i in range(MAX_LEVEL_NUM):
			self.lvBtnGroup.addButton(self.levelBtns[i], i+1)
			self.levelBtns[i].setEnabled(AVAILABLE_LEVEL[i])
			self.levelBtns[i].StartDisplay.connect(self.scoreLabels[i].show)
			self.levelBtns[i].StopDisplay.connect(self.scoreLabels[i].hide)
		self.connect(self.lvBtnGroup, QtCore.SIGNAL("buttonReleased(int)"),
					 self.on_lvBtnGroup_buttonReleased)

		#self.preText = ""
		#self.fileName = ""
		self.aiPathEdit = self.parent().aiPathEdit
		self.data = data
		self.logicThread = None

	def initialize(self, data):
		print "data", data#for data
		for i in range(MAX_LEVEL_NUM):
			self.scoreLabels[i].setText(_tr("最高分")+str(data[i]))
			self.scoreLabels[i].hide()
		for i in range(MAX_LEVEL_NUM):
			self.lvBtnGroup.addButton(self.levelBtns[i], i+1)
			self.levelBtns[i].setEnabled(AVAILABLE_LEVEL[i])

		#self.preText = ""
		#self.fileName = ""
		self.data = data
		self.logicThread = None

	def on_lvBtnGroup_buttonReleased(self, lv):
		print self.data#for test
		if (str(self.aiPathEdit.text())==""):
			QtGui.QMessageBox.warning(self, "Warning", _tr("没有选择AI。"))
		else:
			self.logicThread = UiD_LogicThread(lv, str(self.aiPathEdit.text()), self)
			self.logicThread.LogicResult.connect(self._showResult)
			self.connect(self.logicThread, QtCore.SIGNAL("connectionError()"), self.on_connectionError)
			self.connect(self.logicThread, QtCore.SIGNAL("finished()"), self.logicThread, QtCore.SLOT("deleteLater()"))
			for i in range(MAX_LEVEL_NUM):
				self.levelBtns[i].setEnabled(False)
			self.logicThread.start()
			# link to platform


	def on_connectionError(self):
		QMessageBox.warning(self, _tr("连接错误"), _tr("不能连接到平台"), QMessageBox.Ok, QMessageBox.NoButton)
		for i in range(MAX_LEVEL_NUM):
			self.levelBtns[i].setEnabled(True)

	def _showResult(self, lv, winner, score):
		if (winner!=0):
			self.data[lv-1] = max(self.data[lv-1], score)
			self.scoreLabels[lv-1].setText(_tr("最高分")+str(self.data[lv-1]))
		if (self.isVisible()):
		   dialog = Ui_ResultDialog(winner, score, self.data[lv-1], self) # winner?
		   dialog.exec_()
		for i in range(MAX_LEVEL_NUM):
			self.levelBtns[i].setEnabled(True)

#	def on_loadAiBtn_released(self):
#		self.aiPathEdit.setText(QtGui.QFileDialog.getOpenFileName(self, _tr("选择AI")))#for test

#	def on_okBtn_released(self):
#		self.close()

#def ShowStartDialog(data, parent):# name?
#	dialog = Ui_StartDialog(data, parent)
#	dialog.exec_()


#------------------------------------------------------#

class UiD_LogicThread(QtCore.QThread):
	LogicResult = QtCore.pyqtSignal(int, int, int)
	def __init__(self, lv, aiPath, parent):
		QtCore.QThread.__init__(self, parent)
		self.lv = lv
		self.aiPath = aiPath
	def run(self):
		print "nimei"#for test
		print self.lv, self.aiPath#for test
		try:
			winner, score = ConnectWithLogic(self.lv, self.aiPath)
		except ConnectionError:
			self.emit(QtCore.SIGNAL("connectionError()"))
		else:
			self.LogicResult.emit(self.lv, winner, score)
	

if __name__=="__main__":
	app = QtGui.QApplication(sys.argv)
	print "helloooooo"#for test
	testMode = ShowTestModeWidget()
	print "helloooooo"#for test
	testMode.showFullScreen()
	app.exec_()
