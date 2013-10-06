#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#人机对战界面

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import lib.human.ui_humanvsai
from lib.human.Humanai_Replay_event import HumanReplay
from lib.human.info_widget import *
import basic, sio, select, os, socket, time, subprocess
from lib.human.herotypedlg import GetHeroTypeDlg
from lib.human.helpDlg import HelpDlg
from functools import partial
#from AI_debugger import AiThread

try:
	_frUtf = QString.fromUtf8
except AttributeError:
	_frUtf = lambda s:s
WAIT_TIME = 5000
AI_DIR = "." #默认ai目录路径
MAP_DIR = "."
Already_Wait = False
Able_To_Comm = False
WaitForCommand=QWaitCondition()
WaitForHero=QWaitCondition()
WaitForAni=QWaitCondition()
WaitForIni=QWaitCondition()
WaitForReplay=QWaitCondition()
mutex = QMutex()
#tmp
#for debug
DEFAULT_MAP = os.getcwd() + "//new_map.map"
DEFAULT_AI = os.getcwd() + "//sclientai.py"

#for test
#file_log = subprocess.Popen("python blabla.py", stdin = subprocess.PIPE)
class ConnectionError(Exception):
	def __init__(self, value = ""):
		super(ConnectionError, self).__init__()
		self.value = value
class AiThread(QThread):
	def __init__(self,parent=None):# lock, parent = None):
		super(AiThread, self).__init__(parent)

		self.mutex = QMutex()
		self.closed = False#close标识以便强制关闭线程
		self.replay_mode = False
	#每次开始游戏时，用ai路径和地图路径调用initialize以开始一个新的游戏
	def initialize(self, gameAIPath, gameMapPath):
		if not sio.DEBUG_MODE:
			self.serverProg = sio.Prog_Run(os.getcwd() + sio.SERV_FILE_NAME)
		self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			self.conn.connect((sio.HOST,sio.UI_PORT))
		except:
			self.conn.close()
			raise ConnectionError()
		else:
			sio._sends(self.conn,(sio.PLAYER_VS_AI, unicode(gameMapPath),(unicode(gameAIPath),None)))
	def isStopped(self):
		try:
			self.mutex.lock()
			return self.closed
		finally:
			self.mutex.unlock()
	def stop(self):
		try:
			self.mutex.lock()
			self.closed = True
		finally:
			self.mutex.unlock()
	@pyqtSlot()
	def on_shut(self):
		self.conn.shutdown(socket.SHUT_RDWR)
		self.serverProg.kill()
		self.exit(0)
		
	def run(self):
		temp = sio._recvs(self.conn)#add base info
		self.emit(SIGNAL("tmpRecv()"))

		mapInfo,baseInfo,aiInfo = sio._recvs(self.conn)#add base info
		frInfo = sio._recvs(self.conn)
		self.emit(SIGNAL("firstRecv"),mapInfo, frInfo, aiInfo, baseInfo)
		try:
			rCommand, reInfo = sio._recvs(self.conn)
		except sio.ConnException:
			self.stop()
			pass
		self.emit(SIGNAL("reRecv"), rCommand, reInfo)
		while not reInfo.over and not self.isStopped():
			try:
				rbInfo = sio._recvs(self.conn)
			except sio.ConnException:
				#self.quit()
				self.stop()
				pass
				#raise sio.ConnException
			if self.isStopped():
				break
			self.emit(SIGNAL("rbRecv"),rbInfo)
			try:
				rCommand,reInfo = sio._recvs(self.conn)
			except sio.ConnException:
				#self.quit()
				self.stop()
				pass
				#raise sio.ConnException
			
			if self.isStopped():
				break

			self.emit(SIGNAL("reRecv"),rCommand, reInfo)
		if not self.isStopped():
			winner = sio._recvs(self.conn)
			self.emit(SIGNAL("gameWinner"),winner)
	#	是否存储回放文件
		if not self.isStopped():
			global WaitForReplay

			self.mutex.lock()
			WaitForReplay.wait(self.mutex)

			sio._sends(self.conn, self.replay_mode)


		self.conn.close()

