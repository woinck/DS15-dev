#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#人机对战界面

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import lib.human.ui_humanvsai
from lib.human.Humanai_Replay_event import HumanReplay
from lib.human.info_widget import *
import basic, sio, select, os, socket
from lib.human.herotypedlg import GetHeroTypeDlg
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
WaitForTemp=QWaitCondition()
mutex = QMutex()
#tmp
#for debug
DEFAULT_MAP = os.getcwd() + "//new_map.map"
DEFAULT_AI = os.getcwd() + "//sclientai.py"

#def mapReverse(maps):
#	new_map = []
#	for i in range(len(maps[0])):
#		new_map.append([])
#		for j in range(len(maps)):
#			new_map[i].append(maps[j][i])
#	return new_map

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
			server_run = sio.Prog_Run(os.getcwd() + sio.SERV_FILE_NAME)
			server_run.start()

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
	def run(self):
		temp = sio._recvs(self.conn)#add base info
		print 'i sent it!!!!!!!!!!'
		self.emit(SIGNAL("tmpRecv()"))
		#print temp#for test
		#global WaitForTemp
		#WaitForTemp.wakeAll()
		mapInfo,baseInfo,aiInfo = sio._recvs(self.conn)#add base info
		frInfo = sio._recvs(self.conn)
		#mapInfo = mapReverse(mapInfo)#debugging
		self.emit(SIGNAL("firstRecv"),mapInfo, frInfo, aiInfo, baseInfo)
		print "first rbInfo"
		rCommand, reInfo = sio._recvs(self.conn)
		self.emit(SIGNAL("reRecv"), rCommand, reInfo)
		while not reInfo.over and not self.isStopped():
			rbInfo = sio._recvs(self.conn)
			print "here is rbInfo got in platform"#for test
			if self.isStopped():
				break
			self.emit(SIGNAL("rbRecv"),rbInfo)
			readFlag = 0
			while not readFlag:
				ready = select.select([self.conn], [], [], WAIT_TIME)
				if ready[0]:
					rCommand,reInfo = sio._recvs(self.conn)
					readFlag = 1

				if self.isStopped():
					break
			if self.isStopped():
				break

			self.emit(SIGNAL("reRecv"),rCommand, reInfo)
		if not self.isStopped():
			winner = sio._recvs(self.conn)
			self.emit(SIGNAL("gameWinner"),winner)
	#	是否存储回放文件
		if not self.isStopped():
			global WaitForReplay
			WaitForReplay.wait()

			sio._sends(self.conn,replay_mode)
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
#		self.parent = parent
		self.result = ("Player", (6,6))

	def initialize(self):
		self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		num = 0 #for test
		for i in range(5):
			num += 1
			try:
				print "try %d" %num
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
			#print "emit hero"#for test
			global WaitForHero
			self.lock.lockForRead()
			WaitForHero.wait(self.lock)
			#print "rec hero",self.result#for test
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
			print "able to command?", Able_To_Comm
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
#			self.emit(SIGNAL("waitforC()"))
			# time for player to make a command here!!
					print "~~~ani waiting"#for test
					WaitForAni.wait(self.lock)
#			self.lock.lockForRead()
				else:
					self.emit(SIGNAL("firstCmd()"))
					#print "lala"#for test
					#检查player是否是第一个开始做命令的,若是则要等待initialize(需要加强双向等待)
					WaitForIni.wait(self.lock)
			finally:
				self.lock.unlock()

		self.func()
		print "func called"#for test
		WaitForCommand.wait(self.lock)
		self.lock.unlock()
		return self.command

	def run(self):
		mapInfo,base = sio._recvs(self.conn)
	#	mapInfo = mapReverse(mapInfo)#debugging
		self.emit(SIGNAL("mapRecv"), mapInfo)
		result = self.GetHeroType(mapInfo)
		sio._sends(self.conn, (result[0],result[1][0]))
		while True and not self.isStopped():
			readFlag2 = 0
			while not readFlag2:
				ready2 = select.select([self.conn], [], [], WAIT_TIME)
				if ready2[0]:
					rBeginInfo = sio._recvs(self.conn)
					readFlag2 = 1
				if self.isStopped():
					break
			print 'rbInfo got'
			if rBeginInfo != '|':
				sio._sends(self.conn,self.AI(rBeginInfo))
				print 'cmd sent'
				self.cmdNum += 1
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

