# -*- coding: utf-8 -*-
#Ver 0.3.1 edited at 2013-07-23-23:56
#Changes: animation, goto func
#Changes: data updates
#Changes: initialize
#need to change: error sended in showstatus func

#replay widget

from Ui_2DReplaySceneNew import *
from testdata import *


class Ui_2DReplayWidget(Ui_ReplayView):
	def __init__(self, scene, parent = None):
		Ui_ReplayView.__init__(self, scene, parent)
		self.data = None
		self.nowRound = 0
		self.status = self.BEGIN_FLAG
		self.latestRound = -1
		self.latestStatus = self.BEGIN_FLAG
		self.anim = None
		self.additionItem = []
		#animation
		self.animState = 0
	def Initialize(self, iniInfo, begInfo):
		self.data = UiD_BattleData(iniInfo, begInfo)
		print self.data.iniUnits#for test
		Ui_ReplayView.Initialize(self, self.data.map, self.data.iniUnits)
		#connecting disp signals
		#for column in self.mapItem:
			#for grid in column:
				#grid.mapGridSelected.connect(self.__callMapGridDisp)
		#for unit in self.soldierItem:
			#unit.soldierSelected.connect(self.__callUnitDisp)
		self.focusGridChange.connect(self.__emitInfo)
		#self.connect(self, QtCore.SIGNAL("unitSelected"), self.__dispFun)#for test
		#self.connect(self, QtCore.SIGNAL("mapGridSelected"), self.__dispFun)#for test
		#maybe the connecting part shouldn't be here.
		self.nowRound = 0
		self.status = self.BEGIN_FLAG
		self.latestRound = 0
		self.latestStatus = self.BEGIN_FLAG
		self.ShowStatus()

	def UpdateBeginData(self, begInfo):
		if (self.data.nextRoundInfo!=None):
			raise TypeError#raise error
		self.data.UpdateBeginData(begInfo)
		self.latestRound += 1
		self.latestStatus = self.BEGIN_FLAG
	def UpdateEndData(self, cmd, endInfo):
		if (self.data.nextRoundInfo==None):
			raise TypeError#raise error
		self.data.UpdateEndData(cmd, endInfo)
		self.latestStatus = self.END_FLAG

	#def GetGameInfo(self):
	#def GetTerrainInfo(self):
	#def GetSolldierInfo(self):

	def ShowStatus(self):
		self.__TerminateAnimation()
		self.animState = 0
		if (self.nowRound*2+self.status>self.latestRound*2+self.latestStatus):
			raise TypeError#raise error
		units = self.__getNowUnitArray()
		self.SetSoldiers(units)

	def ShowMoveAnimation(self):
		#check
		if (self.status==self.END_FLAG):
			return
		self.ShowStatus()
		try:
			cmd = self.data.roundInfo[self.nowRound].cmdChanges
		except IndexError:
			return#raise error?
		#initialize
		self.status = self.END_FLAG
		self.animState = self.ANIM_RUNNING
		self.anim = QtCore.QSequentialAnimationGroup()
		self.additionItem = []
		#move
		anim, item = self.MovingAnimation(cmd.idNum, cmd.route)
		self.anim.addAnimation(anim)
		self.additionItem.extend(item)
		#terrain changes
		#
		if (cmd.order==1):#attack
			anim, item = self.AttackingAnimation(cmd.idNum, cmd.target,
												 cmd.damage[1], cmd.note[1])
			self.anim.addAnimation(anim)
			self.additionItem.extend(item)
			if (cmd.isDead[1]):#target died
				anim, item = self.DiedAnimation(cmd.target)
				self.anim.addAnimation(anim)
				self.additionItem.extend(item)
			elif (cmd.fightBack):#target fights back
				anim, item = self.AttackingAnimation(cmd.target, cmd.idNum,
													 cmd.damage[0], cmd.damage[1])
				self.anim.addAnimation(anim)
				self.additionItem.extend(item)
				if (cmd.isDead[0]):#attacker dies
					anim, item = self.DiedAnimation(cmd.idNum)
					self.anim.addAnimation(anim)
					self.additionItem.extend(item)
		elif (cmd.order==2):#skill
			raise NotImplementedError
		elif (cmd.order==0):#standby
			pass
		#some other prepararion
		for item in self.additionItem:
			self.scene().addItem(item)
			item.SetEnabled(False)#set them invisible
		self.connect(self.anim, QtCore.SIGNAL("finished()"), self.ShowStatus)
		self.connect(self.anim, QtCore.SIGNAL("finished()"), self.moveAnimEnd)
		self.cursor.SetEnabled(False)
		self.setEnabled(False)

		self.anim.start()

	def __TerminateAnimation(self):
		if (self.anim!=None):
			self.anim.stop()
			self.anim.deleteLater()
			self.anim = None
		self.animState = self.ANIM_STOP
		for item in self.additionItem:
			self.scene().removeItem(item)
		