class Ui_Player(QThread):
	def __init__(self,num, func, parent):
		super(Ui_Player, self).__init__(parent)
		self.name = 'Thread-Player'
		self.num = num
		self.command = None
		self.lock = QReadWriteLock()
		self.stopped = False
		self.func = func
		self.cmdNum = 0
		self.flag = 1
		self.result = ("Player", (6,6))
	@pyqtSlot()
	def on_shut(self):
		self.conn.shutdown(socket.SHUT_RDWR)
		self.exit(0)
	def initialize(self):
		self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		for i in range(5):
			try:
				self.conn.connect((sio.HOST,sio.AI_PORT))
			except:
				pass
			else:
				break
		else:
			self.conn.close()
			raise ConnectionError("ai port")
	def GetHeroType(self,mapInfo):
			self.emit(SIGNAL("getHeroType()"))
			global WaitForHero
			self.lock.lockForRead()
			WaitForHero.wait(self.lock)
			self.lock.unlock()
			return self.result

	def AI(self,rBeginInfo):
		self.command=basic.Command()
		global mutex, Already_Wait
		global WaitForCommand,WaitForAni,WaitForIni
		self.lock.lockForRead()
		global Able_To_Comm
		flag1 = False
		#检查able_TO_comm全局变量,如果主线程已经准备好所有只待开始做命令则直接开始
		try:
			mutex.lock()

			if Able_To_Comm:
				flag1 = True
				Able_To_Comm = False
		finally:
			mutex.unlock()
		if not flag1:#flag1 = AbleToComm
			try:
				self.lock.lockForRead()
				if self.cmdNum or not self.flag:
					try:
						mutex.lock()
						Already_Wait = True
					finally:
						mutex.unlock()
					WaitForAni.wait(self.lock)
				else:
					self.emit(SIGNAL("firstCmd()"))
					#检查player是否是第一个开始做命令的,若是则要等待initialize(需要加强双向等待)
					WaitForIni.wait(self.lock)
			finally:
				self.lock.unlock()

		self.func()

		WaitForCommand.wait(self.lock)
		self.lock.unlock()
		return self.command

	def run(self):
		mapInfo,base = sio._recvs(self.conn)
	#	mapInfo = mapReverse(mapInfo)#debugging
		self.emit(SIGNAL("mapRecv"), mapInfo, base)
		result = self.GetHeroType(mapInfo)
		sio._sends(self.conn, (result[0],result[1][0]))
		while True and not self.isStopped():
			try:
				rBeginInfo = sio._recvs(self.conn)
			except sio.ConnException:
				#self.quit()
				self.stop()
				pass
				#raise sio.ConnException
			if self.isStopped():
				break
			if rBeginInfo != '|':
				try:	
					sio._sends(self.conn,self.AI(rBeginInfo))
					self.cmdNum += 1
				except sio.ConnException:
					self.stop()
					pass
			else:
				break
		self.conn.close()

	def stop(self):
		try:
			self.lock.lockForWrite()
			self.stopped = True
		finally:
			self.lock.unlock()
	def isStopped(self):
		try:
			self.lock.lockForRead()
			return self.stopped
		finally:
			self.lock.unlock()