#class CommThread(QThread):
#	def __init__(self, func, parent = None):
#		super(CommTread, self).__init__(parent)
#		self.func = func

#	def run(self):
#		self.func()
#	def stop(self):
#		#end GetCommand()
#		pass

class HumanvsAi(QWidget, lib.human.ui_humanvsai.Ui_HumanvsAi):
	willReturn = pyqtSignal()
	def __init__(self, parent = None):
		super(HumanvsAi, self).__init__(parent)
		self.setupUi(self)
	 #   pal = self.palette()
	#	pal.setBrush(QPalette.Window, QBrush(Qt.NoBrush))
	 #   self.setPalette(pal)


		self.aiPath = ""
		self.mapPath = ""
		self.started = False
		self.nowRound = 0
		self.gameBegInfo = []
		self.gameEndInfo = []
#		self.startButton.setEnabled(False)
		self.Able_To_Play = True
		self.winner = None
		self.lastRound = -1
		#widget
		self.scene = QGraphicsScene()
		self.replayWindow = HumanReplay(self.scene)

		self.getComm = self.replayWindow.GetCommand

		self.infoWidget = InfoWidget()

		#layout
		self.verticalLayout_2.addWidget(self.infoWidget)
		self.verticalLayout_3.addWidget(self.replayWindow)
#		self.

		#connect
		self.connect(self.replayWindow, SIGNAL("commandFinished"), self.on_recvC)
#		self.connect(self.replayWindow, SIGNAL("unitSelected"), self.on_unitS)
#		self.connect(self.replayWindow, SIGNAL("mapSelected"), self.on_mapS)
		self.connect(self.replayWindow, SIGNAL("unitSelected"), self.infoWidget.newUnitInfo)
		self.connect(self.replayWindow, SIGNAL("mapSelected"), self.infoWidget.newMapInfo)
		#self.replayWindow.moveAnimEnd.connect(self.on_aniFinished)
		self.connect(self.replayWindow.animation, SIGNAL("finished()"), self.on_aniFinished)#for test
		self.connect(self, SIGNAL("ableToPlay()"), self.on_ablePlay, Qt.QueuedConnection)
		#other
		pal = self.scoLabel1.palette()
		br = QBrush(Qt.Dense3Pattern)
		br.setColor(QColor(255,51,0,200))
		pal.setBrush(QPalette.Window, br)
		self.scoLabel1.setPalette(pal)
		self.scoLabel2.setPalette(pal)

		self.roundLabel.setWindowOpacity(0)

	def updateUi(self):
#		if self.mapPath and self.aiPath and not self.started:
#			self.startButton.setEnabled(True)
#		else:
#			self.startButton.setEnabled(False)
		pass
	@pyqtSlot()
	def on_aiButton_clicked(self):
		filename = QFileDialog.getOpenFileName(self, _frUtf("载入ai文件"), AI_DIR,
											   "ai files(*.py)")
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

		#检查工作
#	   if not os.path.exists(r"%s" %self.aiPath):
#			QMessageBox.critical(self, _frUtf("错误"), _frUtf("ai文件 %s 不存在。" %self.aiPath),
#								 QMessageBox.Ok, QMessageBox.NoButton)
#			return
#		if not os.path.exists(r"%s" %self.mapPath):
#			QMessageBox.critical(self, _frUtf("错误"), _frUtf("map文件 %s 不存在。" %self.mapPath),
#								 QMessageBox.Ok, QMessageBox.NoButton)
#			return
		#打开与平台UI_PORT连接的线程
	@pyqtSlot()
	def on_startButton_clicked(self):

		flag = 0
		self.aiThread = AiThread(self)
 #	   try:
		if self.info_ai.text() and self.info_map.text():
			self.aiThread.initialize(self.info_ai.text(),self.info_map.text())
		else:
			self.aiThread.initialize(DEFAULT_AI, DEFAULT_MAP)
			#		except:
#			flag = 1
#		except:

