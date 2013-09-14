#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#回放GraphicsView定义

#改掉pos property的setter使得corX一起变
#动画等特效部分,没完成
from myHumanReplay import *
import sys,copy
from myGetRoute import *
class REPLAYERROR(Exception):
	def __init__(self, value = ""):
		self.value = value

	def __str__(self):
		return self.value
#MCE_Type = QEvent.registerEventType()
#KCE_Type = QEvent.registerEventType()

#class MouseCommEvent(QEvent):
#	def __init__(self, pos):
#		super(MouseCommEvent, self).__init__(MCE_Type)
#		self.pos = pos
#class KeyCommEvent(QEvent):
#	def __init(self, key):
#		super(KeyCommEvent, self).__init__(KCE_Type)

#class MoveTransition(QAbstractTransition):
#	def __init__(self, source = None):
#		super(MoveTransition, self).__init__(source)

#   def eventTest(self, event):
#		if not isinstance(event, MouseCommEvent):
#			return
		
class HumanReplay(QGraphicsView):
	commBeg = pyqtSignal()
	moveFinished = pyqtSignal()
	lastAgain = pyqtSignal()
	oprFinished = pyqtSignal()
	endGame = pyqtSignal()
	commandFinished = pyqtSignal()
	moveAnimEnd = pyqtSignal()
	def __init__(self, scene, parent = None):
		super(HumanReplay, self).__init__(parent)

		self.scene = scene
		self.setScene(self.scene)
		self.run = False
		self.animation = None
		self.setMouseTracking(True)
		#游戏记录变量
		self.iniMapInfo = None
		self.latestStatus = 1
		self.latestRound = 0
		self.nowMoveUnit = None
		self.now_state = None
		#命令变量
		self.command = None
		self.moveToPos = None
		self.Operation = None
		#临时命令展示信息
		self.route_ind_list = []
		self.move_range_list = []
		self.attack_range_list = []
		self.tmp_route_list = []
		self.tmp_move_list = []
		self.tmp_attack_list = []

		self.animationItem = []
		#储存展示信息
		self.UnitBase = [[],[]]
		self.MapList=[]
		self.mapChangeInfo = []

		#储存游戏信息
		self.command_list = []
		self.gameBegInfo = []
		self.gameEndInfo = []
		#鼠标选定单位
		self.focusUnit = MouseFocusUnit(0, 0)
		self.scene.addItem(self.focusUnit)

		self.focusUnit.setVisible(False)

		self.mouseUnit = MouseIndUnit(0, 0)
		self.mouseUnit.setVis(False)
		self.mouseUnit.setVisible(False)
		self.scene.addItem(self.mouseUnit)
		self.mouseUnit.setPos(0,0)
		self.setCursor(QCursor(QPixmap(":normal_cursor.png"),0,0))
		#状态机定义与连接
		self.stateMachine = QStateMachine(self)
		self.State_Run = QState(self.stateMachine)
		self.State_No_Comm = QState(self.State_Run)
		self.State_Comm = QState(self.State_Run)
		self.State_Move = QState(self.State_Comm)
		self.State_Opr = QState(self.State_Comm)
		self.State_Target = QState(self.State_Comm)
		self.stateMachine.setInitialState(self.State_Run)
		self.State_Run.setInitialState(self.State_No_Comm)
		self.State_Comm.setInitialState(self.State_Move)
		self.State_Final = QFinalState(self.stateMachine)

		self.stateList = [self.State_No_Comm, self.State_Move, self.State_Opr, self.State_Target]

		self.State_No_Comm.addTransition(self, SIGNAL("commBeg()"), self.State_Move)
		self.State_Move.addTransition(self, SIGNAL("moveFinished()"), self.State_Opr)
		self.State_Opr.addTransition(self, SIGNAL("lastAgain()"), self.State_Move)
		self.State_Target.addTransition(self, SIGNAL("lastAgain()"), self.State_Opr)
		self.State_Opr.addTransition(self, SIGNAL("oprFinished()"), self.State_Target)
		self.State_Comm.addTransition(self, SIGNAL("commandFinished()"), self.State_No_Comm)
		self.State_Run.addTransition(self, SIGNAL("endGame()"), self.State_Final)

		for state in self.stateList:
			self.connect(state, SIGNAL("entered()"), self.on_Entered)
		self.connect(self.State_Target, SIGNAL("exited()"), self.on_Exited)
