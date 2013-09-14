# -*- coding: utf-8 -*-
#new version

from Ui_UnitsNew import *
from Ui_Error import Ui_Error
import sys, math
from testdata import *

class Ui_MouseInfo:
	def __init__(self, view, event):
		if (not issubclass(view.__class__, Ui_View)):
			pass#raise error
		self.nowCoor = view.mapToScene(event.pos())
		self.initPos = view.nowPos
		self.nowPos = GetGrid(self.nowCoor.x(), self.nowCoor.y())
		self.isValid = True
		if (self.nowPos[0]<0 or self.nowPos[1]<0 or
			self.nowPos[0]>=view.mapSize[0] or self.nowPos[1]>=view.mapSize[0]):
			self.nowPos = self.initPos
			self.isValid = False
		self.eventType = event.type()
		self.eventButton = event.button()
		self.eventAccept = True
		if (self.eventType==event.MouseButtonRelease and
			view._Ui_View__validMousePress):
			self.isValid = False


class Ui_View(QtGui.QGraphicsView):
	def __init__(self, scene, parent = None):
		QtGui.QGraphicsView.__init__(self, scene, parent)
		self.unitMap = {}
		self.mapSize = (0, 0)
		self.nowPos = (0, 0)
		self.focusGrid = QtCore.QPoint(0, 0)
		#self.focusPoint = QtCore.QPoint(0, 0)
		self.dragUnit = None
		self.__validMousePress = False

	def Initialize(self, mapSizeX, mapSizeY):
		self.mapSize = (mapSizeX, mapSizeY)
		self.unitMap.clear()
		for x in range(mapSizeX):
			for y in range(mapSizeY):
				self.unitMap[(x, y)] = []
		self.setMouseTracking(True)#for test
		sizeX = mapSizeX*UNIT_WIDTH
		sizeY = mapSizeY*UNIT_HEIGHT
		self.scene().setSceneRect(0-MARGIN_WIDTH, 0-MARGIN_WIDTH,
								  sizeX+2*MARGIN_WIDTH, sizeY+2*MARGIN_WIDTH)
		self.setBackgroundBrush(QtGui.QColor(255, 255, 255))

	def AddItem(self, item):
		item.hashIndex = (item.mapX, item.mapY)
		self.unitMap[item.hashIndex].append(item)
		self.scene().addItem(item)
	def RemoveItem(self, item):
		self.unitMap[item.hashIndex].remove(item)
		del item.hashIndex
		self.scene().removeItem(item)
	def UpdateHash(self, pos):
		if (pos not in self.unitMap.keys()):
			print "error : key"#for test
			return
		newHash = []
		for item in self.unitMap[pos]:
			if ((item.mapX, item.mapY)==pos):
				newHash.append(item)
			else:
				item.hashIndex = (item.mapX, item.mapY)
				self.unitMap[item.hashIndex].append(item)
		self.unitMap[pos] = newHash
	#if bug appears, consider the z value

	def GetFocusPoint(self):
		rect = self.geometry()
		return self.mapToScene(QtCore.QPoint(0, 0))+QtCore.QPoint(rect.width(), rect.height())/2
		#return self.focusPoint
	def SetFocusPoint(self, point):
		#self.focusPoint = point
		#pointf = QtCore.QPointF(point.x(), point.y())
		self.centerOn(point)

	def GetFocusGrid(self):
		return self.focusGrid
	def SetFocusGrid(self, grid):
		if (self.focusGrid!=grid):
			self.focusGridChange.emit(grid)
		self.focusGrid = grid
	focusGridChange = QtCore.pyqtSignal(QtCore.QPoint)
	
	pFocusPoint = QtCore.pyqtProperty(QtCore.QPointF, fget = GetFocusPoint,
									 fset = SetFocusPoint)
	pFocusGrid = QtCore.pyqtProperty(QtCore.QPoint, fget = GetFocusGrid,
									fset = SetFocusGrid, notify = focusGridChange)

	def SetFocusAnimation(self, grid, time):
		centerAnim = QtCore.QPropertyAnimation(self, "pFocusPoint")
		centerAnim.setDuration(time)
		#centerAnim.setStartValue(GetPos(grid[0], grid[1]))
		centerAnim.setKeyValueAt(0.5, GetPos(grid[0], grid[1]))
		centerAnim.setEndValue(GetPos(grid[0], grid[1]))
		focusAnim = QtCore.QPropertyAnimation(self, "pFocusGrid")
		focusAnim.setDuration(time)
		focusAnim.setStartValue(QtCore.QPoint(grid[0], grid[1]))
		focusAnim.setEndValue(QtCore.QPoint(grid[0], grid[1]))
		anim = QtCore.QParallelAnimationGroup()
		anim.addAnimation(centerAnim)
		anim.addAnimation(focusAnim)
		return anim
		
	def RaiseEvent(self, pos, eventType, args):
		l = len(self.unitMap[pos])
		while (l>0):
			l -= 1
			if (eventType==self.MOUSE_PRESS_EVENT):
				result = self.unitMap[pos][l].MousePressEvent(args)
			elif (eventType==self.ENTER_EVENT):
				result = self.unitMap[pos][l].MouseEnterEvent(args)
			elif (eventType==self.LEAVE_EVENT):
				result = self.unitMap[pos][l].MouseLeaveEvent(args)
			elif (eventType==self.DRAG_START_EVENT):
				result = self.unitMap[pos][l].DragStartEvent(args)
			elif (eventType==self.DRAG_STOP_EVENT):
				result = self.unitMap[pos][l].DragStopEvent(args)
			if (result):
				return result

	def mousePressEvent(self, event):
		self.MouseEvent(event)
	def mouseReleaseEvent(self, event):
		self.MouseEvent(event)
	def mouseMoveEvent(self, event):
		self.MouseEvent(event)
	#transformer
	
	def MouseEvent(self, event):
		info = Ui_MouseInfo(self, event)
		self.nowPos = info.nowPos
		if (info.eventType==QtCore.QEvent.MouseButtonPress and
			info.eventButton==QtCore.Qt.LeftButton and info.isValid):
			self.SetFocusGrid(QtCore.QPoint(info.nowPos[0], info.nowPos[1]))
			self.RaiseEvent(info.nowPos, self.MOUSE_PRESS_EVENT, info)
			self.__validMousePress = True
			#handles the mouse press event
			self.dragUnit = self.RaiseEvent(info.nowPos, self.DRAG_START_EVENT, info)
			#starts a drag
		elif (info.eventType==QtCore.QEvent.MouseButtonRelease and
			  info.eventButton==QtCore.Qt.LeftButton):
			if (self.dragUnit!=None):
				if (self.unitMap[info.nowPos]==[] or
					self.RaiseEvent(info.nowPos, self.DRAG_STOP_EVENT, (self.dragUnit, info))):
					self.dragUnit.DragComplete(info)
					self.UpdateHash(self.dragUnit.hashIndex)
				else:
					self.dragUnit.DragFail(info)
					raise IndexError#for test
			self.dragUnit = None
			self.__validMousePress = False
			#handles the drop event
		elif (info.eventType==QtCore.QEvent.MouseMove and info.isValid):
			if (self.dragUnit!=None):
				self.dragUnit.setPos(info.nowCoor-DRAG_SPOT)#handles the drag-move event
				self.RaiseEvent(info.nowPos, self.DRAG_STOP_EVENT, (self.dragUnit, info))
			if (info.initPos!=info.nowPos):
				self.RaiseEvent(info.initPos, self.LEAVE_EVENT, info)
				self.RaiseEvent(info.nowPos, self.ENTER_EVENT, info)
				#handles the enter and the leave event
				#如果鼠标在拖放状态下移出widget外怎么办？
		self.UpdateHash(info.initPos)
		self.UpdateHash(info.nowPos)
		self.scene().update()
		#updates the hash map
	#handles seperatedly or together?
			
	#def keyPressEvent(self, event):

	MOUSE_PRESS_EVENT = 1
	DRAG_START_EVENT = 2
	DRAG_STOP_EVENT = 3
	LEAVE_EVENT = 4
	ENTER_EVENT = 5



