#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#回放GraphicsView定义

#改掉pos property的setter使得corX一起变
#动画等特效部分,没完成
DEBUGGER_USE = 0
from myHumanReplay import *
import sys,copy,time
import main
from functools import partial
from myGetRoute import getAttackRange
class REPLAYERROR(Exception):
	def __init__(self, value = ""):
		self.value = value

	def __str__(self):
		return self.value

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

		#设置透明
		self.setStyleSheet("background: transparent; border:0px")
		self.scene = scene
		self.setScene(self.scene)
		self.run = False
		self.animation = None
		self.setMouseTracking(True)
		#游戏记录变量
		self.nowRound = 0
		self.nowStatus = 0
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

		self.gameBegInfo = []
		self.gameEndInfo = []
		#鼠标选定单位
		self.focusUnit = MouseFocusUnit(0, 0)
		self.scene.addItem(self.focusUnit)
		#self.animation = QSequentialAnimationGroup()#debugging
		self.focusUnit.setVisible(False)

		self.mouseUnit = MouseIndUnit(0, 0)
		self.mouseUnit.setVis(False)
		self.mouseUnit.setVisible(False)
		self.scene.addItem(self.mouseUnit)
		self.mouseUnit.setPos(0,0)
		self.setCursor(QCursor(QPixmap(":normal_cursor.png").scaled(30,30),0,0))
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
		self.connect(self.State_Comm, SIGNAL("exited()"), self.on_Exited)

	#begin to get command
	def GetCommand(self):
		if not self.run:
			return
		self.nowMoveUnit = self.UnitBase[self.gameBegInfo[-1].id[0]][self.gameBegInfo[-1].id[1]]
		#等待state已进入初始状态(started并已entered)
		QTimer.singleShot(0, self, SIGNAL("commBeg()"))
		self.nowMoveUnit.setNowMove(True)

	#event handlers
	def mouseMoveEvent(self, event):
		if not self.run:
			QGraphicsView.mouseMoveEvent(self, event)
			return
		pos = event.pos()
		#让move的时候保持显现状态
		if not self.mouseUnit.isVisible():
			self.mouseUnit.setVisible(True)
		items = self.items(pos)
		if not items:
			return
		item = items[-1]
		if isinstance(item, EffectIndUnit):
			if len(items) == 1:
				return
			item = items[0]
		if self.mouseUnit.corX == item.corX and self.mouseUnit.corY == item.corY:
			return
		self.mouseUnit.setPos(item.corX, item.corY)

	def mousePressEvent(self, event):
		if not self.run:
			QGraphicsView.mousePressEvent(self, event)
			return

		pos = event.pos()
		items = self.items(pos)
		if not items:
			return
		#右键发出信息,但不设置focus
		flag = False
		for it in items:
			if isinstance(it, SoldierUnit):
				self.emit(SIGNAL("unitSelected"),it.obj)
			elif isinstance(it, MapUnit):
				self.emit(SIGNAL("mapSelected"), it.obj)
				item = it
				flag = True
		if event.button() == Qt.RightButton:
			return
		if not flag:
			return
		if not self.focusUnit.isVisible():
			self.focusUnit.setVisible(True)


		if not self.now_state == self.State_Move:
			self.focusUnit.setPos(item.corX, item.corY)
		if self.now_state == self.State_No_Comm or self.now_state == self.State_Opr:
			return
		if self.now_state == self.State_Move:
			if (item.corX, item.corY) not in self.move_range_list:
				return
			self.moveToPos = (item.corX, item.corY)

			#在这里判断mirror传递是否会成功，并根据mirror传递是否成功画出route和攻击范围
			if item.obj.kind == basic.MIRROR:
				self.transPoint = item.obj.out
				flag = False
				for i in range(2):
					if flag == True:
						break
					for it in self.UnitBase[i]:
						if it.scene() == self.scene and it.obj.position == self.transPoint:
							self.transPoint = None
							flag = True
							break
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


	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			if self.now_state == self.State_Opr or self.State_Target:
				self.lastAgain.emit()
		if self.now_state != self.State_Opr:
			return
		#攻击
		if event.key() == Qt.Key_A:
			if self.nowMoveUnit.obj.kind == basic.WIZARD:
				self.emit(SIGNAL("errorOperation"), QString.fromUtf8("法师不能攻击,请选择其他命令s或d"))
				return
			self.Operation = 1
			self.oprFinished.emit()
		#skill
		elif event.key() == Qt.Key_S:
			if self.nowMoveUnit.obj.kind < 5 or self.nowMoveUnit.obj.kind == 7:
				self.emit(SIGNAL("errorOperation"), QString.fromUtf8("此单位不能使用技能，请选择其他命令a或d"))
				return
			self.Operation = 2
			self.oprFinished.emit()
		#待机
		elif event.key() == Qt.Key_D:
			self.command = basic.Command(0, self.moveToPos, None)
			self.emit(SIGNAL("commandFinished"), self.command)
			self.commandFinished.emit()
	#展示便于用户下达命令的信息
	def on_Entered(self):
		now_state = self.sender()
		if not isinstance(now_state, QState):
			return
		self.now_state = now_state
		self.resetToPlay()

		if now_state == self.State_No_Comm:
			self.Operation = self.moveToPos = self.command = None
		elif now_state == self.State_Move:
			if isinstance(self.nowMoveUnit, SoldierUnit):
				self.setCursor(QCursor(QPixmap(":normal_cursor.png").scaled(30,30),0,0))
				self.transPoint = None
				self.focusUnit.setVisible(True)
				self.focusUnit.setPos(self.nowMoveUnit.corX, self.nowMoveUnit.corY)
				self.move_range_list = self.gameBegInfo[self.latestRound].range
				self.drawArrange(self.move_range_list,self.tmp_move_list)
				#setCursor
		elif now_state == self.State_Opr:
			if isinstance(self.nowMoveUnit, SoldierUnit):
				self.route_ind_list = main.available_spots(self.getMap(self.latestRound, 0), self.gameBegInfo[-1].base, self.gameBegInfo[-1].id,self.moveToPos)#改成逻辑的函数
				if not self.route_ind_list:
					self.route_ind_list = [self.nowMoveUnit.obj.position]
				#print "route_int_list:::::::::::", self.route_ind_list#for test
				self.drawRoute(self.route_ind_list,self.tmp_route_list)
				#镜子
				if self.transPoint:
					#self.moveToPos = self.transPoint
					self.drawRoute([self.transPoint], self.tmp_route_list)
		elif now_state == self.State_Target:
			if self.Operation == 1:
				self.setCursor(QCursor(QPixmap(":attack_cursor.png").scaled(30,30),0,0))
				tmp_point = self.transPoint if self.transPoint else self.moveToPos#debugging
				turret_flag = self.nowMoveUnit.obj.kind == basic.ARCHER and self.iniMapInfo[tmp_point[0]][tmp_point[1]].kind == basic.TURRET
				self.attack_range_list = getAttackRange(self.gameBegInfo[-1].base, self.gameBegInfo[-1].id, tmp_point, turret_flag)
				if not self.attack_range_list:
					self.emit(SIGNAL("errorOperation"), QString.fromUtf8("没有可攻击的对象,esc可返回上一阶段"))
				self.drawArrange(self.attack_range_list,self.tmp_attack_list)
			elif self.Operation == 2:
				self.setCursor(QCursor(QPixmap(":skill_cursor.png").scaled(30,30),0,0))
				poses = [x.obj.position for x in self.UnitBase[self.nowMoveUnit.idNum[0]] if x.scene() == self.scene]
				if not poses:
					self.emit(SIGNAL("errorOperation"), QString.fromUtf8("没有可施用技能的对象,esc可返回上一阶段"))
				self.attack_range_list = poses
				self.drawArrange(poses, self.tmp_attack_list)


	def on_Exited(self):
		self.setCursor(QCursor(QPixmap(":normal_cursor.png").scaled(30,30),0,0))
		self.nowMoveUnit.setNowMove(False)

	def drawArrange(self, arrange_list,list_):
		for pos in arrange_list:
			ind_unit = ArrangeIndUnit(pos[0], pos[1])
			self.scene.addItem(ind_unit)
			ind_unit.setPos(pos[0],pos[1])
			list_.append(ind_unit)

	def drawRoute(self, route_list, list_, vis = True):
		for pos in route_list:
			ind_unit = RouteIndUnit(pos[0], pos[1])
			self.scene.addItem(ind_unit)
			ind_unit.setPos(pos[0],pos[1])
			if not vis:
				ind_unit.setVisible(False)
			list_.append(ind_unit)
			
	#得到指定回合的地图,通过每回合mapchange计算,也可以采用占用内存提高速度的办法一开始就计算好每回合地图
	def getMap(self, round_, status):
		map_ = copy.copy(self.iniMapInfo)
		for i in range(round_):
			if self.mapChangeInfo[i]:
				for change in self.mapChangeInfo[i]:
					map_[change[1][1]][change[1][0]] = basic.Map_Basic(change[0])
		if status:
			change_ = self.mapChangeInfo[round_]
			for change in change_:
				map_[change[1][1]][change[1][0]] = basic.Map_Basic(change[0])
		return map_

	def setMap(self, map_):
		self.resetMap()
		self.width = len(map_[0])
		self.height = len(map_)
		for i in range(self.height):
			for j in range(self.width):
				new_map = MapUnit(i,j,map_[i][j])
				self.scene.addItem(new_map)
				new_map.setPos(i,j)
				self.MapList.append(new_map)

	def setSoldier(self, units):
		self.resetUnit()
		for i in range(2):
			for j in range(len(units[i])):
				#如果生命小于0
				new_unit = SoldierUnit(units[i][j],(i,j))
				self.UnitBase[i].append(new_unit)
				if units[i][j].life <= 0:
					continue
				self.scene.addItem(new_unit)
				new_unit.setPos(new_unit.corX, new_unit.corY)

	def SetInitMap(self, mapInfo, baseInfo):
		self.setMap(mapInfo)
		self.setSoldier(baseInfo)

	def Initialize(self, begInfo,frInfo):
		self.setMap(begInfo.map)
		self.iniMapInfo = begInfo.map
		self.setSoldier(begInfo.base)
		self.latestStatus = self.latestRound = 0
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
		#self.mapChangeInfo.append(reInfo.change)
		self.mapChangeInfo.append([])

	#从当前回合开始播放至这一回合结束
	def TerminateAni(self):
		if self.animation:
			self.animation.stop()
			self.animation.deleteLater()
			self.animation = None
		for item in self.animationItem:
			self.scene.removeItem(item)
		self.animationItem = []

	def moveAnimation(self, move_unit, move_pos,route):
		TIME_PER_GRID = 800

		steps = len(route)
		print "route::::::::::::::::", route
		movAnim = QPropertyAnimation(move_unit, "pos")
		movAnim.setDuration(steps * TIME_PER_GRID)
		movAnim.setStartValue(GetPos(move_unit.obj.position[0], move_unit.obj.position[1]))

		for i in range(steps):
			pos = GetPos(route[i][0], route[i][1])
			movAnim.setKeyValueAt(float(i + 1)/steps, pos)
		if route:
			movAnim.setEndValue(GetPos(route[-1][0],route[-1][1]))
		else:
			movAnim.setEndValue(GetPos(move_unit.obj.position[0], move_unit.obj.position[1]))
		return movAnim, []

	def attackAnimation(self, move_unit,move_pos, attack_target, target_pos, effect):
		ATTACK_TIME = 1500
		TOTAL_TIME = 2000

		if effect == -1:#超出范围或未攻击(已死亡)
			#可以增加逻辑展示超出范围等信息(not nessasary)
			return QPauseAnimation(500), []

		attackInd = AttackIndUnit(move_pos[0], move_pos[1],":attack_ind1.png")# %move_unit.obj.kind)
		attackInd.setOpacity(0)
		targetInd = TargetIndUnit(0,0)
		targetInd.setOpacity(0)
		sound = QSound(":attack_sound.wav")

		self.scene.addItem(attackInd)
		self.scene.addItem(targetInd)
		attackInd.setPos(attackInd.corX, attackInd.corY)
		targetInd.setPos(target_pos[0],target_pos[1])

		showAtkAnim = QParallelAnimationGroup()
		ani = QPropertyAnimation(attackInd, "pos")
		ani.setStartValue(GetPos(attackInd.corX,attackInd.corY))
		ani.setDuration(ATTACK_TIME)
		ani.setEndValue(GetPos(targetInd.corX, targetInd.corY))
		self.connect(ani, SIGNAL("finished()"), sound, SLOT("play()"))
		showAtkAnim.addAnimation(ani)

		ani = QPropertyAnimation(attackInd, "opacity")
		ani.setDuration(TOTAL_TIME)
		ani.setStartValue(0)
		ani.setKeyValueAt(0.1, 1)
		ani.setKeyValueAt(0.8, 0.9)
		ani.setKeyValueAt(0.9, 0.8)
		ani.setEndValue(0)
		showAtkAnim.addAnimation(ani)

		ani = QPropertyAnimation(targetInd, "opacity")
		ani.setDuration(TOTAL_TIME)
		ani.setStartValue(0)
		ani.setKeyValueAt(0.1, 1)
		ani.setKeyValueAt(0.5, 0.7)
		ani.setKeyValueAt(0.99, 1)