#		else:
		print "link now"
		self.connect(self.aiThread, SIGNAL("firstRecv"), self.on_firstRecv)
		self.connect(self.aiThread, SIGNAL("rbRecv"), self.on_rbRecv)
		self.connect(self.aiThread, SIGNAL("reRecv"), self.on_reRecv)
		self.connect(self.aiThread, SIGNAL("mapRecv"), self.on_mapRecv)
		self.connect(self.aiThread, SIGNAL("gameWinner"), self.on_gameWinner)
#			self.connect(self.aiThread, SIGNAL("finished()"), self.replayWindow.updateUI)
		self.connect(self.aiThread, SIGNAL("finished()"), self.aiThread,
						 SLOT("deleteLater()"))
		self.connect(self.aiThread, SIGNAL("finished()"), partial(self.on_threadF,0))
		self.connect(self.aiThread, SIGNAL("tmpRecv()"), self.on_tmpRecv)
		self.aiThread.start()
		
	def on_tmpRecv(self):
		self.playThread = Ui_Player(0, self.getComm, self)
#		try:
		self.playThread.initialize()
#print "link now 2"#for test
#		except:
#			if not flag:
#				flag = 2
#			else:
#				flag = 3
#		else:
			#connect work
#			self.connect(self.playThread, SIGNAL("waitforC()"), self.on_waitforC)
#		self.connect(self.playThread, SIGNAL("nameGet(QString)"), self.on_nameGet)
		self.connect(self.playThread, SIGNAL("getHeroType()"), self.on_getHero)
		self.connect(self.playThread, SIGNAL("firstCmd()"), self.on_firstCmd)
		self.connect(self.playThread, SIGNAL("finished()"), self.playThread,
						 SLOT("deleteLater()"))
		self.connect(self.playThread, SIGNAL("finished()"), partial(self.on_threadF,1))
		self.playThread.start()
#		if flag == 0:
#			self.started = True
#			self.updateUi()
#			self.playThread.start()
#			self.aiThread.start()
#		elif flag == 1:
#			QMessageBox.critical(self, "Connection Error",
#								 "Failed to connect to UI_PORT\n",
#								 QMessageBox.Ok, QMessageBox.NoButton)
#			self.aiThread.deleteLater()
#			self.playThread.deleteLater()
#		elif flag == 2:
#			QMessageBox.critical(self, "Connection Error",
#									  "Failed to connect to AI_PORT\n",
#									  QMessageBox.Ok, QMessageBox.NoButton)
#			self.playThread.deleteLater()
#			self.aiThread.deleteLater()
#		else:
#			QMessageBox.critical(self, "Connection Error",
#								 "Failed to connect to UI_PORT and the AI_PORT\n",
#								 QMessageBox.Ok, QMessageBox.NoButton)
#			self.aiThread.deleteLater()
#			self.playThread.deleteLater()

	@pyqtSlot()
	def on_helpButton_clicked(self):
		#显示帮助信息
		pass

	@pyqtSlot()
	def on_returnButton_clicked(self):
		if self.started:
			answer = QMessageBox.question(self, _frUtf("稍等"), _frUtf("你的游戏还没有完全结束，你确定要退出吗?"),
										  QMessageBox.Yes, QMessageBox.No)
			if answer == QMessageBox.No:
				return
			#清理工作，停止游戏，关闭线程,强制结束游戏
			if self.aiThread and self.aiThread.isRunning():
				self.aiThread.stop()
				self.aiThread.wait()
			global WaitForCommand, WaitForIni, WaitForAni
			WaitForIni.wakeAll()
			WaitForAni.wakeAll()
			WaitForCommand.wakeAll()
			if self.playThread and self.playThread.isRunning():
				self.playTread.stop()
				self.playThread.wait()
#			if self.commandThread.running():
#				self.commandThread.stop()
#				self.commandThread.wait()
			self.reset()
			self.started = False
			self.nowRound = 0
		self.willReturn.emit()

	def on_threadF(self, arg):
		if arg:
			self.playThread = None
		else:
			self.aiThread = None

#	def on_waitforC(self):
#		self.commThread = CommThread(self, self.getComm)
#		self.connect(self,commThread, SIGNAL("finished()"), self.commThread, SLOT("deleteLater()"))
#		self.commThread.start()
		#提示用户开始进行动作