#		self.nowRound += (self.status+1)/2
#		self.status = (self.status+1)/2#
		self.additionItem = []
		self.cursor.SetEnabled(True)
		self.setEnabled(True)

				
		

	#def ShowBeginAnimation(self):

	def Play(self):
		if (self.nowRound*2+self.status>=self.latestRound*2+self.latestStatus
			or (self.nowRound==self.latestRound and self.latestStatus==self.BEGIN_FLAG)):
			raise TypeError#raise error
		else:
			if (self.status==self.BEGIN_FLAG):
				self.ShowMoveAnimation()
			elif (self.status==self.END_FLAG):
				pass#show begin

	def GoToRound(self, r = None, flag = None):
		"stop the animation and set the round state"
		if (flag!=None):
			self.status = flag
		if (r!=None):
			self.nowRound = r
		self.ShowStatus()

	def GetRoute(self, pos):
		return GetRoute(self.data.map,
						ConvertBackTo2D(self.__getNowUnitArray()),
						self.data.roundInfo[self.nowRound].idNum,
						pos)
	def GetMovRange(self):
		idNum = self.data.roundInfo[self.nowRound].idNum
		units = self.__getNowUnitArray()
		movRng = available_spots(self.data.map,
								 ConvertBackTo2D(units),
								 idNum)
		for i in units.keys():
			if (units[i].position in movRng and i!=idNum):
				movRng.remove(units[i].position)
		return movRng
	#some Qs
			
#	def GetAtkTarget(self, movPos):
		#returns a dictionary, with keys targets' pos, contents their id
#		raise NotImplementedError
#	def GetSkillTarget(self, movPos):
		#ts
#		raise NotImplementedError

	def __emitInfo(self, grid):
		x, y = grid.x(), grid.y()
		units = self.__getNowUnitArray()
		for i in self.soldierItem.keys():
			if ((self.soldierItem[i].mapX, self.soldierItem[i].mapY)==(x, y)):
				self.emit(QtCore.SIGNAL("unitSelected"), units[i])
				break
		self.emit(QtCore.SIGNAL("mapGridSelected"), self.data.map[x][y])
		
	#def __callUnitDisp(self, idnum):
		#self.unitSelected.emit((self.__getNowUnitArray())[idnum].__dict__)
	#def __callMapGridDisp(self, x, y):
		#self.mapGridSelected.emit(self.data.map[x][y].__dict__)

	def __getNowUnitArray(self):
		if (self.nowRound*2+self.status>self.latestRound*2+self.latestStatus):
			raise IndexError, "out of range"#raise error
		return self.data.GetUnitArray(self.nowRound, self.status)

	def __dispFun(self, dic):#for test
		print dic.__dict__#for test

	BEGIN_FLAG = 0
	END_FLAG = 1
	#flags showing the round state(at the beginning or the end)
	ANIM_STOP = 0
	ANIM_RUNNING = 1
	#flags showing the state of the animation
	moveAnimEnd = QtCore.pyqtSignal()
	begAnimEnd = QtCore.pyqtSignal()
	#signals of animation
	#unitSelected = QtCore.pyqtSignal(dict)
	#mapGridSelected = QtCore.pyqtSignal(dict)
	#signals for info display




if __name__=="__main__":
	app = QtGui.QApplication(sys.argv)
	scene = QtGui.QGraphicsScene()
	view = Ui_2DReplayWidget(scene)
	view.Initialize(iniInfo, begInfo0)
	view.UpdateEndData(cmd0, endInfo0)
	view.UpdateBeginData(begInfo1)
	view.UpdateEndData(cmd1 ,endInfo1)
	view.show()
	sys.exit(app.exec_())
	