#		self.stateMachine.start()
	#begin to get command
	def GetCommand(self):
#		QTimer.singleShot(0, self, SLOT("getCommand()"))
#	@pyqtSlot()
#	def getCommand(self):
		self.nowMoveUnit = self.UnitBase[self.gameBegInfo[-1].id[0]][self.gameBegInfo[-1].id[1]]
#		self.commBeg.emit()
		print "emit,get command getget~~~~~~~~~~~~~~"
		QTimer.singleShot(0, self, SIGNAL("commBeg()"))

	#event handlers
	def mouseMoveEvent(self, event):
		if not self.run:
			QGraphicsView.mouseMoveEvent(self, event)
			return
		pos = event.pos()
		if not self.mouseUnit.isVisible():
			self.mouseUnit.setVisible(True)
		item = self.itemAt(pos)
		if not item:
			return
		if self.mouseUnit.corX == item.corX and self.mouseUnit.corY == item.corY:
			return
		self.mouseUnit.setPos(item.corX, item.corY)

	def mousePressEvent(self, event):
		if not self.run:
			QGraphicsView.mousePressEvent(self, event)
			return

			
		pos = event.pos()
		item = self.itemAt(pos)
		items = self.items(pos)
		if not item:
			return
		#右键发出信息,不设置focus
		if event.button() == Qt.RightButton:
			for it in items:
				if isinstance(it, SoldierUnit):
					self.emit(SIGNAL("unitSelected"),it.obj)
					print "emit unit", it.obj.kind
				elif isinstance(it, MapUnit):
					self.emit(SIGNAL("mapSelected"), it.obj)
					print "emit map", it.obj.kind
			return
		#还没有做发出展示信号的部分
		if not self.focusUnit.isVisible():
			self.focusUnit.setVisible(True)

		if self.focusUnit in items:
			return

		if not self.now_state == self.State_Move:
			self.focusUnit.setPos(item.corX, item.corY)
		if self.now_state == self.State_No_Comm or self.now_state == self.State_Opr:
			return
		if self.now_state == self.State_Move:

			if (item.corX, item.corY) not in self.move_range_list:
				return
			self.moveToPos = (item.corX, item.corY)
			self.moveFinished.emit()
			return
		if self.now_state == self.State_Target:
			if (item.corX, item.corY) not in self.attack_range_list:
				return
			for item in self.items(pos):
				if isinstance(item, SoldierUnit):
					self.command = basic.Command(self.Operation, self.moveToPos, item.idNum)
					self.emit(SIGNAL("commandFinished"), self.command)
					self.commandFinished.emit()
					self.command_list.append(self.command)

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			if self.now_state == self.State_Opr or self.State_Target:
				print "lastAgain"
				self.lastAgain.emit()
		if self.now_state != self.State_Opr:
			return
		#攻击
		if event.key() == Qt.Key_A:
			self.Operation = 1
			self.oprFinished.emit()
		#skill
		elif event.key() == Qt.Key_S:
			#判断该单位是否可以使用skill
			self.Operation = 2
			self.oprFinished.emit()
		#待机
		elif event.key() == Qt.Key_D:
			self.command = basic.Command(0, self.moveToPos, None)
			self.command_list.append(self.command)
			self.emit(SIGNAL("commandFinished"), self.command)
			self.commandFinished.emit()
	#展示便于用户下达命令的信息
	def on_Entered(self):
		now_state = self.sender()
		print now_state
		if not isinstance(now_state, QState):
			return
		self.now_state = now_state
		self.resetToPlay()

		if now_state == self.State_No_Comm:
			self.Operation = self.moveToPoint = self.command = None
		elif now_state == self.State_Move:
			print "move state"
			if isinstance(self.nowMoveUnit, SoldierUnit):
				self.focusUnit.setPos(self.nowMoveUnit.corX, self.nowMoveUnit.corY)
				self.move_range_list = getMoveArrange(self.getMap(self.latestRound,0), self.gameBegInfo[-1].base, self.gameBegInfo[-1].id)
				self.drawArrange(self.move_range_list,self.tmp_move_list)
				#setCursor
		elif now_state == self.State_Opr:
			if isinstance(self.nowMoveUnit, SoldierUnit):
				self.route_ind_list = GetRoute(self.getMap(self.latestRound, 0), self.gameBegInfo[-1].base, self.gameBegInfo[-1].id,self.moveToPos)
				self.drawRoute(self.route_ind_list,self.tmp_route_list)
		elif now_state == self.State_Target:
			if self.Operation == 1:
				self.setCursor(QCursor(QPixmap(":attack_cursor.png"),0,0))
				self.attack_range_list = getAttackRange(self.gameBegInfo[-1].base, self.gameBegInfo[-1].id, self.moveToPos)
				self.drawArrange(self.attack_range_list,self.tmp_attack_list)
			elif self.Operation == 2:
				self.setCursor(QCursor(QPixmap(":skill_cursor.png"),0,0))
				#not completed
