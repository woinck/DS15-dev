#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#AI debugger for watching two ai fighting

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import qrc_resource
from lib.debugger.info_widget_debugger import *
#from Ai_Thread import *
from Debug_CtrlWidget import *
import socket,cPickle,time,basic, os
import sio

DEBUG_MODE = [False, False]
DEFAULT_SCILENT_AI = os.getcwd() + "\\Sample_AI.py"#默认的ai路径,待设置
DEFAULT_MAP = os.getcwd() + "\\mapwithturret.map"

#WaitForNext = QWaitCondition()
#WaitForPause = QWaitCondition()

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
			sio._sends(self.conn,(sio.AI_VS_AI, self.map ,[self.ai1, self.ai2], DEBUG_MODE))

			mapInfo,baseInfo,aiInfo = sio._recvs(self.conn)
			try:
				rbInfo = sio._recvs(self.conn)
				self.emit(SIGNAL("firstRecv"), mapInfo, rbInfo, aiInfo, baseInfo)
			except:
				self.stop()
			try:
				rCommand,reInfo = sio._recvs(self.conn)
				self.emit(SIGNAL("reRecv"), rCommand, reInfo)
			except:
				self.stop()
			self.emit(SIGNAL("round()"))

			while not reInfo.over and not self.isStopped():
				try:
					rbInfo = sio._recvs(self.conn)
					self.emit(SIGNAL("rbRecv"), rbInfo)
				except:
					self.stop()
				try:
					rCommand,reInfo = sio._recvs(self.conn)
					self.emit(SIGNAL("reRecv"), rCommand, reInfo)
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

