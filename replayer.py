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

		self.setFixedSize(self.size())
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
			self.buttons[i].setIconSize(self.buttons[i].size())
			self.buttons[i].setStyleSheet("border-radius: 20px")

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
		self.connect(self.pauseButton, SIGNAL("toggled(bool)"), self.on_pauseButton_toggled)#for test
		self.connect(self.playBackwardButton, SIGNAL("toggled(bool)"), self.on_playBackwardButton_toggled)#for test
		self.connect(self.playForwardButton, SIGNAL("toggled(bool)"), self.on_playForwardButton_toggled)#for test
		#self.connect(se
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
				QMessageBox.critical(self, QString.fromUtf8("文件加载错误"), QString.fromUtf8("加载中出现问题,加载失败。"), QMessageBox.Ok, QMessageBox.NoButton)
			else:
				self.fileInfo = fileInfo
				self.repFileName = fname
				#self.reloaded = True
				self.updateUi()

	@pyqtSlot()
	def on_rePlayButton_clicked(self):
		self.checkTimer()
		if self.started:
			self.replayWidget.GoToRound(0, 0)
			if not self.isPaused:
				self.replayWidget.Play()
		else:
			self.started = True
			self.replayWidget.Initialize(basic.Begin_Info(self.fileInfo[0][0],self.fileInfo[0][1]), self.fileInfo[1][0])
			self.replayWidget.UpdateEndData(*self.fileInfo[1][1:])
			for roundInfo in self.fileInfo[2:]:
				self.replayWidget.UpdateBeginData(roundInfo[0])
				self.replayWidget.UpdateEndData(*roundInfo[1:])
			#开始播放
			self.pauseButton.setChecked(False)
			self.replayWidget.GoToRound(0, 0)
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
	def on_pauseButton_toggled(self, pause):
		self.isPaused = pause
		self.checkTimer()
		print "pause trigger!!!:",pause#for test
		if not self.started:
			return
		if pause:
			print "gotor called in pausebutton"#for test
			self.replayWidget.GoToRound(self.replayWidget.nowRound, self.replayWidget.nowStatus)
		else:
			if self.replayWidget.nowStatus:
				try:
					self.replayWidget.GoToRound(self.replayWidget.nowRound + 1, 0)
				except:
					self.emit(SIGNAL("toPause()"))
					print "emit to pause"
				else:
					self.replayWidget.Play()
			else:
				self.replayWidget.Play()
	@pyqtSlot()
	def on_nextStepButton_clicked(self):
		self.checkTimer()
		try:
			self.replayWidget.GoToRound(self.replayWidget.nowRound + 1, 0)
		except:
			return
		print self.isPaused
		if not self.isPaused:
			#self.replayWidget.Play()
			self.pauseButton.setChecked(False)

	@pyqtSlot()
	def on_preStepButton_clicked(self):
		self.checkTimer()
		try:
			self.replayWidget.GoToRound(self.replayWidget.nowRound -1 , 0)
		except:
			return
		if not self.isPaused:
			self.pauseButton.setChecked(False)

	@pyqtSlot()
	def on_playForwardButton_toggled(self, trigger):
		print "playForwardbutton clicked triger:", trigger#for test
		if self.playBackwardButton.isChecked():
			self.playBackwardButton.setChecked(False)
		if trigger:
			self.BorF = 'f'
			self.timer = self.startTimer(500)
		else:
			self.killTimer(self.timer)
			self.timer = None
			if not self.isPaused:
				self.pauseButton.setChecked(False)

	@pyqtSlot()
	def on_playBackwardButton_toggled(self, trigger):
		print "playBackwardButton trigger:", trigger#for test
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
			if not self.isPaused:
				self.pauseButton.setChecked(False)

	def timerEvent(self, event):
		if event.timerId() == self.timer:
			 print "recv timer event!!!"#for test
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
		self.replayWidget.GoToRound(self.replayWidget.nowRound, 1)
		try:
			#print "call go to round on animEnd::",self.replayWidget.nowRound#for test
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