#				self.
#			elif self.Operation == "N":
#				self.emit("commandComplete")

	def on_Exited(self):
		self.setCursor(QCursor(QPixmap(":normal_cursor.png"),0,0))

	def drawArrange(self, arrange_list,list_):
		for pos in arrange_list:
			ind_unit = ArrangeIndUnit(pos[0], pos[1])
			self.scene.addItem(ind_unit)
			ind_unit.setPos(pos[0],pos[1])
			list_.append(ind_unit)
			print pos
	def drawRoute(self, route_list, list_, vis = True):
		for pos in route_list:
			ind_unit = RouteIndUnit(pos[0], pos[1])
			self.scene.addItem(ind_unit)
			ind_unit.setPos(pos[0],pos[1])
			if not vis:
				ind_unit.setVisible(False)
			list_.append(ind_unit)
			
	#得到指定回合的地图,通过每回合mapchange计算
	def getMap(self, round_, status):
		map_ = copy.copy(self.iniMapInfo)
		for i in range(round_):
			if self.mapChangeInfo[i]:
				for change in self.mapChangeInfo[i]:
					map_[change[1][1]][change[1][0]] = basic.Map_Basic(change[0])
		if status:
			change = self.mapChangeInfo[round_]
			map_[change[1][1]][change[1][0]] = basic.Map_Basic(change[0])
		return map_

	def setMap(self, map_):
		self.resetMap()
		self.width = len(map_[0])
		self.height = len(map_)
		for i in range(self.height):
			for j in range(self.width):
				new_map = MapUnit(j,i,map_[i][j])
				self.scene.addItem(new_map)
				new_map.setPos(j,i)
				self.MapList.append(new_map)

	def setSoldier(self, units):
		self.resetUnit()
		for i in range(2):
			for j in range(len(units[i])):
				new_unit = SoldierUnit(units[i][j],(i,j))
				self.scene.addItem(new_unit)
				new_unit.setPos(new_unit.corX, new_unit.corY)
				self.UnitBase[i].append(new_unit)
		print "unitbase",len(self.UnitBase)#for test

	def Initialize(self, begInfo,frInfo):
		self.setMap(begInfo.map)
		self.iniMapInfo = begInfo.map
		self.setSoldier(begInfo.base)
		self.latestStatus = 0
		self.gameBegInfo.append(frInfo)
		self.run = True
		self.mouseUnit.setVis(True)
		if not self.stateMachine.isRunning():
			self.stateMachine.start()

	def UpdateBeginData(self, rbInfo):
		self.gameBegInfo.append(rbInfo)
		self.latestStatus = 0
		self.latestRound += 1

	def UpdateEndData(self, comInfo, reInfo):
		self.gameEndInfo.append((comInfo, reInfo))
		self.latestStatus = 1
		self.mapChangeInfo.append(reInfo.change)
