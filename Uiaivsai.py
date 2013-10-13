#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#嵌入主界面的简单ai对战界面

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import socket, sio, os
import ui_aivsai
import qrc_resource
AI_FILE_DIR = ""#ai目录路径
MAP_FILE_DIR = ""#map目录路径
Score = (0, 0)
class AiThread(QThread):
	def __init__(self, map, ai1, ai2, parent = None):
		super(AiThread, self).__init__(parent)
		self.map = map
		self.ai1 = ai1
		self.ai2 = ai2
		self.Stopped = False
		self.lock = QMutex()

	def run(self):
		#先用QProcess打开平台程序
		self.platProcess = sio.Prog_Run(os.getcwd() + sio.SERV_FILE_NAME)
		
		self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			self.conn.connect((sio.HOST,sio.UI_PORT))
		except:
			self.emit(SIGNAL("connectError()"))
		else:
			sio._sends(self.conn,(sio.AI_VS_AI, self.map ,[self.ai1, self.ai2],[False,False]))

			mapInfo,baseInfo,aiInfo = sio._recvs(self.conn)
			try:
				rbInfo = sio._recvs(self.conn)
			except:
				self.stop()
			try:
				rCommand,reInfo = sio._recvs(self.conn)
			except:
				self.stop()
			self.emit(SIGNAL("round()"))

			while not reInfo.over and not self.isStopped():
				try:
					rbInfo = sio._recvs(self.conn)
				except:
					self.stop()
				try:
					rCommand,reInfo = sio._recvs(self.conn)
				except:
					self.stop()
					pass
				self.emit(SIGNAL("round()"))
			if not self.isStopped():
				global Score
				Score = reInfo.score
				winner = sio._recvs(self.conn)
				self.emit(SIGNAL("gameEnd"),winner)
			if not self.isStopped():
				sio._sends(self.conn, True)
				self.sleep(2)
		finally:
			self.platProcess.kill()
			self.conn.close()

	@pyqtSlot()
	def on_shut(self):
		self.conn.shutdown(socket.SHUT_RDWR)
		self.conn.close()
		self.platProcess.kill()
		self.exit(0)
	def stop(self):
		try:
			self.lock.lock()
			self.Stopped = True
		finally:
			self.lock.unlock()
	def isStopped(self):
		try:
			self.lock.lock()
			return self.Stopped
		finally:
			self.lock.unlock()