#		ani.setKeyValueAt(1, 1)
		ani.setEndValue(0)
		showAtkAnim.addAnimation(ani)
		#攻击效果展示

		if effect:
			label = EffectIndUnit("- %d" %(-self.gameEndInfo[self.nowRound][1].base[attack_target[0]][attack_target[1]].life +\
											self.gameBegInfo[self.nowRound].base[attack_target[0]][attack_target[1]].life)
								  )
		else:
			label = EffectIndUnit("Miss")
		label.setOpacity(0)
		self.scene.addItem(label)
		label.setPos(GetPos(targetInd.corX, targetInd.corY)+QPointF(0,-10))
		ani = QPropertyAnimation(label, "opacity")
		ani.setDuration(TOTAL_TIME)
		ani.setStartValue(0)
		ani.setKeyValueAt(0.05, 1)
		ani.setEndValue(0)
		showAtkAnim.addAnimation(ani)

		ani = QPropertyAnimation(label, "pos")
		ani.setDuration(TOTAL_TIME)
		pos1 = label.pos()
		ani.setStartValue(pos1)
		ani.setEndValue(pos1 + QPointF(0,-30))
		ani.setEasingCurve(QEasingCurve.OutCubic)
		showAtkAnim.addAnimation(ani)

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
		dieInd.setOpacity(0)
		
		dieAnim = QParallelAnimationGroup()
		dieAni = QPropertyAnimation(unit, "opacity")
		dieAni.setDuration(TOTAL_TIME)
		dieAni.setStartValue(1)
		dieAni.setEndValue(0)
		dieAnim.addAnimation(dieAni)
		dieAni1 = QPropertyAnimation(dieInd, "opacity")
		dieAni1.setDuration(TOTAL_TIME)
		dieAni1.setStartValue(0)
		dieAni1.setKeyValueAt(0.1 ,1)
		dieAni1.setKeyValueAt(0.2, 0.3)
		dieAni1.setKeyValueAt(0.4, 0.8)
		dieAni1.setKeyValueAt(0.7, 0.2)
		dieAni1.setKeyValueAt(0.9, 0.6)
		dieAni1.setEndValue(0)
		dieAnim.addAnimation(dieAni1)

		return dieAnim, [dieInd]

	def transAnimation(self, move_unit, pos1, pos2):
		items = []
		ani = QParallelAnimationGroup()
		
		item = TransIndUnit(0, pos1[0], pos1[1])
		self.scene.addItem(item)
		item.setPos(item.corX, item.corY)
		item.setOpacity(0)
		items.append(item)
		anim = QPropertyAnimation(item, "opacity")
		anim.setDuration(1500)
		anim.setStartValue(0)
		anim.setKeyValueAt(0.1, 1)
		anim.setKeyValueAt(0.9, 0.8)
		anim.setEndValue(0)
		ani.addAnimation(anim)
		
		item = TransIndUnit(0, pos2[0], pos2[1])
		self.scene.addItem(item)
		item.setPos(item.corX, item.corY)
		item.setOpacity(0)
		items.append(item)
		anim = QPropertyAnimation(item, "opacity")
		anim.setDuration(1500)
		anim.setStartValue(0)
		anim.setKeyValueAt(0.3, 1)
		anim.setKeyValueAt(0.95, 0.8)
		anim.setEndValue(0)
		ani.addAnimation(anim)

		pos1 = GetPos(pos1[0], pos1[1])
		pos2 = GetPos(pos2[0], pos2[1])
		anim = QPropertyAnimation(move_unit, "pos")
		anim.setDuration(1500)
		anim.setStartValue(pos1)
		anim.setKeyValueAt(0.4, pos1)
		anim.setKeyValueAt(0.5,pos2)
		anim.setEndValue(pos2)
		ani.addAnimation(anim)

		anim = QPropertyAnimation(move_unit, "opacity")
		anim.setDuration(1500)
		anim.setStartValue(1)
		anim.setKeyValueAt(0.1, 0.5)
		anim.setKeyValueAt(0.2, 1)
		anim.setKeyValueAt(0.3, 0.5)
		anim.setKeyValueAt(0.4, 0)
		anim.setKeyValueAt(0.5, 0)
		anim.setKeyValueAt(0.6, 1)
		anim.setEndValue(1)
		ani.addAnimation(anim)

		return ani, items

	def skillAnimation(self, unit_move, target_unit,target):
		items = []
		anim = QParallelAnimationGroup()

		kind = unit_move.obj.kind
		if kind == 8:
			eff_ind = EffectIndUnit(QString.fromUtf8("能力提升"))
		else:
			healthier = self.gameEndInfo[self.nowRound][1].base[target_unit[0]][target_unit[1]].life - \
				self.gameBegInfo[self.nowRound].base[target_unit[0]][target_unit[1]].life
			eff_ind = EffectIndUnit("+ %d"%healthier)
		self.scene.addItem(eff_ind)
		eff_ind.setOpacity(0)
		eff_ind.setPos(GetPos(target[0], target[1]) + QPointF(0, -20))
		ani = QPropertyAnimation(eff_ind, "pos")
		ani.setDuration(1000)
		ani.setStartValue(GetPos(target[0],target[1]) + QPointF(0, -20))
		ani.setEndValue(GetPos(target[0], target[1]) + QPointF(0,-50))
		ani.setEasingCurve(QEasingCurve.OutCubic)
		anim.addAnimation(ani)
		items.append(eff_ind)

		ani = QPropertyAnimation(eff_ind, "opacity")
		ani.setDuration(1000)
		ani.setStartValue(0)
		ani.setKeyValueAt(0.1, 1)
		ani.setKeyValueAt(0.9, 1)
		ani.setEndValue(0)
		anim.addAnimation(ani)

		text = "某某光环" if kind == 8 else "回复技能"
		kind_ind = EffectIndUnit(QString.fromUtf8(text))
		self.scene.addItem(kind_ind)
		kind_ind.setOpacity(0)
		pos_ = self.gameEndInfo[self.nowRound][1].base[unit_move.idNum[0]][unit_move.idNum[1]].position
		pos_ = GetPos(pos_[0], pos_[1])
		kind_ind.setPos(pos_ + QPointF(0, -10))
		ani = QPropertyAnimation(kind_ind, "pos")
		ani.setDuration(1000)
		ani.setStartValue(pos_ + QPointF(0, -20))
		ani.setEndValue(pos_ + QPointF(0,-50))
		ani.setEasingCurve(QEasingCurve.OutCubic)
		anim.addAnimation(ani)
		items.append(kind_ind)

		
		ani = QPropertyAnimation(kind_ind, "opacity")
		ani.setDuration(1000)
		ani.setStartValue(0)
		ani.setKeyValueAt(0.05, 1)
		ani.setKeyValueAt(0.9, 1)
		ani.setEndValue(0)
		anim.addAnimation(ani)

		target_ind = TargetIndUnit(0, 0)
		self.scene.addItem(target_ind)
		target_ind.setPos(target[0], target[1])
		target_ind.setOpacity(0)
		ani = QPropertyAnimation(target_ind, "opacity")
		ani.setDuration(1000)
		ani.setStartValue(0)
		ani.setKeyValueAt(0.1, 1)
		ani.setKeyValueAt(0.5, 0.7)
		ani.setKeyValueAt(0.9, 1)
		ani.setEndValue(0)
		anim.addAnimation(ani)
		items.append(target_ind)

		return anim, items
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
		ani, item = self.moveAnimation(unit_move, cmd.move, endInfo.route)
		self.animation.addAnimation(ani)
		self.animationItem.extend(item)
		ani = QPauseAnimation(300)
		self.animation.addAnimation(ani)

		if cmd.move != endInfo.base[unit_id[0]][unit_id[1]].position:
			ani, item = self.transAnimation(unit_move, cmd.move, endInfo.base[unit_id[0]][unit_id[1]].position)
			self.animation.addAnimation(ani)
			self.animationItem.extend(item)
		#attack
		if cmd.order:
			unit_target = self.UnitBase[cmd.target[0]][cmd.target[1]]
		if cmd.order == 1:
			if self.UnitBase[cmd.target[0]][cmd.target[1]].obj.life > 0:
				ani, item = self.attackAnimation(unit_move, endInfo.base[unit_id[0]][unit_id[1]].position, cmd.target,
												unit_target.obj.position,
												endInfo.effect[0])

				self.animationItem.extend(item)
				self.animation.addAnimation(ani)
				
				#target die
				if endInfo.base[cmd.target[0]][cmd.target[1]].life <= 0:
					anim, item = self.dieAnimation(cmd.target)
					self.animationItem.extend(item)
					self.animation.addAnimation(anim)
				
				#fight back
				anim, item = self.attackAnimation(unit_target, (unit_target.corX, unit_target.corY),
												  unit_id ,endInfo.base[unit_id[0]][unit_id[1]].position, endInfo.effect[1])
				self.animationItem.extend(item)
				self.animation.addAnimation(anim)
				if endInfo.base[unit_id[0]][unit_id[1]].life <= 0:
					anim, item = self.dieAnimation(unit_id)
					self.animationItem.extend(item)
					self.animation.addAnimation(anim)
		#skill
		elif cmd.order == 2:
			if unit_move.obj.kind >= 5 and unit_move.obj.kind != 7:
				anim, item = self.skillAnimation(unit_move, cmd.target, unit_target.obj.position) 
				self.animation.addAnimation(anim)
				self.animationItem.extend(item)

		#待机只暂停1秒
		self.animation.addAnimation(QPauseAnimation(1000))
		self.connect(self.animation, SIGNAL("finished()"), self.moveAnimEnd)
		self.connect(self.animation, SIGNAL("finished()"), self.animation, SLOT("deleteLater()"))
		#self.connect(self.animation, SIGNAL("finished()"), self.__test)
		#self.connect(self.animation, SIGNAL("finished()"), self.TerminateAni)	
		self.animation.start()

	#展示round_, status的场面
	def GoToRound(self, round_, status):
		self.TerminateAni()

		if round_ * 2 + status > self.latestRound * 2 + self.latestStatus or round_ < 0:
			raise REPLAYERROR("not update to that status")

		self.nowRound = round_
		self.nowStatus = status

		self.setMap(self.getMap(round_, status))

		if status:
			self.setSoldier(self.gameEndInfo[round_][1].base)
		else:

			self.setSoldier(self.gameBegInfo[round_].base)

	def resetMap(self):
		for item in self.MapList:
			self.scene.removeItem(item)

		self.MapList = []
	def resetUnit(self):
		for item in self.UnitBase[0]:
			if item.scene() == self.scene:
				self.scene.removeItem(item)
		for item in self.UnitBase[1]:
			if item.scene() == self.scene:
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
		self.TerminateAni()
		self.emit(SIGNAL("endGame()"))
		self.resetToPlay()
		self.route_ind_list = []
		self.move_range_list = []
		self.attack_range_list = []

		self.resetUnit()
		self.resetMap()
		self.mapChangeInfo = []

		self.gameBegInfo = []
		self.gameEndInfo = []

		self.now_state = self.nowMoveUnit = self.command = self.moveToPos = self.Operation = self.iniMapInfo = None
		self.latestStatus = 1
		self.latestRound = 0
		self.run = False
		self.mouseUnit.setVis(False)
		self.mouseUnit.setVisible(False)
		self.focusUnit.setVisible(False)
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