#		if reInfo.change:
#			map_item = self.scene.items(GetPos(change[1][0], change[1][1]))[-1]
#			map_item.obj = Map_Basic(change[0])
#			map_item.update()
#			map_list
	#从当前回合开始播放至这一回合结束
	def TerminateAni(self):
		if self.animation:
			self.animation.stop()
			self.animation.deleteLater()
			self.animation = None
		for item in self.animationItem:
			self.scene.removeItem(item)
		self.animationItem = []

	def moveAnimation(self, move_unit, move_pos):
		TIME_PER_GRID = 800
		
		route = self.gameEndInfo[self.nowRound][1].route
		#GetRoute(self.getMap(self.nowRound,0),self.gameBegInfo[self.nowRound].base,move_unit.idNum,move_pos)
		
		steps = len(route) - 1
#		items = []

		movAnim = QPropertyAnimation(move_unit, "pos")
		movAnim.setDuration(steps * TIME_PER_GRID)
		movAnim.setStartValue(GetPos(move_unit.obj.position[0], move_unit.obj.position[1]))
		if steps:			
			for i in range(steps + 1):
				pos = GetPos(route[i][0], route[i][1])
				movAnim.setKeyValueAt(float(i)/steps, pos)
		print route
		if route:
			movAnim.setEndValue(GetPos(route[-1][0],route[-1][1]))
		else:
			movAnim.setEndValue(GetPos(move_unit.obj.position[0], move_unit.obj.position[1]))
		return movAnim, []

	def attackAnimation(self, move_unit,move_pos, attack_target, effect):
		ATTACK_TIME = 1500
		TOTAL_TIME = 2000

		if effect == -1:#超出范围或未攻击(已死亡)
			return QPauseAnimation(500), []
		print "attack kindlalala", move_unit.obj.kind
		attackInd = AttackIndUnit(move_pos[0], move_pos[1],":attack_ind1.png")# %move_unit.obj.kind)
		attackInd.setVisible(False)
		targetInd = TargetIndUnit(self.UnitBase[attack_target[0]][attack_target[1]].corX,self.UnitBase[attack_target[0]][attack_target[1]].corY)
	#	targetInd.setVisible(False) 
		sound = QSound(":attack_sound.wav")

		self.scene.addItem(attackInd)
		self.scene.addItem(targetInd)
		attackInd.setPos(attackInd.corX, attackInd.corY)
		targetInd.setPos(targetInd.corX, targetInd.corY)

		showAtkAnim = QParallelAnimationGroup()
		ani = QPropertyAnimation(attackInd, "pos")
		ani.setStartValue(GetPos(attackInd.corX,attackInd.corY))
		ani.setDuration(ATTACK_TIME)
		ani.setEndValue(GetPos(targetInd.corX, targetInd.corY))
		self.connect(ani, SIGNAL("finished()"), sound, SLOT("play()"))
		showAtkAnim.addAnimation(ani)

		ani = QPropertyAnimation(attackInd, "opacity")
		ani.setDuration(TOTAL_TIME)
		ani.setStartValue(1)
		ani.setKeyValueAt(0.8, 0.9)
		ani.setKeyValueAt(0.9, 0.8)
		ani.setEndValue(0)
		showAtkAnim.addAnimation(ani)

		ani = QPropertyAnimation(targetInd, "opacity")
		ani.setDuration(TOTAL_TIME)
		ani.setStartValue(1)
		ani.setKeyValueAt(0.99, 1)