#		self.roundLabel.setText(_frUtf("开始操作吧!"))
#		self.labelAnimation()

	def on_recvC(self, cmd):
		#tmp_move = cmd.move
		#cmd.move = (tmp_move[1], tmp_move[0])
		global WaitForCommand
		try:
			self.playThread.lock.lockForWrite()
			self.playThread.command = cmd
			WaitForCommand.wakeAll()
		finally:
			self.playThread.lock.unlock()
#			WaitForCommand.wakeAll()
			print "command:", cmd.move, cmd.order,cmd.target
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
#		self.emit(SIGNAL("nameGet(QString)"), result[0])
		#return result
		self.playerLabel.setText(result[0])
		global WaitForHero
		try:
			self.playThread.lock.lockForWrite()
			self.playThread.result = result
			WaitForHero.wakeAll()	
		finally:
			#print "abc"#for test
			self.playThread.lock.unlock()



	def on_firstRecv(self, mapInfo, frInfo, aiInfo, baseInfo):
		self.replayWindow.Initialize(basic.Begin_Info(mapInfo, baseInfo), frInfo)
		self.setRoundBegInfo(frInfo)
		self.gameBegInfo.append(frInfo)
		#展示
		global WaitForIni
		self.nowRound = 0
		self.replayWindow.GoToRound(self.nowRound, 0)
		WaitForIni.wakeAll()
		self.roundLabel.setText("Round %d" %(self.nowRound))
		self.labelAnimation()
		try:
			self.playThread.lock.lockForWrite()
			self.playThread.flag = frInfo.id[0]
		finally:
			self.playThread.lock.unlock()
		self.Ani_Finished = True
		self.winner = None

	def on_rbRecv(self, rbInfo):
		self.replayWindow.UpdateBeginData(rbInfo)
		self.setRoundBegInfo(rbInfo)
		self.gameBegInfo.append(rbInfo)
#		#如果动画已经结束且在等待这一次的rbinfo,就调转回合
		if self.Ani_Finished and len(self.gameBegInfo) == self.nowRound + 2:
			self.nowRound += 1
			self.replayWindow.GoToRound(self.nowRound, 0)
			self.roundLabel.setText("Round %d" %self.nowRound)
			self.labelAnimation()
			#设置ani_Finished False
#			self.Ani_Finished = False
			#并且发出ablePlay要么play动画,要么开始等待作出命令
			self.emit(SIGNAL("ableToPlay()"))#queued connection

#		self.roundLabel.setText("Round %d" %len(self.gameBegInfo))
#		self.labelAnimation()


	def on_reRecv(self, rCommand, reInfo):
		#tmp = rCommand.move
		#rCommand.move = (tmp[1], tmp[0])
		self.replayWindow.UpdateEndData(rCommand, reInfo)
		self.setRoundEndInfo(rCommand, reInfo)
		self.gameEndInfo.append((rCommand,reInfo))
		print "rCommand recv:", rCommand.move, rCommand.order, rCommand.target
		#第一次接收直接开始播放
		if len(self.gameEndInfo) == 1:
			self.Ani_Finished = False
			self.replayWindow.Play()
		#如果动画已结束则会设置abletoplay为False不然就设置abletoplay为假
		if self.Ani_Finished and len(self.gameEndInfo) == self.nowRound + 1:
			self.Ani_Finished = False
			self.replayWindow.Play()