#调试器主界面
class ai_debugger(QMainWindow):
	def __init__(self, parent = None):
		super(ai_debugger, self).__init__(parent)

		self.started = False
		self.loaded_ai = []
		self.loaded_map = None
		self.pltThread = None
		self.ispaused = False
		self.gameBegInfo = []
		self.gameEndInfo = []

		#composite replay widget
		self.replayScene = QGraphicsScene()
		self.replayWindow = AiReplayWidget(self.replayScene)
		self.setCentralWidget(self.replayWindow)

		#add a dock widget to show infomations of the running AI and loaded files

		self.infoDockWidget = QDockWidget("Infos", self)
		self.infoDockWidget.setObjectName("InfoDockWidget")
		self.infoDockWidget.setAllowedAreas(Qt.RightDockWidgetArea)
		self.infoWidget = InfoWidget(self)
		self.infoDockWidget.setWidget(self.infoWidget)
		self.addDockWidget(Qt.RightDockWidgetArea, self.infoDockWidget)
		self.info_visible = self.infoDockWidget.isVisible()

		#add status bar

		self.status = self.statusBar()
		self.status.setSizeGripEnabled(False)
		self.status.showMessage("Ready", 5000)

		#creat game actions

		self.gameStartAction = self.createAction("&Start", self.startGame,
											"Ctrl+S","gameStart",
											"开始游戏")
		self.gameEndAction = self.createAction("&End", self.endGame,
										 "Ctrl+E","gameEnd",
										 "结束游戏")
		self.gameLoadAction1 = self.createAction("Load &AI", self.loadAIdlg,
										  "Ctrl+A", "loadAI",
										  "加载ai")
		self.gameLoadAction2 = self.createAction("Load &MAP", self.loadMapdlg,
										   "Ctrl+M", "loadMap",
										   "加载地图")
		self.gameUnloadAction = self.createAction("Unload Ais", self.unloadAI,
												  tip = "清楚已加载的ai")
		#creat game menu and add actions
		self.gameMenu = self.menuBar().addMenu("&Game")
		self.addActions(self.gameMenu, (self.gameStartAction,
								  self.gameEndAction, None, self.gameLoadAction1,
										self.gameLoadAction2, self.gameUnloadAction))

		#creat actions and add them to config menu
		self.configMenu = self.menuBar().addMenu("&Config")
		resetAction = self.createAction("&Reset", self.reset,
										icon = "reset",
										tip = "reset all settings")
		
		self.debugAction1 = self.createAction("Debug1", self.setDebugMode1, icon = "debug_mode0",
										checkable = True, signal = "toggled(bool)", tip ="ai设置debug模式")
		self.debugAction2 = self.createAction("Debug2", self.setDebugMode2, icon = "debug_mode0",
										checkable = True, signal = "toggled(bool)", tip = "ai2设置debug模式")
		self.addActions(self.configMenu, (resetAction, self.debugAction1, self.debugAction2))

		#creat action and add it to window menu
		self.dockAction = self.createAction("(dis/en)able infos", self.setInfoWidget,
									   tip = "显示/隐藏信息栏",
									   checkable = True,
									   signal = "toggled(bool)")
		self.windowMenu = self.menuBar().addMenu("&Window")
		self.windowMenu.addAction(self.dockAction)
		self.dockAction.setChecked(True)
		#creat toolbars and add actions

		gameToolbar =  self.addToolBar("Game")
		self.addActions(gameToolbar, (self.gameStartAction,
								  self.gameEndAction, self.gameLoadAction1, self.gameLoadAction2,None,self.debugAction1, self.debugAction2))

		self.connect(self.infoWidget, SIGNAL("hided()"), self.synhide)
		#to show messages
		self.connect(self.replayWindow.replayWidget, SIGNAL("unitSelected"),
					 self.infoWidget.newUnitInfo)
		self.connect(self.replayWindow.replayWidget, SIGNAL("mapSelected"),
					 self.infoWidget.newMapInfo)
		#进度条到主界面的通信
		self.connect(self.replayWindow, SIGNAL("goToRound"), self.infoWidget.on_goToRound)



		self.updateUi()
		self.setWindowTitle("MIRROR_Debugger")


	#wrapper function for reducing codes
	def createAction(self, text, slot=None, shortcut=None, icon=None,
					 tip=None, checkable=False, signal="triggered()"):
		action = QAction(text, self)
		if icon is not None:
			action.setIcon(QIcon(":/%s.png" % icon))
		if shortcut is not None:
			action.setShortcut(shortcut)
		if tip is not None:
			action.setToolTip(QString.fromUtf8(tip))
			action.setStatusTip(QString.fromUtf8(tip))
		if slot is not None:
			self.connect(action, SIGNAL(signal), slot)
		if checkable:
			action.setCheckable(True)
		return action

	def addActions(self, target, actions):
		for action in actions:
			if action is None:
				target.addSeparator()
			else:
				target.addAction(action)

	#enable/disable actions according to the game status
	def updateUi(self):
		if len(self.loaded_ai) == 2 and self.loaded_map:
			if not self.started:
				self.gameStartAction.setEnabled(True)
				self.gameEndAction.setEnabled(False)
				self.gameLoadAction1.setEnabled(True)
				self.gameLoadAction2.setEnabled(True)
			else:
				self.gameStartAction.setEnabled(False)
				self.gameEndAction.setEnabled(True)