#		ani.setKeyValueAt(1, 1)
		ani.setEndValue(0)
		showAtkAnim.addAnimation(ani)
		#攻击效果展示

		if effect:
			label = EffectIndUnit("- %d" %(self.gameEndInfo[self.nowRound][1].base[attack_target[0]][attack_target[1]].life -\
											self.gameBegInfo[self.nowRound].base[attack_target[0]][attack_target[1]].life)
								  )
		else:
			label = EffectIndUnit("Miss")
		label.setVisible(False)
		self.scene.addItem(label)
		label.setPos(GetPos(targetInd.corX, targetInd.corY)+QPointF(0,-20))
		ani = QPropertyAnimation(label, "opacity")
		ani.setDuration(TOTAL_TIME)
		ani.setStartValue(1)
		ani.setEndValue(0)

		showAtkAnim.addAnimation(ani)
		ani = QPropertyAnimation(label, "pos")
		ani.setDuration(TOTAL_TIME)
		ani.setStartValue(label.pos())
		ani.setEndValue(label.pos() + QPointF(0,-20))
		ani.setEasingCurve(QEasingCurve.OutCubic)
		item = [attackInd, targetInd, label]
		return showAtkAnim, item


	def dieAnimation(self, die_unit):
		TOTAL_TIME = 2000

		unit = self.UnitBase[die_unit[0]][die_unit[1]]
		die_e = QGraphicsBlurEffect(self)
		die_e.setBlurRadius(0.2)
		unit.setGraphicsEffect(die_e)

		dieInd = DieIndUnit()
		self.scene.addItem(dieInd)
		dieInd.setPos(unit.corX, unit.corY)

		dieAnim = QParallelAnimationGroup()
		dieAni = QPropertyAnimation(unit, "opacity")
		dieAni.setDuration(TOTAL_TIME)
		dieAni.setStartValue(1)
		dieAni.setEndValue(0)
		dieAnim.addAnimation(dieAni)
		dieAni1 = QPropertyAnimation(dieInd, "opacity")
		dieAni1.setDuration(TOTAL_TIME)
		dieAni1.setStartValue(1)
		dieAni1.setKeyValueAt(0.2, 0.3)
		dieAni1.setKeyValueAt(0.4, 0.8)
		dieAni1.setKeyValueAt(0.7, 0.2)
		dieAni1.setKeyValueAt(0.9, 0.6)
		dieAni1.setEndValue(0)
		dieAnim.addAnimation(dieAni1)

		return dieAnim, [dieInd]

	def Play(self):
		#回合末没有动画,先调转再调用
		if self.nowStatus:
			return
		#还没有更新完
		if len(self.gameEndInfo) < self.nowRound + 1:
			return
		self.TerminateAni()
		unit_id = self.gameBegInfo[self.nowRound].id
		unit_move = self.UnitBase[unit_id[0]][unit_id[1]]
		cmd = self.gameEndInfo[self.nowRound][0]
		endInfo = self.gameEndInfo[self.nowRound][1]

		self.animation = QSequentialAnimationGroup()

		#移动动画
		ani, item = self.moveAnimation(unit_move, cmd.move)
		self.animation.addAnimation(ani)
		self.animationItem.extend(item)
		#attack
		if cmd.order == 1:
			ani, item = self.attackAnimation(unit_move, cmd.move,cmd.target, endInfo.effect[0])
			self.animationItem.extend(item)
			self.animation.addAnimation(ani)
			print "add animation"
			#target die
			if endInfo.base[cmd.target[0]][cmd.target[1]].life == 0:
				anim, item = self.dieAnimation(cmd.target)
				self.animationItem.extend(item)
				self.animation.addAnimation(anim)
