#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#专门只读取回放文件的回放器

from lib.human.ui_replayer import Ui_Replayer
from lib.human.ui_replaymap import Ui_Replaymap
from lib.human.Humanai_Replay_event import *
from lib.human import info_widget

import sio,basic
import os
#import testdata#for test
REPLAY_FILE_DIR = "."

BUTTONPIC = ["return0", "noSound0", "playSound0", "open0", "pause0", "endPlay0", "rePlay0",
			 "playForward0", "playBackward0", "preStep0", "nextStep0"]

class ReplayMap(QWidget, Ui_Replaymap):
	def __init__(self, scene, parent = None):
		super(ReplayMap, self).__init__(parent)
		self.setupUi(self)
		self.setAutoFillBackground(True)
		palette = QPalette()
		palette.setBrush(QPalette.Window,
								 QBrush(QPixmap(":replay_mapback.png").scaled(self.size(),
																			  Qt.IgnoreAspectRatio,
																			  Qt.SmoothTransformation)))
		self.setPalette(palette)

		self.replayWidget = HumanReplay(scene)
		self.replayLayout.addWidget(self.replayWidget)

class Replayer(QWidget, Ui_Replayer):
	willReturn = pyqtSignal()
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
		#for i in range(len(self.buttons)):
		#	pixmap = QPixmap(":" + BUTTONPIC[i] + ".png")
		#	self.buttons[i].setIcon(QIcon(pixmap))
		#	self.buttons[i].setIconSize(self.buttons[i].size())
		#	self.buttons[i].setStyleSheet("QPushButton{border-radius: 20px;}"
		#									"QPushButton:pressed{border-style:inset;}"
		#									"QPushButton:checked{border-style:inset;}")
		self.returnButton.setStyleSheet("#returnButton{border-image: url(:return0.png);}"
										"#returnButton:hover{border-image: url(:return1.png);}"
										"QToolTip{opacity: 200; border-radius:3;color:rgb(255,255,0);background-color:darkgray;}")
		self.noSoundButton.setStyleSheet("#noSoundButton{border-image: url(:noSound0.png);border:0;}"
		"QToolTip{opacity: 200; border-radius:3;color:rgb(255,255,0);background-color:darkgray;}")
		self.soundButton.setStyleSheet("#soundButton{border-image: url(:playSound0.png);border:0;}"
		"QToolTip{opacity: 200; border-radius:3;color:rgb(255,255,0);background-color:darkgray;}")
										#"*:checked
		self.loadFileButton.setStyleSheet("#loadFileButton{border-image: url(:open0.png);border:0;}"
											"#loadFileButton:hover{border-image:url(:open1.png);border:0;}"
											"QToolTip{opacity: 200; border-radius:3;color:rgb(255,255,0);background-color:darkgray;}")
		self.pauseButton.setStyleSheet("#pauseButton{border-image: url(:pause0.png);border:0;}"
											"#pauseButton:checked{border-image:url(:start1.png);border:0;}"
											"QToolTip{opacity: 200; border-radius:3;color:rgb(255,255,0);background-color:darkgray;}")
		self.endPlayButton.setStyleSheet("#endPlayButton{border-image: url(:endPlay0.png);border:0;}"
										"#endPlayButton:hover{border-image: url(:endPlay1.png);border:0;}"
										"QToolTip{opacity: 200; border-radius:3;color:rgb(255,255,0);background-color:darkgray;}")
		self.rePlayButton.setStyleSheet("#rePlayButton{border-image:url(:rePlay0.png);border:0;}"
										"#rePlayButton:hover{border-image:url(:rePlay1.png);border:0;}"
										"QToolTip{opacity: 200; border-radius:3;color:rgb(255,255,0);background-color:darkgray;}")
		self.playForwardButton.setStyleSheet("#playForwardButton{border-image:url(:playForward0.png);border:0;}"
										"#playForwardButton:checked{border-image:url(:playForward1.png);border:0;}"
										"QToolTip{opacity: 200; border-radius:3;color:rgb(255,255,0);background-color:darkgray;}")
		self.playBackwardButton.setStyleSheet("#playBackwardButton{border-image:url(:playBackward0.png);border:0;}"
										"#playBackwardButton:checked{border-image:url(:playBackward1.png);border:0;}"
										"QToolTip{opacity: 200; border-radius:3;color:rgb(255,255,0);background-color:darkgray;}")
		self.preStepButton.setStyleSheet("#preStepButton{border-image:url(:preStep0.png);border:0;}"
										"#preStepButton:hover{border-image:url(:preStep1.png);border:0;}"
										"QToolTip{opacity: 200; border-radius:3;color:rgb(255,255,0);background-color:darkgray;}")
		self.nextStepButton.setStyleSheet("#nextStepButton{border-image:url(:nextStep0.png); border:0;}"
										"#nextStepButton:hover{border-image:url(:nextStep1.png);border:0;}"
										"QToolTip{opacity: 200; border-radius:3;color:rgb(255,255,0);background-color:darkgray;}")
		self.playSpeedSlider.setStyleSheet("QSlider::groove:horizontal {background-color:darkgrey;margin: 2px 0;}"
											"QSlider::handle:horizontal {background:white;border: 1px solid #5c5c5c;border-radius:3px; width: 18px;}")
		self.roundSlider.setStyleSheet("QSlider::groove:horizontal {background:darkgrey;height:10px;}"
										"QSlider::handle:horizontal {background:#008f8f;height:15px;margin:-3px 0; border-radius:4px;width:15px;}"
										"QSlider::add-page:horizontal {background: darkgrey;}"
										"QSlider::sub-page:horizontal {background: lightblue;}")
		self.roundLabel.setStyleSheet("border-image:url(:roundLabel.png)")
		#信息变量
		self.isPaused = False
		self.started = False
		self.fileInfo = None
		self.repFileName = ""
		self.timer = None
		self.forback_flag = False
		self.scene = QGraphicsScene()
		self.replayWindow = ReplayMap(self.scene)
		self.replayLayout.addWidget(self.replayWindow)
		self.replayWidget = self.replayWindow.replayWidget
		self.infoWidget = info_widget.InfoWidget()
		self.infoLayout.addWidget(self.infoWidget)
		#connect signals
		self.connect(self.replayWidget, SIGNAL("unitSelected"), self.infoWidget.newUnitInfo)
		self.connect(self.replayWidget, SIGNAL("mapSelected"), self.infoWidget.newMapInfo)
		self.connect(self, SIGNAL("toPause()"),  partial(self.pauseButton.setChecked, True), Qt.QueuedConnection)
		self.connect(self.pauseButton, SIGNAL("toggled(bool)"), self.on_pauseButton_toggled)#for test
		self.connect(self.playBackwardButton, SIGNAL("toggled(bool)"), self.on_playBackwardButton_toggled)#for test
		self.connect(self.playForwardButton, SIGNAL("toggled(bool)"), self.on_playForwardButton_toggled)#for test
		self.connect(self.playSpeedSlider, SIGNAL("valueChanged(int)"), self.on_playSpeedSlider_valueChanged)
		self.connect(self.roundSlider, SIGNAL("valueChanged(int)"), self.on_roundSlider_valueChanged)
		#self.connect(se
		self.replayWidget.moveAnimEnd.connect(self.on_animEnd)
		self.replayWidget.HUMAN_REPLAY = 0
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

	def on_threeDReplayBtn_released(self):
		filename = QFileDialog.getOpenFileName(self,
												QString.fromUtf8("加载回放文件"),
												REPLAY_FILE_DIR,
												"3D replay files(*.rep3d)")
		os.chdir("ds15gl_1.0beta")
		if filename and filename!= self.repFileName:
			os.system(str("ds15gl.exe " + filename))
		os.chdir("..")

	@pyqtSlot()
	def on_playSpeedSlider_valueChanged(self, speed):
		self.replayWidget.TIME_PER_GRID = 500 - speed * 5

	@pyqtSlot()
	def on_returnButton_clicked(self):
		self.on_endPlayButton_clicked()
		self.willReturn.emit()

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
				self.infoWidget.setAiInfo(fileInfo[0][2])
				#self.reloaded = True
				self.updateUi()

	@pyqtSlot()
	def on_rePlayButton_clicked(self):
		self.checkTimer()
		if self.started:
			self.replayWidget.GoToRound(0, 0)
			self.synRoundSlider()
			self.roundLabel.setText("Round 0")
			self.infoWidget.setRoundInfo(0)
			if not self.isPaused:
				self.replayWidget.Play()
		else:
			self.started = True
			self.replayWidget.Initialize(basic.Begin_Info(self.fileInfo[0][0],self.fileInfo[0][1]), self.fileInfo[1][0])
			self.replayWidget.UpdateEndData(*self.fileInfo[1][1:])
			for roundInfo in self.fileInfo[2:]:
				self.replayWidget.UpdateBeginData(roundInfo[0])
				self.replayWidget.UpdateEndData(*roundInfo[1:])

			self.roundSlider.setRange(0, len(self.fileInfo) - 2)
			#开始播放
			self.pauseButton.setChecked(False)
			self.replayWidget.GoToRound(0, 0)
			self.synRoundSlider()
			self.roundLabel.setText("Round 0")
			self.infoWidget.setRoundInfo(0)
			self.replayWidget.Play()
			self.updateUi()

	@pyqtSlot()
	def on_endPlayButton_clicked(self):
		self.checkTimer()
		self.replayWidget.reset()
		self.started = False
		self.pauseButton.setChecked(False)
		self.roundSlider.setRange(0, 0)
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
					self.synRoundSlider()
					self.roundLabel.setText("Round %d" %self.replayWidget.nowRound)
					self.infoWidget.setRoundInfo(self.replayWidget.nowRound)
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
			self.synRoundSlider()
			self.roundLabel.setText("Round %d" %self.replayWidget.nowRound)
			self.infoWidget.setRoundInfo(self.replayWidget.nowRound)
		except:
			return
		if not self.isPaused:
			self.replayWidget.Play()
			#self.pauseButton.setChecked(False)

	@pyqtSlot()
	def on_preStepButton_clicked(self):
		self.checkTimer()
		try:
			self.replayWidget.GoToRound(self.replayWidget.nowRound -1 , 0)
			self.synRoundSlider()
			self.roundLabel.setText("Round %d" %self.replayWidget.nowRound)
			self.infoWidget.setRoundInfo(self.replayWidget.nowRound)
		except:
			return
		if not self.isPaused:
			self.replayWidget.Play()
			#self.pauseButton.setChecked(False)

	@pyqtSlot()
	def on_playForwardButton_toggled(self, trigger):
		print "playForwardbutton clicked triger:", trigger#for test
		if self.playBackwardButton.isChecked() and not self.forback_flag:
			self.forback_flag = True
			self.playBackwardButton.setChecked(False)
			self.forback_flag = False
		if trigger:
			self.BorF = 'f'
			self.timer = self.startTimer(200)
		else:
			self.killTimer(self.timer)
			self.timer = None
			print self.isPaused
			if not self.isPaused:
				#self.pauseButton.setChecked(False)
				self.replayWidget.Play()

	@pyqtSlot()
	def on_playBackwardButton_toggled(self, trigger):
		print "playBackwardButton trigger:", trigger#for test
		if self.playForwardButton.isChecked() and not self.forback_flag:
			self.forback_flag = True
			self.playForwardButton.setChecked(False)
			self.forback_flag = False
		if trigger:
			self.BorF = 'b'
			self.timer = self.startTimer(200)
			#			if not self.isPaused:
			#		  #	  self.pauseButton.setChecked(False)
		else:
			self.killTimer(self.timer)
			self.timer = None
			if not self.isPaused:
			#	self.pauseButton.setChecked(False)
				self.replayWidget.Play()

	def on_roundSlider_valueChanged(self, round_):
		if self.started:
			if not round_ == self.replayWidget.nowRound:
				self.replayWidget.GoToRound(round_, 0)
				self.roundLabel.setText("Round %d" %round_)
				if not self.isPaused:
					self.replayWidget.Play()

	def timerEvent(self, event):
		if event.timerId() == self.timer:
			print "recv timer event!!!"#for test
			change = 1 if self.BorF == 'f' else -1
			try:
				self.replayWidget.GoToRound(self.replayWidget.nowRound + change, 0)
				self.synRoundSlider()
				self.roundLabel.setText("Round %d" %self.replayWidget.nowRound)
				self.infoWidget.setRoundInfo(self.replayWidget.nowRound)
			except:
				if self.BorF == 'f':
					self.playForwardButton.setChecked(False)
				else:
					self.playBackwardButton.setChecked(False)
				self.pauseButton.setChecked(True)
		else:
			QWidget.timerEvent(self, event)

	def on_animEnd(self):
		self.replayWidget.GoToRound(self.replayWidget.nowRound, 1)
		try:
			#print "call go to round on animEnd::",self.replayWidget.nowRound#for test
			self.replayWidget.GoToRound(self.replayWidget.nowRound + 1, 0)
			self.synRoundSlider()
			self.roundLabel.setText("Round %d" %self.replayWidget.nowRound)
			self.infoWidget.setRoundInfo(self.replayWidget.nowRound)
		except:
			self.pauseButton.setChecked(True)
		else:
			self.replayWidget.Play()

	def checkTimer(self):
		if self.timer:
			print "check timer!!!"
			if self.BorF == 'b':
				self.playBackwardButton.setChecked(False)
			else:
				self.playForwardButton.setChecked(False)
				
	def synRoundSlider(self):
		print "blabla"
		self.roundSlider.blockSignals(True)
		self.roundSlider.setValue(self.replayWidget.nowRound)
		self.roundSlider.blockSignals(False)
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