class AivsAi(QWidget, ui_aivsai.Ui_AIvsAI):
	willReturn = pyqtSignal()
	def __init__(self, parent = None):
		super(AivsAi, self).__init__(parent)
		self.setupUi(self)
		
		self.roundLCD.display(0)
		self.setStyleSheet("#frame{border-image: url(:singleWindow.png);}"
							"QPushButton{border-style:flat;border:0;}")
		#self.returnButton.setIcon(QIcon(QPixmap(":return0.png")))
		#self.returnButton.setIconSize(self.returnButton.size())
		#self.startButton.setIcon(QIcon(QPixmap(":start0.png")))
		#self.startButton.setIconSize(self.startButton.size())
		#self.mapButton.setIcon(QIcon(QPixmap(":openMap0.png")))
		#self.mapButton.setIconSize(self.mapButton.size())
		#self.AiButton1.setIcon(QIcon(QPixmap(":openAI0.png")))
		#self.AiButton1.setIconSize(self.AiButton1.size())
		#self.AiButton2.setIcon(QIcon(QPixmap(":openAI1.png")))
		#self.AiButton2.setIconSize(self.AiButton2.size())
		self.returnButton.setStyleSheet("*{border-image: url(:return0.png);}"
										"*:hover{border-image: url(:return1.png);}")
		self.startButton.setStyleSheet("*{border-image: url(:start0.png);}"
										"*:hover{border-image: url(:start1.png);}")
		self.mapButton.setStyleSheet("*{border-image: url(:openMap0.png);}"
										"*:hover{border-image: url(:openMap1.png);}")
		self.AiButton1.setStyleSheet("*{border-image: url(:openAI0.png);}"
										"*:hover{border-image: url(:openAI0.png);}")
		self.AiButton2.setStyleSheet("*{border-image: url(:openAI1.png);}"
										"*:hover{border-image: url(:openAI1.png);}")	
		self.exitButton.setStyleSheet("*{border-image: url(:exit0.png);}"
										"*:hover{border-image: url(:exit1.png);}")

	@pyqtSlot()
	def on_startButton_clicked(self):
		self.round = 0
		self.roundLCD.display(0)
		self.ai1 = self.AiCombo1.currentText()
		self.ai2 = self.AiCombo2.currentText()
		self.map = self.mapCombo.currentText()
		if self.ai1 and self.ai2 and self.map:
			self.startGame()
		else:
			QMessageBox.warning(self, QString.fromUtf8("错误"),QString.fromUtf8("请载入ai与地图"),QMessageBox.Ok, QMessageBox.NoButton)
	@pyqtSlot()					
	def on_AiButton1_clicked(self):
		dir = AI_FILE_DIR if AI_FILE_DIR else "."
		newAiName = unicode(QFileDialog.getOpenFileName(self, QString.fromUtf8("载入ai"),
														dir, "aifile(*.py)"))
		if newAiName:
			for i in range(self.AiCombo1.count()):
				if newAiName == self.AiCombo1.itemText(i):
					self.AiCombo1.setCurrentIndex(i)
					return
			self.AiCombo1.addItem(newAiName)
			self.AiCombo1.setCurrentIndex(self.AiCombo1.count() - 1)
	@pyqtSlot()
	def on_AiButton2_clicked(self):
		dir = AI_FILE_DIR if AI_FILE_DIR else "."
		newAiName = unicode(QFileDialog.getOpenFileName(self,QString.fromUtf8("载入ai"),
														dir, "aifile(*.py)"))
		if newAiName:
			for i in range(self.AiCombo2.count()):
				if newAiName == self.AiCombo2.itemText(i):
					self.AiCombo2.setCurrentIndex(i)
					return
			self.AiCombo2.addItem(newAiName)
			self.AiCombo2.setCurrentIndex(self.AiCombo2.count() - 1)
	@pyqtSlot()
	def on_mapButton_clicked(self):
		dir = MAP_FILE_DIR if MAP_FILE_DIR else "."
		newMapName = unicode(QFileDialog.getOpenFileName(self, QString.fromUtf8("载入地图"),
														dir, "mapfile(*.map)"))
		if newMapName:
			for i in range(self.mapCombo.count()):
				if newMapName == self.mapCombo.itemText(i):
					self.mapCombo.setCurrentIndex(i)
					return
			self.mapCombo.addItem(newMapName)
			self.mapCombo.setCurrentIndex(self.mapCombo.count() - 1)

	@pyqtSlot()
	def on_returnButton_clicked(self):
		self.emit(SIGNAL("toShut()"))
		self.willReturn.emit()
		self.startButton.setEnabled(True)

	@pyqtSlot()
	def on_exitButton_clicked(self):
		self.emit(SIGNAL("toShut()"))
		self.startButton.setEnabled(True)

	def roundDisplay(self):
		self.round += 1
		self.roundLCD.display(self.round)


	def endGame(self, winner):
		QMessageBox.information(self, QString.fromUtf8("游戏结束"), QString.fromUtf8("ai %s 胜利\n 分数:%d : %d " %(winner, Score[0], Score[1] )))
		self.startButton.setEnabled(True)


	def connectError(self):
		QMessageBox.critical(self, QString.fromUtf8("连接错误"),QString.fromUtf8("平台连接错误"),
							 QMessageBox.Ok, QMessageBox.NoButton)
		self.startButton.setEnabled(True)

	def startGame(self):
		self.startButton.setEnabled(False)
		self.thread = AiThread(unicode(self.map), unicode(self.ai1), unicode(self.ai2), self)
		self.connect(self, SIGNAL("toShut()"), self.thread, SLOT("on_shut()"))
		self.connect(self.thread, SIGNAL("finished()"), self.thread, SLOT("deleteLater()"))
		self.connect(self.thread, SIGNAL("gameEnd"), self.endGame)
		self.connect(self.thread, SIGNAL("connectError()"), self.connectError)
		self.connect(self.thread, SIGNAL("round()"), self.roundDisplay)
		self.thread.start()


#for test
if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	form = AivsAi()
	form.show()
	app.exec_()