#			elif endInfo.effect[1] != -1:
			#fight back
			anim, item = self.attackAnimation(self.UnitBase[cmd.target[0]][cmd.target[1]], (self.UnitBase[cmd.target[0]][cmd.target[1]].corX,\
																								self.UnitBase[cmd.target[0]][cmd.target[1]].corY),
												  unit_move.idNum, endInfo.effect[1])
			self.animationItem.extend(item)
			if endInfo.base[unit_id[0]][unit_id[1]].life == 0:
				anim, item = self.dieAnimation(unit_id)
				self.animation.extend(item)
				self.animation.addAnimation(anim)
		#skill
		elif cmd.order == 2:
			pass
		#待机只暂停1秒
		self.animation.addAnimation(QPauseAnimation(1000))
#		self.drawRoute(route, self.animationItem)
		self.connect(self.animation, SIGNAL("finished()"), self.moveAnimEnd)
		self.connect(self.animation, SIGNAL("finished()"), self.animation, SLOT("deleteLater()"))
		self.connect(self.animation, SIGNAL("finished()"), self.text__)

		self.animation.start()
		#skill
	#展示round_, status的场面
	def text__(self):
		self.animation = None
	def GoToRound(self, round_, status):

		self.TerminateAni()
		if round_ * 2 + status > self.latestRound * 2 + self.latestStatus:
			raise REPLAYERROR("not update to that status")

		self.nowRound = round_
		self.nowStatus = status

		self.setMap(self.getMap(round_, status))

		if status:
			self.setSoldier(self.gameEndInfo[round_][1].base)
		else:
			print "round:",round_,self.gameBegInfo[round_]
			self.setSoldier(self.gameBegInfo[round_].base)

	def resetMap(self):
		for item in self.MapList:
			self.scene.removeItem(item)

		self.MapList = []
	def resetUnit(self):
		for item in self.UnitBase[0]:
			self.scene.removeItem(item)
		for item in self.UnitBase[1]:
			self.scene.removeItem(item)
		self.UnitBase = [[],[]]

	#去掉临时方便用户命令的信息展示
	def resetToPlay(self):
		for item in self.tmp_move_list:
			self.scene.removeItem(item)
		self.move_range_list = []
		self.tmp_move_list = []
		for item in self.tmp_attack_list:
			self.scene.removeItem(item)
		self.attack_range_list = []
		self.tmp_attack_list = []
		for item in self.tmp_route_list:
			self.scene.removeItem(item)
		self.route_ind_list = []
		self.tmp_route_list = []

	#供结束游戏时的完全清理,需要保存录像请在此之前提取游戏信息
	def reset(self):
		self.emit(SIGNAL("endGame()"))
		self.resetToPlay()
		self.route_ind_list = []
		self.move_range_list = []
		self.attack_range_list = []

		self.resetUnit()
		self.resetMap()
		self.mapChangeInfo = []

		self.command_list = []
		self.gameBegInfo = []
		self.gameEndInfo = []

		self.now_state = self.nowMoveUnit = self.command = self.moveToPos = self.Operation = self.iniMapInfo = None
		self.latestStatus = 1
		self.latestRound = 0
		self.run = False
		self.mouseUnit.setVis(False)
#test
if __name__ == "__main__":
	app = QApplication(sys.argv)
	scene = QGraphicsScene()
	form = HumanReplay(scene)
	form.show()
	m = basic.Map_Basic
	map_ = [[m(0), m(0), m(1), m(2), m(0), m(0)],
			[m(0), m(1), m(0), m(0), m(1), m(0)],
			[m(2), m(2), m(0), m(0), m(1), m(0)]]
	u = basic.Base_Unit
	units = [[u(0,(0,0)), u(1,(0,2))],
			 [u(0,(3,1)), u(1,(2,0))]]
	form.Initialize(map_, basic.Begin_Info(map_,units,((6,6),(6,6))),basic.Round_Begin_Info((0,1),0,units,0))
	form.GetCom()
	app.exec_()
