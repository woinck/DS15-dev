#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#AI debugger for watching two ai fighting

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import AI_debugger.qrc_resource
from AI_debugger.info_widget import *
#from Ai_Thread import *
from AI_debugger.AI_2DReplayWidget import *
import basic, sio, os, socket

DEBUG_MODE = 1
DEFAULT_SCILENT_AI = os.getcwd() + "\\sclientai.py"#默认的ai路径,待设置
DEFAULT_MAP = os.getcwd() + "\\new_map.map"
#WaitForNext = QWaitCondition()
#WaitForPause = QWaitCondition()

class AiThread(QThread):
	def __init__(self, parent = None):
		super(AiThread, self).__init__(parent)

		self.mutex = QMutex()
		self.closed = False#close标识以便强制关闭线程

	#每次开始游戏时，用ai路径和地图路径调用initialize以开始一个新的游戏
	def initialize(self, gameAIPath, gameMapPath):
		
		if not sio.DEBUG_MODE:
			server_run = sio.Prog_Run(os.getcwd() + sio.SERV_FILE_NAME)
			server_run.start()
		
		self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			self.conn.connect((sio.HOST,sio.UI_PORT))
		except exception:
			self.conn.close()
			raise exception
		else:
			self.gameMapPath = gameMapPath
			self.gameAIPath = gameAIPath

	def isClosed(self):
		try:
			self.mutex.lock()
			return self.closed
		finally:
			self.mutex.unlock()
	def close(self):
		try:
			self.mutex.lock()
			self.closed = True
		finally:
			self.mutex.unlock()
	def run(self):
		sio._sends(self.conn,(sio.AI_VS_AI, self.gameMapPath, self.gameAIPath))
		'''
		if gameMode == sio.PLAYER_VS_PLAYER or gameMode == sio.PLAYER_VS_AI:
			conn.recv(1)
			cpu_0 = UI_Player(0)
			cpu_0.start()
			if gameMode == sio.PLAYER_VS_PLAYER:
				conn.recv(1)
				cpu_1 = UI_Player(1)
				cpu_1.start()
		'''	
		(mapInfo,baseInfo,aiInfo) = sio._recvs(self.conn)#add base info
		frInfo = sio._recvs(self.conn)
		self.emit(SIGNAL("firstRecv"),mapInfo, frInfo, aiInfo, baseInfo)

		rCommand, reInfo = sio._recvs(self.conn)
		print "over",reInfo.over
		self.emit(SIGNAL("reRecv"), rCommand, reInfo)
		while not reInfo.over and not self.isClosed():
			rbInfo = sio._recvs(self.conn)
			if self.isClosed():
				break
			self.emit(SIGNAL("rbRecv"),rbInfo)
			(rCommand,reInfo) = sio._recvs(self.conn)
			print reInfo.over
			if self.isClosed():
				break
			self.emit(SIGNAL("reRecv"),rCommand, reInfo)
			print "one round!"
		if not self.isClosed():
			winner = sio._recvs(self.conn)
			self.emit(SIGNAL("gameWinner"),winner)
			print winner
		
		#	是否存储回放文件
			replay_mode = False
			sio._sends(self.conn,replay_mode)
		
		self.conn.close()


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
		self.infoDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|
											Qt.RightDockWidgetArea)
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
											"start game")
		self.gameEndAction = self.createAction("&End", self.endGame,
										 "Ctrl+E","gameEnd",
										 "end game")
		self.gameLoadAction1 = self.createAction("Load &AI", self.loadAIdlg,
										  "Ctrl+A", "loadAI",
										  "load AI")
		self.gameLoadAction2 = self.createAction("Load &MAP", self.loadMapdlg,
										   "Ctrl+M", "loadMap",
										   "load MAP")
		self.gameUnloadAction = self.createAction("Unload Ais", self.unloadAI,
												  tip = "unload Ais")
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
		self.configMenu.addAction(resetAction)


		#creat action and add it to window menu
		self.dockAction = self.createAction("(dis/en)able infos", self.setInfoWidget,
									   tip = "enable/disable info dock-widget",
									   checkable = True,
									   signal = "toggled(bool)")
		self.windowMenu = self.menuBar().addMenu("&Window")
		self.windowMenu.addAction(self.dockAction)
		self.dockAction.setChecked(True)
		#creat toolbars and add actions

		gameToolbar =  self.addToolBar("Game")
		self.addActions(gameToolbar, (self.gameStartAction,
								  self.gameEndAction, self.gameLoadAction1, self.gameLoadAction2))


		self.connect(self.infoWidget, SIGNAL("hided()"), self.synhide)
		#to show messages
		self.connect(self.replayWindow.replayWidget, SIGNAL("unitSelected"),
					 self.infoWidget.newUnitInfo)
		self.connect(self.replayWindow.replayWidget, SIGNAL("mapGridSelected"),
					 self.infoWidget.newMapInfo)
		#进度条到主界面的通信
		self.connect(self.replayWindow, SIGNAL("goToRound(int, int)"), self.on_goToRound)



		self.updateUi()
		self.setWindowTitle("DS15_AIDebugger")


	#wrapper function for reducing codes
	def createAction(self, text, slot=None, shortcut=None, icon=None,
					 tip=None, checkable=False, signal="triggered()"):
		action = QAction(text, self)
		if icon is not None:
			action.setIcon(QIcon(":/%s.png" % icon))
		if shortcut is not None:
			action.setShortcut(shortcut)
		if tip is not None:
			action.setToolTip(tip)
			action.setStatusTip(tip)
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
#		if len(self.loaded_ai) != 0 and self.loaded_map:
#			if not self.started:
#				self.gameStartAction.setEnabled(True)
#				self.gameEndAction.setEnabled(False)
#				self.gameLoadAction1.setEnabled(True)
#				self.gameLoadAction2.setEnabled(True)
#			else:
#				self.gameStartAction.setEnabled(False)
#				self.gameEndAction.setEnabled(True)
#				self.gameLoadAction1.setEnabled(False)
#				self.gameLoadAction2.setEnabled(False)
#		else:
#			self.gameStartAction.setEnabled(False)
#			self.gameEndAction.setEnabled(False)
#			self.gameLoadAction1.setEnabled(True)
#			self.gameLoadAction2.setEnabled(True)
		pass	
	#game operation slot
	def startGame(self):
		if not self.loaded_ai:
			self.loaded_ai.append(DEFAULT_SCILENT_AI)
			self.loaded_ai.append(DEFAULT_SCILENT_AI)
		if len(self.loaded_ai) == 1:
		 #加入默认的什么都不做ai
			self.loaded_ai.append(DEFAULT_SCILENT_AI)
		#开始这个线程开始交互
		if not self.loaded_map:
			self.loaded_map = DEFAULT_MAP
		self.pltThread = AiThread(self)
		try:
			self.pltThread.initialize(self.loaded_ai,self.loaded_map)
		except:
			QMessageBox.critical(self, "Connection Error",
								 "Failed to connect to UI_PORT\n",
								 QMessageBox.Ok, QMessageBox.NoButton)
			self.pltThread.deleteLater()
		else:
			self.connect(self.pltThread, SIGNAL("firstRecv"), self.on_firstRecv)
			self.connect(self.pltThread, SIGNAL("rbRecv"), self.on_rbRecv)
			self.connect(self.pltThread, SIGNAL("reRecv"), self.on_reRecv)
			self.connect(self.pltThread, SIGNAL("gameWinner"), self.on_gameWinner)
			self.connect(self.pltThread, SIGNAL("finished()"), self.replayWindow.updateUI)
			self.connect(self.pltThread, SIGNAL("finished()"), self.deletePlt)

			self.started = True
			self.replayWindow.started = True
			self.replayWindow.updateUI()
			self.updateUi()

			self.pltThread.start()

	def deletePlt(self):
		self.pltThread.deleteLater()
		self.pltThread = None

	def endGame(self):
		#清空游戏缓存数据
		#强制在游戏没有进行到胜利条件的时候结束游戏
		if self.pltThread:
			self.pltThread.close()
			self.pltThread.wait()
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
		dir = QDir.toNativeSeparators(r"./FileAI")
		fname = unicode(QFileDialog.getOpenFileName(self,
													"load AI File", dir,
													"AI files (%s)" % "*.py"))
		if len(self.loaded_ai) < 2 and fname:
			self.loaded_ai.append(fname)
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

	def on_firstRecv(self, mapInfo, frInfo, aiInfo, baseInfo):
		print "fisrtRecv"
		self.replayWindow.updateIni(basic.Begin_Info(mapInfo, baseInfo), frInfo)
		self.infoWidget.beginRoundInfo(frInfo)
		#这个aiInfo是什么...
		self.gameBegInfo.append(frInfo)

	def on_rbRecv(self, rbInfo):
		self.replayWindow.updateBeg(rbInfo)
		self.gameBegInfo.append(rbInfo)

	def on_reRecv(self, rCommand, reInfo):
		self.replayWindow.updateEnd(rCommand, reInfo)
		self.gameEndInfo.append((rCommand,reInfo))

	#进度条跳转回合信息同步
	def on_goToRound(self, round_, status):
		self.infoWidget.beginRoundInfo(self.gameBegInfo[round_-1])
		if len(self.gameEndInfo) >= round_:
			self.infoWidget.endRoundInfo(*self.gameEndInfo[round_-1])

	#胜利展示
	def on_gameWinner(self, winner):
		QMessageBox.information(self, "Game Winner", "player %s win the game" %winner)
		#需要其他特效再加

	def reset(self):
		pass
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