ButtonPics = ["start0", "return0", "openMap0", "openAI0", "help0"]
class HumanvsAi(QWidget, lib.human.ui_humanvsai.Ui_HumanvsAi):
	willReturn = pyqtSignal()
	def __init__(self, parent = None):
		super(HumanvsAi, self).__init__(parent)
		self.setupUi(self)

		self.setFixedSize(self.size())
		palette = self.palette()
		palette.setBrush(QPalette.Window,
						QBrush(QPixmap(":humanai_back.png").scaled(self.size(),
																	Qt.IgnoreAspectRatio,
																	Qt.SmoothTransformation)))

		self.setPalette(palette)
		#self.setStyleSheet("#backFrame{border-image:url(:humanai_back.png);}")
		#画button图片
		buttons = [self.startButton, self.returnButton, self.mapButton,
				self.aiButton, self.helpButton]
		for i in range(len(buttons)):
			buttons[i].setIcon(QIcon(QPixmap(":" + ButtonPics[i] + ".png")))
			buttons[i].setIconSize(buttons[i].size())
			buttons[i].setStyleSheet("border-radius: 30px;")
		self.setCursor(QCursor(QPixmap(":normal_cursor.png").scaled(30,30),0,0))
		self.aiPath = ""
		self.mapPath = ""
		self.started = False
		self.nowRound = 0
		self.startButton.setEnabled(False)
		self.Able_To_Play = True
		self.winner = None
		self.lastRound = -1
		#widget
		self.scene = QGraphicsScene()
		self.replayWindow = HumanReplay(self.scene)

		self.getComm = self.replayWindow.GetCommand

		self.infoWidget = InfoWidget()
		
		#self.helpdlg = HelpDlg(self)
		#layout
		self.verticalLayout_2.addWidget(self.infoWidget)
		self.verticalLayout_3.addWidget(self.replayWindow)

		#connect
		self.connect(self.replayWindow, SIGNAL("commandFinished"), self.on_recvC)
		self.connect(self.replayWindow, SIGNAL("unitSelected"), self.infoWidget.newUnitInfo)
		self.connect(self.replayWindow, SIGNAL("mapSelected"), self.infoWidget.newMapInfo)
		self.replayWindow.moveAnimEnd.connect(self.on_aniFinished)
		self.connect(self.replayWindow, SIGNAL("errorOperation"), self.on_errOpr)
		self.connect(self, SIGNAL("ableToPlay()"), self.on_ablePlay, Qt.QueuedConnection)

		self.setWindowTitle("Human_Vs_Ai")
		self.setWindowIcon(QIcon(QPixmap(":hero_11.png")))

	def updateUi(self):
		if self.mapPath and self.aiPath and not self.started:
			self.startButton.setEnabled(True)
		else:
			self.startButton.setEnabled(False)

	@pyqtSlot()
	def on_aiButton_clicked(self):
		filename = QFileDialog.getOpenFileName(self, _frUtf("载入ai文件"), AI_DIR,
											   "ai files(*.exe;*.py)")
		if filename:
			self.aiPath = filename
			self.info_ai.setText(filename)
			self.updateUi()

	@pyqtSlot()
	def on_mapButton_clicked(self):
		filename = QFileDialog.getOpenFileName(self, _frUtf("载入map文件"), MAP_DIR,
											   "map files(*.map)")
		if filename:
			self.mapPath = filename
			self.info_map.setText(filename)
			self.updateUi()

	@pyqtSlot()
	def on_startButton_clicked(self):
		#检查工作
		if not os.path.exists(r"%s" %self.aiPath):
			QMessageBox.critical(self, _frUtf("错误"), _frUtf("ai文件 %s 不存在。" %self.aiPath),
								 QMessageBox.Ok, QMessageBox.NoButton)
			return
		if not os.path.exists(r"%s" %self.mapPath):
			QMessageBox.critical(self, _frUtf("错误"), _frUtf("map文件 %s 不存在。" %self.mapPath),
								 QMessageBox.Ok, QMessageBox.NoButton)
			return
		#打开与平台UI_PORT连接的线程
		self.started = True
		self.aiThread = AiThread(self)
		try:
			if self.info_ai.text() and self.info_map.text():
				self.aiThread.initialize(self.info_ai.text(),self.info_map.text())
			else:
				self.aiThread.initialize(DEFAULT_AI, DEFAULT_MAP)
		except:
			QMessageBox.critical(self, "Connection Error",
								 "Failed to connect to UI_PORT\n",
								 QMessageBox.Ok, QMessageBox.NoButton)
			self.started = False
			self.aiThread.deleteLater()
		else:
			self.connect(self.aiThread, SIGNAL("firstRecv"), self.on_firstRecv)
			self.connect(self.aiThread, SIGNAL("rbRecv"), self.on_rbRecv)
			self.connect(self.aiThread, SIGNAL("reRecv"), self.on_reRecv)
			self.connect(self.aiThread, SIGNAL("gameWinner"), self.on_gameWinner)
			self.connect(self.aiThread, SIGNAL("finished()"), self.aiThread,
							 SLOT("deleteLater()"))
			self.connect(self.aiThread, SIGNAL("finished()"), partial(self.on_threadF,0))
			self.connect(self.aiThread, SIGNAL("tmpRecv()"), self.on_tmpRecv)
			#self.connect(self, SIGNAL("aiShut()"), self.aiThread, SLOT("quit()"))
			self.connect(self, SIGNAL("aiShut()"), self.aiThread, SLOT("on_shut()"))
			self.aiThread.start()
			
		self.updateUi()
	#打开player线程
	def on_tmpRecv(self):
		self.playThread = Ui_Player(0, self.getComm, self)
		try:
			self.playThread.initialize()
		except:
			QMessageBox.critical(self, "Connection Error",
									  "Failed to connect to AI_PORT\n",
									  QMessageBox.Ok, QMessageBox.NoButton)
			self.playThread.deleteLater()
			self.aiThread.stop()
			self.aiThread.wait()
			self.aiThread.deleteLater()
			self.started = False

		else:
			self.connect(self.playThread, SIGNAL("getHeroType()"), self.on_getHero)
			self.connect(self.playThread, SIGNAL("firstCmd()"), self.on_firstCmd)
			self.connect(self.playThread, SIGNAL("mapRecv"), self.on_mapRecv)
			self.connect(self.playThread, SIGNAL("finished()"), self.playThread,
							 SLOT("deleteLater()"))
			self.connect(self.playThread, SIGNAL("finished()"), partial(self.on_threadF,1))
			#self.connect(self, SIGNAL("playShut()"), self.playThread, SLOT("quit()"))
			self.connect(self, SIGNAL("playShut()"), self.playThread, SLOT("on_shut()"))
			self.playThread.start()
		self.updateUi()

	@pyqtSlot()
	def on_helpButton_clicked(self):
		self.helpdlg = HelpDlg(self)
		self.helpdlg.exec_()


	@pyqtSlot()
	def on_returnButton_clicked(self):
		if self.started:
			answer = QMessageBox.question(self, _frUtf("稍等"), _frUtf("你的游戏还没有完全结束，你确定要退出吗?"),
										  QMessageBox.Yes, QMessageBox.No)
			if answer == QMessageBox.No:
				return
			#清理工作，停止游戏，关闭线程,强制结束游戏
			self.replayWindow.reset()
			if self.aiThread and self.aiThread.isRunning():
				#self.aiThread.terminate()
				#self.aiThread.conn.shutdown(socket.SHUT_RDWR)
				self.emit(SIGNAL("aiShut()"))
				#self.aiThread.exit()
				#self.aiThread.wait()
				#self.aiThread.stop()
				#self.aiThread.wait()
			global WaitForCommand, WaitForIni, WaitForAni
			WaitForIni.wakeAll()
			WaitForAni.wakeAll()
			WaitForCommand.wakeAll()
			if self.playThread and self.playThread.isRunning():
				#self.playThread.terminate()
				#self.playThread.exit()
				self.emit(SIGNAL("playShut()"))
				#self.playThread.stop()
				#self.playThread.wait()
			self.reset()
		self.updateUi()
		self.willReturn.emit()

	def on_threadF(self, arg):
		if arg:
			self.playThread = None
		else:
			self.aiThread = None

	def on_recvC(self, cmd):
		global WaitForCommand
		try:
			self.playThread.lock.lockForWrite()
			self.playThread.command = cmd
			WaitForCommand.wakeAll()
		finally:
			self.playThread.lock.unlock()

	def on_errOpr(self, err_ind):
		self.errorLabel.setText(err_ind)
		QTimer.singleShot(2000, self.resetError)
	
	def resetError(self):
		self.errorLabel.setText("")

	def on_getHero(self):
		dialog = GetHeroTypeDlg(self)
		name = ""
		if dialog.exec_():
			if len(dialog.choice) == 0:
				result = (6, 6)
			elif len(dialog.choice) == 2:
				result = tuple(dialog.choice)
			elif len(dialog.choice) == 1:
				result = tuple([dialog.choice[0], dialog.choice[0]])
			name = dialog.nameEdit.text()
			if not name:
				name = "Player"
			result = (name, result)
		else:
			result = ("Player", (6, 6))
		self.playerLabel.setText(result[0])
		global WaitForHero
		try:
			self.playThread.lock.lockForWrite()
			self.playThread.result = result
			WaitForHero.wakeAll()	
		finally:
			self.playThread.lock.unlock()



	def on_firstRecv(self, mapInfo, frInfo, aiInfo, baseInfo):
		self.replayWindow.Initialize(basic.Begin_Info(mapInfo, baseInfo), frInfo)

		#展示
		global WaitForIni
		self.nowRound = 0
		self.replayWindow.GoToRound(self.nowRound, 0)
		self.roundLabel.setText("Round 0")
		WaitForIni.wakeAll()
		try:
			self.playThread.lock.lockForWrite()
			self.playThread.flag = frInfo.id[0]
		finally:
			self.playThread.lock.unlock()
		self.Ani_Finished = True
		self.winner = None

	def on_rbRecv(self, rbInfo):
		self.replayWindow.UpdateBeginData(rbInfo)