#				self.gameLoadAction1.setEnabled(False)
#				self.gameLoadAction2.setEnabled(False)
		else:
			self.gameStartAction.setEnabled(False)
			self.gameEndAction.setEnabled(False)
 #		   self.gameLoadAction1.setEnabled(True)
 #		   self.gameLoadAction2.setEnabled(True)

	#game operation slot
	def startGame(self):
		#for debug
		#if not self.loaded_ai:
		#	self.loaded_ai.append(DEFAULT_SCILENT_AI)
		#	self.loaded_ai.append(DEFAULT_SCILENT_AI)
		#if not self.loaded_map:
	#		self.loaded_map = DEFAULT_MAP
	#	if len(self.loaded_ai) == 1:
		 #加入默认的什么都不做ai
	#		self.loaded_ai.append(DEFAULT_SCILENT_AI)
		#开始这个线程开始交互
		if len(self.loaded_ai) < 2 or not self.loaded_map:
			return
		self.pltThread = AiThread(unicode(self.loaded_map), *self.loaded_ai)

		self.connect(self.pltThread, SIGNAL("firstRecv"), self.on_firstRecv)
		self.connect(self.pltThread, SIGNAL("rbRecv"), self.on_rbRecv)
		self.connect(self.pltThread, SIGNAL("reRecv"), self.on_reRecv)
		self.connect(self.pltThread, SIGNAL("gameEnd"), self.on_gameWinner)
		self.connect(self, SIGNAL("toShut()"), self.pltThread, SLOT("on_shut()"))
		self.connect(self.pltThread, SIGNAL("finished()"), self.deletePlt)

		self.started = True
		self.replayWindow.started = True
		self.updateUi()

		self.pltThread.start()

	def deletePlt(self):
		self.pltThread.deleteLater()
		self.pltThread = None

	def endGame(self):
		#清空游戏缓存数据
		#强制在游戏没有进行到胜利条件的时候结束游戏
		if self.pltThread and self.pltThread.isRunning():
			self.emit(SIGNAL("toShut()"))
		self.gameBegInfo = []
		self.gameEndInfo = []
		self.replayWindow.reset()
		self.started = False
		self.updateUi()

	#把已经选择好的的ai文件路径清空,以便修改ai文件路径
	def unloadAI(self):
		self.loaded_ai = []
		self.infoWidget.infoWidget_Game.setAiFileinfo(["",""])
		self.updateUi()

	def loadAIdlg(self):
		dir = QDir.toNativeSeparators(r".")#/FileAI")
		fname = unicode(QFileDialog.getOpenFileName(self,
													"load AI File", dir,
													"AI files (%s)" % "*.exe"))
		if len(self.loaded_ai) < 2 and fname:
			self.loaded_ai.append(unicode(fname))
			self.infoWidget.infoWidget_Game.setAiFileinfo(self.loaded_ai)
			self.updateUi()

	def loadMapdlg(self):
		dir = QDir.toNativeSeparators(r"./FileMap")
		fname = unicode(QFileDialog.getOpenFileName(self,
													"load Map File", dir,
													"Map files (%s)" % "*.map"))
		if fname and fname != self.loaded_map:
			self.loaded_map = fname
			self.infoWidget.infoWidget_Game.setMapFileinfo(self.loaded_map)
			self.updateUi()

	def setDebugMode1(self, debug_mode):
		global DEBUG_MODE
		DEBUG_MODE[0] = debug_mode

	def setDebugMode2(self, debug_mode):
		global DEBUG_MODE
		DEBUG_MODE[1] = debug_mode
			
	def on_firstRecv(self, mapInfo, frInfo, aiInfo, baseInfo):
		print "fisrtRecv"
		self.replayWindow.updateIni(basic.Begin_Info(mapInfo, baseInfo), frInfo)
		self.infoWidget.beginRoundInfo(frInfo)
		self.gameBegInfo.append(frInfo)

	def on_rbRecv(self, rbInfo):
		self.replayWindow.updateBeg(rbInfo)
		self.gameBegInfo.append(rbInfo)

	def on_reRecv(self, rCommand, reInfo):
		self.replayWindow.updateEnd(rCommand, reInfo)
		self.gameEndInfo.append((rCommand,reInfo))


	#胜利展示
	def on_gameWinner(self, winner):
		QMessageBox.information(self, QString.fromUtf8("游戏结束"), "player %s win the game" %winner)
		#需要其他特效再加

	def reset(self):
		self.debugAction1.setChecked(False)
		self.debugAction2.setChecked(False)
		self.loaded_ai = []
		self.loaded_map = ""
		self.infoWidget.infoWidget_Game.setAiFileinfo(self.loaded_ai)
		self.infoWidget.infoWidget_Game.setMapFileinfo(self.loaded_map)
		self.updateUi()
#为了同步窗口菜单和信息栏的关闭和打开
	def synhide(self):
		self.dockAction.setChecked(False)
		self.info_visible = False
	def setInfoWidget(self):
		if (self.info_visible):
			self.infoDockWidget.close()
			self.info_visible = False
		else:
			self.infoDockWidget.show()
			self.info_visible = True

if __name__ == "__main__":
	app = QApplication(sys.argv)
	form = ai_debugger()
	rect = QApplication.desktop().availableGeometry()
	form.resize(rect.size())
	form.setWindowIcon(QIcon(":/icon.png"))
	form.show()
	app.exec_()