##############################################################

class Ui_ReplayView(Ui_View):
	"the replay graphic view"
	def __init__(self, scene, parent = None):
		Ui_View.__init__(self, scene, parent)
		self.__mapUnitType = Ui_MapUnit
		self.__soldierUnitType = Ui_SoldierUnit
		self.__cursorType = Ui_MouseCursor
		#init of types
		self.mapItem = []
		self.soldierItem = []
		self.soldierAlive = []
		self.sizeX = 0
		self.sizeY = 0
		#ini of items
		self.cursor = None
		#ini of the cursor
		#self.movTimeline = QtCore.QTimeLine()
		#self.atkTimeline = QtCore.QTimeLine()
		#self.dieTimeline = QtCore.QTimeLine()
		#self.animation = QtGui.QGraphicsItemAnimation()
		#self.label = Ui_GridLabel("", 0, 0)
		#ini of the animation

	def SetUnitType(self, mapUnit, soldierUnit, cursor):
		if (mapUnit!=None and issubclass(mapUnit, Ui_MapUnit)):
			self.__mapUnitType = mapUnit
		if (soldierUnit!=None and issubclass(soldierUnit, Ui_SoldierUnit)):
			self.__soldierUnitType = soldierUnit
		if (cursor!=None and issubclass(cursor, Ui_GridUnit)):
			self.__cursorType = cursor
	
	def Initialize(self, maps, units,
				   MapUnit = None, SoldierUnit = None, Cursor = None):
		self.SetUnitType(MapUnit, SoldierUnit, Cursor)
		#check the type
		scene = self.scene()
		for item in scene.items():
			scene.removeItem(item)
		if (maps==[]):#trying...
			Ui_View.Initialize(0, 0)#for trying...
			return#for trying...
		Ui_View.Initialize(self, len(maps), len(maps[0]))
		#initialize
		#self.sizeX = len(maps)*UNIT_WIDTH
		#self.sizeY = len(maps[0])*UNIT_HEIGHT
		self.mapItem = []
		for i in range(len(maps)):
			newColumn = []
			for j in range(len(maps[i])):
				newMapUnit = self.__mapUnitType(i, j, maps[i][j])
				self.AddItem(newMapUnit)
				newColumn.append(newMapUnit)
			self.mapItem.append(newColumn)
		for i in range(len(maps)):
			for j in range(len(maps[i])):
				self.mapItem[i][j].setPos(GetPos(i, j))
		#initialization of map units
		self.soldierItem = {}
		self.soldierAlive = {}
		for idNum in units.keys():
			newSoldierUnit = self.__soldierUnitType(idNum, idNum[0], units[idNum])
			self.AddItem(newSoldierUnit)
			self.soldierItem[idNum] = newSoldierUnit
			self.soldierAlive[idNum] = True
		self.SetSoldiers(units)
		#initialization of soldier units
		self.cursor = self.__cursorType()
		self.AddItem(self.cursor)
		#initialization of the cursor

	def SetSoldiers(self, units):
		"set the pos of soldiers"
		#alive = map(lambda unit: (unit.life!=0), units)
		for i in units.keys():
			alive = (units[i].life!=0)
			if (alive!=self.soldierAlive[i]):
				self.soldierItem[i].SetEnabled(alive)
				self.soldierAlive[i] = alive
			if (self.soldierAlive[i]):
				self.soldierItem[i].SetMapPos(units[i].position[0],
											  units[i].position[1])
				
	#animation module
	def MovingAnimation(self, idnum, route):
		"moving animation, displayed when the soldier moves"
		TIME_PER_FRAME = 1000#ms, one-step movement in a frame
		FRAMES_BEFORE_MOVE = 3
		soldier = self.soldierItem[idnum]
		steps = len(route) - 1
		if (not route):
			print "EEEEEEEEEEEEEEEEEEEEEEError!!"#for test
			route = ((soldier.mapX, soldier.mapY),)#for test

		#movTimeline = QtCore.QTimeLine(frames*TIME_PER_FRAME)
		#movTimeline.setCurveShape(movTimeline.LinearCurve)
		#animation = QtGui.QGraphicsItemAnimation()
		#animation.setItem(soldier)
		#animation.setTimeLine(movTimeline)
		movAnim = Ui_Animation(soldier, "pos")
		movAnim.setStartValue(GetPos(route[0][0],route[0][1]))
		if steps:
			movAnim.setDuration(steps*TIME_PER_FRAME)
			for i in range(steps+1):
				pos = GetPos(route[i][0], route[i][1])
				movAnim.setKeyValueAt(float(i)/steps, pos)
		else:
			movAnim.setDuration(TIME_PER_FRAME)
		movAnim.setEndValue(GetPos(route[-1][0],route[-1][1]))
		cursor = Ui_GridCursor(route[0][0], route[0][1])
		cursAnim = Ui_Animation(cursor, "enability")
		cursAnim.setDuration(FRAMES_BEFORE_MOVE*TIME_PER_FRAME)
		cursAnim.setStartValue(True)
		cursAnim.setKeyValueAt(0.999, False)
		cursAnim.setEndValue(False)
		focusAnim = self.SetFocusAnimation(route[0],
										   FRAMES_BEFORE_MOVE*TIME_PER_FRAME)
		prepAnim = QtCore.QParallelAnimationGroup()
		prepAnim.addAnimation(cursAnim)
		prepAnim.addAnimation(focusAnim)
		
		anim = QtCore.QSequentialAnimationGroup()
		anim.addAnimation(prepAnim)
		anim.addAnimation(movAnim)
		#
		#anim = {}
		#anim["timeline"] = movTimeline
		#anim["animation"] = animation
		item = [cursor]
		cursor.SetEnabled(False)
		return anim, item

	def AttackingAnimation(self, selfId, targetId, damage, info = ""):
		"attack animation, displayed when the soldier launches an attack."
		TOTAL_TIME = 2000
		TIME_FOR_MOVING = 500
		TIME_WHEN_RESETING = 1900
		FRICKER_INTERVAL = 200
		TIME_FOR_SHOW = 200
		DIST = 0.3
		attacker = self.soldierItem[selfId]
		target = self.soldierItem[targetId]
		
		#atkTimeline = QtCore.QTimeLine(TOTAL_TIME)
		#atkTimeline.setCurveShape(atkTimeline.LinearCurve)
		#animation = QtCore.QGraphicsItemAnimation()
		#animation.setItem(attacker)
		#animation.setTimeLine(atkTimeline)
		showAtkAnim = QtCore.QParallelAnimationGroup()
		showAtkAnim.addAnimation(self.SetFocusAnimation((attacker.mapX, attacker.mapY),
													TIME_FOR_SHOW))
		atkCurs = Ui_GridCursor(attacker.mapX, attacker.mapY)
		atkCursAnim = Ui_Animation(atkCurs, "enability")
		atkCursAnim.setDuration(TIME_FOR_SHOW)
		atkCursAnim.setStartValue(True)
		atkCursAnim.setKeyValueAt(0.999, False)
		atkCursAnim.setEndValue(False)
		showAtkAnim.addAnimation(atkCursAnim)
		
		showTagAnim = QtCore.QParallelAnimationGroup()
		showTagAnim.addAnimation(self.SetFocusAnimation((target.mapX, target.mapY),
													TIME_FOR_SHOW))
		tagCurs = Ui_TargetCursor(target.mapX, target.mapY)
		tagCursAnim = Ui_Animation(tagCurs, "enability")
		tagCursAnim.setDuration(TIME_FOR_SHOW)
		tagCursAnim.setStartValue(True)
		tagCursAnim.setKeyValueAt(0.999, False)
		tagCursAnim.setEndValue(False)
		showTagAnim.addAnimation(tagCursAnim)

		atkAnim = QtCore.QParallelAnimationGroup()
		r = DIST/math.sqrt((attacker.mapX-target.mapX)**2+(attacker.mapY-target.mapY)**2)
		pos = attacker.GetPos()*(1-r)+target.GetPos()*r
		atkMovAnim = Ui_Animation(attacker, "pos")
		atkMovAnim.setDuration(TOTAL_TIME)
		atkMovAnim.setKeyValueAt(0, attacker.GetPos())
		atkMovAnim.setKeyValueAt(float(TIME_FOR_MOVING)/TOTAL_TIME, pos)
		atkMovAnim.setKeyValueAt(float(TIME_WHEN_RESETING)/TOTAL_TIME, pos)
		atkMovAnim.setKeyValueAt(1, attacker.GetPos())
		atkAnim.addAnimation(atkMovAnim)		

		text = "%+d" % damage
		if (damage==0):
			text = info
		label = Ui_GridLabel(text, target.mapX, target.mapY)
		labelAnim = QtCore.QPropertyAnimation(label, "opacity")
		labelAnim.setDuration(TOTAL_TIME)
		labelAnim.setKeyValueAt(0, 0)
		labelAnim.setKeyValueAt(0.25, 0)
		labelAnim.setKeyValueAt(0.3, 0)
		labelAnim.setKeyValueAt(0.9, 1)
		labelAnim.setKeyValueAt(0.91, 0)
		labelAnim.setKeyValueAt(1, 0)
		atkAnim.addAnimation(labelAnim)

		if (damage<0):
			dmgAnim = Ui_Animation(target, "enability")
			dmgAnim.setDuration(TOTAL_TIME)
			enabled = False
			for i in range(TIME_FOR_MOVING, TIME_WHEN_RESETING, FRICKER_INTERVAL):
				dmgAnim.setKeyValueAt(float(i)/TOTAL_TIME, enabled)
				enabled = not enabled
			dmgAnim.setKeyValueAt(float(TIME_WHEN_RESETING)/TOTAL_TIME, False)
			dmgAnim.setEndValue(True)
			atkAnim.addAnimation(dmgAnim)

		anim = QtCore.QSequentialAnimationGroup()
		anim.addAnimation(showAtkAnim)
		anim.addAnimation(showTagAnim)
		anim.addAnimation(atkAnim)
		#self.scene().addItem(label)
		#self.connect(atkTimeline, QtCore.SIGNAL("valueChanged(qreal)"),
		#			 label.ShowLabel)
		#set focus
		item = [label, atkCurs, tagCurs]
		atkCurs.SetEnabled(False)
		tagCurs.SetEnabled(False)
		label.SetEnabled(True)
		label.setOpacity(0)
		return anim, item

	def DiedAnimation(self, selfId):
		"displayed when a soldier dies"
		TOTAL_TIME = 2000
		soldier = self.soldierItem[selfId]
		print "add die animation........"
		#dieTimeline = QtCore.QTimeLine(TOTAL_TIME)
		#dieTimeline.setCurveShape(dieTimeline.LinearCurve)
		#dieTimeline.setUpdateInterval(TIME_PER_FRAME)
		#self.connect(dieTimeline, QtCore.SIGNAL('valueChanged(qreal)'),
		#			 soldier.FadeOut)
		#anim = {}
		#anim["timeline"] = dieTimeline
		dieAnim = Ui_Animation(soldier, "opacity")
		dieAnim.setDuration(TOTAL_TIME)
		dieAnim.setStartValue(1)
		dieAnim.setEndValue(0)

		cursor = Ui_GridCursor(soldier.mapX, soldier.mapY)
		cursAnim = Ui_Animation(cursor, "enability")
		cursAnim.setDuration(TOTAL_TIME)
		cursAnim.setStartValue(True)
		cursAnim.setKeyValueAt(0.999, False)
		cursAnim.setEndValue(False)

		anim = QtCore.QParallelAnimationGroup()
		anim.addAnimation(dieAnim)
		anim.addAnimation(cursAnim)
		anim.addAnimation(self.SetFocusAnimation((soldier.mapX, soldier.mapY),
												 TOTAL_TIME))
		
		item = [cursor]
		cursor.SetEnabled(False)
		return anim, item

	#def TerrainChangeAnimation(self):

	#cursor




if __name__=="__main__":
	app = QtGui.QApplication(sys.argv)
	scene = QtGui.QGraphicsScene()
	view = Ui_ReplayView(scene)
	units= ConvertTo1D(units0)
	view.Initialize(maps, units)
	anim, item = view.MovingAnimation((0, 0), ((0, 7), (0, 6), (1, 6), (2, 6), (2, 5)))
	#anim, item = view.AttackingAnimation(0, 5, 0, "blocked!")
	#anim, item = view.DiedAnimation(3)

	view.show()
	#view.centerOn(QtCore.QPointF(500, 500))
	for i in item:
		scene.addItem(i)
	#anim["timeline"].start()
	view.cursor.SetEnabled(False)
	view.setEnabled(False)
	anim.start()
	sys.exit(app.exec_())