#		#如果动画已经结束且在等待这一次的rbinfo,就调转回合
		if self.Ani_Finished and len(self.replayWindow.gameBegInfo) == self.nowRound + 2:
			self.nowRound += 1
			self.replayWindow.GoToRound(self.nowRound, 0)
			self.roundLabel.setText("Round %d" %self.nowRound)
			#并且发出ablePlay要么play动画,要么开始等待作出命令
			self.emit(SIGNAL("ableToPlay()"))#queued connection

	def on_reRecv(self, rCommand, reInfo):
		self.replayWindow.UpdateEndData(rCommand, reInfo)
		#第一次接收直接开始播放
		if len(self.replayWindow.gameEndInfo) == 1:
			self.Ani_Finished = False
			self.replayWindow.Play()
		#如果动画已结束则会设置abletoplay为False不然就设置abletoplay为假
		if self.Ani_Finished and len(self.replayWindow.gameEndInfo) == self.nowRound + 1:
			self.Ani_Finished = False
			self.replayWindow.Play()


	def on_aniFinished(self):
		#判断是否更新到足够调转的回合开始信息
		self.replayWindow.GoToRound(self.nowRound , 1)
		self.Ani_Finished = True
		if len(self.replayWindow.gameBegInfo) <= self.nowRound + 1:
			if self.nowRound == self.lastRound and self.winner != None:
				self.on_gameEnd(self.winner)
		else:
			self.nowRound += 1
			self.replayWindow.GoToRound(self.nowRound, 0)
			self.roundLabel.setText("Round %d" %self.nowRound)
			self.emit(SIGNAL("ableToPlay()"))

	#判断有没有回合结束信息相关的更新
	def on_ablePlay(self):
		#判断是否更新到足够播放的回合末信息,如果没有则设置Able_To_Play（基本不可能但还是在调试后加上）并判断是否该是下达命令的时候了
		global Able_To_Comm,mutex
		if len(self.replayWindow.gameEndInfo) < self.nowRound + 1:#==
			global Already_Wait,WaitForAni,mutex
			#临时的判断可以不可以开始做命令的变量
			flag = False
			try:
				mutex.lock()
				if Already_Wait:
			#如果uiplayer线程已经等待动画结束,提示用户开始进行动作
					Already_Wait = False
					flag = True
			finally:
				mutex.unlock()
			if flag and self.replayWindow.gameBegInfo[self.replayWindow.nowRound].id[0] == 1:
				#wake 动画
				WaitForAni.wakeAll()
			#以防命令还没有准备完.每次没有接收到最新的endinfo(不管是等待命令还是等待endinfo)都会设置abletocomm
			else:
				try:
					mutex.lock()
					if Already_Wait:
				#如果uiplayer线程已经等待动画结束,提示用户开始进行动作
						Already_Wait = False
						flag = True
				finally:
					mutex.unlock()
				if flag:
					WaitForAni.wakeAll()
				#以防命令还没有准备完.虽然不太可能,每次没有接收到最新的endinfo(不管是等待命令还是等待endinfo)都会设置abletocomm
				else:
					try:
						mutex.lock()
						Able_To_Comm = True
					finally:
						mutex.unlock()
		else:
			try:
				mutex.lock()
				Able_To_Comm = False
			finally:
				mutex.unlock()
			self.Ani_Finished = False
			self.replayWindow.Play()


	def on_firstCmd(self):
		pass

	def on_mapRecv(self, mapInfo, baseInfo):
		print "hi map recv"#for test
		self.replayWindow.SetInitMap(mapInfo,baseInfo)

	def on_gameWinner(self, winner):
		if not (self.nowRound == self.replayWindow.latestRound and self.Ani_Finished):
			self.lastRound = self.replayWindow.latestRound
			self.winner = winner

	def on_gameEnd(self, winner):
		info = "Player %d win the game" %winner if winner != -1 else "DRAW!"
		QMessageBox.information(self, "Game Winner", info)
		#需要其他特效再加
		answer = QMessageBox.question(self, _frUtf("保存"), _frUtf("是否保存回放文件?"),
											  QMessageBox.Yes, QMessageBox.No)
		global WaitForReplay
		try:
			self.aiThread.mutex.lock()
			if answer == QMessageBox.Yes:
				self.aiThread.replay_mode = True
		finally:
			self.aiThread.mutex.unlock()
			WaitForReplay.wakeAll()
		#一些清理工作，方便开始下一局游戏,
		self.reset()
		self.replayWindow.reset()
		self.updateUi()
	
	def reset(self):
		self.started = False

		self.winner = None
		self.lastRound = -1
		self.Able_To_Play = True
		self.nowRound = 0

#test
if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	form = HumanvsAi()
	#form.showFullScreen()
	form.show()
	app.exec_()
