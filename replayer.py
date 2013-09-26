#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#专门只读取回放文件的回放器

from lib.human.ui_replayer import Ui_Replayer
from lib.human.ui_replaymap import Ui_Replaymap
from lib.human.Humanai_Replay_event import *
import sio,basic
#import testdata#for test
REPLAY_FILE_DIR = "."

BUTTONPIC = ["noSound", "playSound", "open", "pause", "endPlay", "rePlay",
			 "playForward0", "playBackward0", "preStep", "nextStep"]

class ReplayMap(QWidget, Ui_Replaymap):
	def __init__(self, scene, parent = None):
		super(ReplayMap, self).__init__(parent)
		self.setupUi(self)
		self.setAutoFillBackground(True)
		palette = QPalette()
		#print "size..............:",self.size().width(),self.size().height()#for test
		palette.setBrush(QPalette.Window,
						 QBrush(QPixmap(":replay_mapback.png").scaled(self.size(),
																	  Qt.IgnoreAspectRatio,
																	  Qt.SmoothTransformation)))
		self.setPalette(palette)

		self.replayWidget = HumanReplay(scene)
		self.replayLayout.addWidget(self.replayWidget)

class Replayer(QWidget, Ui_Replayer):
	def __init__(self, parent = None):
		super(Replayer, self).__init__(parent)
		self.setupUi(self)
		self.setAutoFillBackground(True)
		palette = QPalette()

		palette.setBrush(QPalette.Window,
						 QBrush(QPixmap(":replay_back.png").scaled(self.size(),
																	  Qt.IgnoreAspectRatio,
																	  Qt.SmoothTransformation)))
		self.setPalette(palette)

		self.buttons = [self.noSoundButton, self.soundButton,self.loadFileButton,
						self.pauseButton, self.endPlayButton,
						self.rePlayButton, self.playForwardButton, self.playBackwardButton,
						self.preStepButton, self.nextStepButton]
		for i in range(len(self.buttons)):
			pixmap = QPixmap(":" + BUTTONPIC[i] + ".png")
			self.buttons[i].setIcon(QIcon(pixmap))
		  #  self.buttons[i].setMask(pixmap.createHeuristicMask())
		#信息变量
		self.isPaused = False
		self.started = False
		self.fileInfo = None
		self.repFileName = ""
		self.timer = None
		self.scene = QGraphicsScene()
		self.replayWindow = ReplayMap(self.scene)
		self.replayLayout.addWidget(self.replayWindow)
		self.replayWidget = self.replayWindow.replayWidget

		#connect signals
		self.connect(self, SIGNAL("toPause()"),  partial(self.pauseButton.setChecked, True), Qt.QueuedConnection)
		self.replayWidget.moveAnimEnd.connect(self.on_animEnd)
		self.updateUi()

	def updateUi(self):
		if not self.fileInfo:
			self.rePlayButton.setEnabled(False)
		else:
			self.rePlayButton.setEnabled(True)
		self.loadFileButton.setEnabled(not self.started)
		self.endPlayButton.setEnabled(self.started)
		self.pauseButton.setEnabled(self.started)
		self.nextStepButton.setEnabled(self.started)
		self.preStepButton.setEnabled(self.started)
		self.playForwardButton.setEnabled(self.started)
		self.playBackwardButton.setEnabled(self.started)

	@pyqtSlot()
	def on_loadFileButton_clicked(self):
		fname = QFileDialog.getOpenFileName(self, QString.fromUtf8("加载回放文件"), REPLAY_FILE_DIR, "replay files(*.rep)")
   #	 print fname
		if fname and fname!= self.repFileName:
			try:
				fileInfo = sio._ReadFile(fname)
			except:
				QMessageBox.critical(QString.fromUtf8("文件加载错误"), QString.fromUtf8("加载中出现问题,加载失败。"), QMessageBox.Ok, QMessageBox.NoButton)
			else:
#				print "fileinfo is ", fileInfo#fortest
				self.fileInfo = fileInfo
				self.repFileName = fname
				#self.reloaded = True
				self.updateUi()

	@pyqtSlot()
	def on_rePlayButton_clicked(self):
		self.checkTimer()
		if self.started:
			self.replayWidget.GoToRound(0, 0)
		else:
			self.started = True
			#self.fileInfo.insert(0, basic.Begin_Info(testdata.maps, testdata.units0))#for test
			self.replayWidget.Initialize(basic.Begin_Info(self.fileInfo[0][0],self.fileInfo[0][1]), self.fileInfo[1][0])
			self.replayWidget.UpdateEndData(*self.fileInfo[1][1:])
			for roundInfo in self.fileInfo[2:]:
				self.replayWidget.UpdateBeginData(roundInfo[0])
				self.replayWidget.UpdateEndData(*roundInfo[1:])
			#开始播放
			self.pauseButton.setChecked(False)
			self.replayWidget.Play()
			self.updateUi()

	@pyqtSlot()
	def on_endPlayButton_clicked(self):
		self.checkTimer()
		self.replayWidget.reset()
		self.started = False
		self.pauseButton.setChecked(False)
		self.updateUi()

	@pyqtSlot()
	def on_pauseButton_triggered(self, pause):
		self.checkTimer()
		self.isPaused = pause
		if not self.started:
			return
		if pause:
			self.replayWidget.GoToRound(self.replayWidget.nowRound, self.replayWidget.nowStatus)
		else:
			if self.replayWidget.nowStatus:
				try:
					self.replayWidget.GoToRound(self.replayWidget.nowRound + 1, 0)
				except:
					self.emit(SIGNAL("toPause()"))
				else:
					self.replayWidget.Play()

	@pyqtSlot()
	def on_nextStepButton_clicked(self):
		self.checkTimer()
		try:
			self.replayWidget.GoToRound(self.replayWidget.nowRound + 1, 0)
		except:
			return
		if not self.isPaused:
			self.replayWidget.Play()

	@pyqtSlot()
	def on_preStepButton_clicked(self):
		self.checkTimer()
		try:
			self.replayWidget.GoToRound(self.replayWidget.nowRound -1 , 0)
		except:
			return
		if not self.isPaused:
			self.replayWidget.Play()

	@pyqtSlot()
	def on_playForwardButton_triggered(self, trigger):
		if self.playBackButton.isChecked():
			self.playBackButton.setChecked(False)
		if trigger:
			self.BorF = 'f'
			self.timer = self.startTimer(500)
		else:
			self.killTimer(self.timer)
			self.timer = None

	@pyqtSlot()
	def on_playBackwardButton_triggered(self, trigger):
		if self.playForwardButton.isChecked():
			self.playForwardButton.setChecked(False)
		if trigger:
			self.BorF = 'b'
			self.timer = self.startTimer(200)
			#			if not self.isPaused:
			#		  #	  self.pauseButton.setChecked(False)
		else:
			self.killTimer(self.timer)
			self.timer = None

	def timerEvent(self, event):
		if event.timerId() == self.timer:
			 change = 1 if self.BorF == 'f' else -1
			 try:
				 self.replayWidget.GoToRound(self.replayWidget.nowRound + change, 0)
			 except:
				 if self.BorF == 'f':
					 self.playForwardButton.setChecked(False)
				 else:
					 self.playBackwardButton.setChecked(False)
		else:
			QWidget.timerEvent(self, event)

	def on_animEnd(self):
		try:
			print "call go to round on animEnd::",self.replayWidget.nowRound
			self.replayWidget.GoToRound(self.replayWidget.nowRound + 1, 0)
		except:
			self.pauseButton.setChecked(True)
		else:
			self.replayWidget.Play()

	def checkTimer(self):
		if self.timer:
			if self.BorF == 'b':
				self.playBackwardButton.setChecked(False)
			else:
				self.playForwardButton.setChecked(False)
#test
if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	form = Replayer()
	form.show()
 #   form.show()
	try:
		app.exec_()
	except KeyboardInterrupt:
		form.close()
		app.quit()
		print "abc"