#			global Able_To_Comm,mutex
#			try:
#				mutex.lock()
#				Able_To_Comm = False
#			finally:
#				mutex.unlock()


	def on_aniFinished(self):
		#判断是否更新到足够调转的回合开始信息
		print "anifinished!!!!!!!!!!!!~~~~~~"#for test
		self.replayWindow.GoToRound(self.nowRound , 1)
		self.Ani_Finished = True#？？？？是否改成全局变量
		if len(self.gameBegInfo) <= self.nowRound + 1:
			print "nani!!! you are here!!?now round:", self.nowRound, "total:", len(self.gameBegInfo) - 1#for test
			if self.nowRound == self.lastRound and self.winner:
				self.on_gameWinner(self.winner)
		else:
			self.nowRound += 1
			print "goto", self.nowRound
			self.replayWindow.GoToRound(self.nowRound, 0)
			self.roundLabel.setText("Round %d" %self.nowRound)
			self.labelAnimation()
			self.emit(SIGNAL("ableToPlay()"))
	#判断有没有回合结束信息相关的更新
	def on_ablePlay(self):
		#判断是否更新到足够播放的回合末信息,如果没有则设置Able_To_Play（基本不可能但还是在调试后加上）并判断是否该是下达命令的时候了
		global Able_To_Comm,mutex
		if len(self.gameEndInfo) < self.nowRound + 1:#==
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
				self.roundLabel.setText(_frUtf("开始操作吧!"))
				self.labelAnimation()
			#以防命令还没有准备完.虽然不太可能,每次没有接收到最新的endinfo(不管是等待命令还是等待endinfo)都会设置abletocomm
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
					self.roundLabel.setText(_frUtf("开始操作吧!"))
					self.labelAnimation()
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
#		time.sleep(1)
		self.roundLabel.setText(_frUtf("开始操作吧!"))
		self.labelAnimation()

	def on_mapRecv(self, mapInfo):
		self.replayWindow.SetInitMap(mapInfo)

	def on_gameWinner(self, winner):
		if not (self.nowRound == self.replayWindow.latestRound and self.Ani_Finished):
			self.lastRound = self.replayWindow.latestRound
			self.winner = winner
			return
		QMessageBox.information(self, "Game Winner", "player %s win the game" %winner)
		#需要其他特效再加
		answer = QMessageBox.question(self, _frUtf("保存"), _frUtf("是否保存回放文件?"),
											  QMessageBox.Yes, QMessageBox.No)
		global WaitForReplay
		if answer == QMessageBox.Yes:
			#把每个回合信息写入(也可以考虑在游戏一开始就设置这个选择)
				self.aiThread.replay_mode = True
				WaitForReplay.wakeAll()
		#一些清理工作，方便开始下一局游戏,
		self.started = False
		self.updateUi()

	def on_nameGet(self, name):
		self.playerLabel.setText(name)
		#要展示英雄信息的话也在这里做

#	def on_unitS(self, unit):
#		self.infoWidget.newUnitInfo(unit)

#	def on_mapS(self, mapInfo):
#		self.infoWidget.newMapInfo(mapInfo)

	def setRoundBegInfo(self, rbInfo):
		pass
	def setRoundEndInfo(self, rCommand, reInfo):
		#同步分数
		sco1 = reInfo.score[0]
		sco2 = reInfo.score[1]
		self.scoLabel1.setText("%d"%sco1)
		self.scoLabel2.setText("%d"%sco2)
 
	def labelAnimation(self):
		animation_1 = QParallelAnimationGroup(self)
		animation_1_1 = QPropertyAnimation(self.roundLabel, "geometry")
		animation_1_1.setDuration(2000)
		animation_1_1.setStartValue(self.roundLabel.geometry())
		animation_1_1.setEndValue(QRect(450,150,141,41))
		animation_1_2 = QPropertyAnimation(self.roundLabel, "windowOpacity")
		animation_1_2.setDuration(1500)
		animation_1_2.setStartValue(0)
		animation_1_2.setEndValue(1)
		animation_1_1.setEasingCurve(QEasingCurve.OutCubic)
		animation_1.addAnimation(animation_1_1)
		animation_1.addAnimation(animation_1_2)

		animation_2 = QParallelAnimationGroup(self)
		animation_2_1 = QPropertyAnimation(self.roundLabel, "geometry")
		animation_2_1.setDuration(2000)
		animation_2_1.setStartValue(self.roundLabel.geometry())
		animation_2_1.setEndValue(QRect(450, 40, 141, 41))
		animation_2_2 = QPropertyAnimation(self.roundLabel, "windowOpacity")
		animation_2_2.setDuration(1000)
		animation_2_2.setStartValue(1)
		animation_2_2.setEndValue(0)
		animation_2_1.setEasingCurve(QEasingCurve.OutCubic)
		animation_2.addAnimation(animation_2_1)
		animation_2.addAnimation(animation_2_2)

		animation = QSequentialAnimationGroup(self)
		animation_3 = QPauseAnimation(1000)
		animation.addAnimation(animation_1)
		animation.addAnimation(animation_3)
		animation.addAnimation(animation_2)
		self.connect(animation, SIGNAL("finished()"), animation, SLOT("deleteLater()"))
		animation.start()


#test
if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	form = HumanvsAi()
	form.show()
	app.exec_()