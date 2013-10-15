# -*- coding: UTF-8 -*-

#last edition: 2013-09-29-21:35


#from testdata import *
import sys, math

from Ui_AnimationView import *
from Ui_DockLabel import Ui_DockLabel, Ui_DockWindow

GRID_CENTER = QtCore.QPointF(UNIT_WIDTH/2, UNIT_HEIGHT/2)



class Ui_NewMapUnit(Ui_MapUnit):
    "map unit item used in editor"
    def __init__(self, pos, mapGrid, parent = None):
        Ui_MapUnit.__init__(self, pos, mapGrid, parent)
        self.__mapGrid = mapGrid
        self.__selected = False # specially for mirror!
        # map grid data

    def GetData(self):
        "get data restored in the item"
        return self.__mapGrid

    def ChangeTerrain(self, terrain):
        "change terrain in data and item"
        if (terrain==MIRROR):
            self.SpTerrainHandler_mirror()
        else:
            self.__mapGrid = MAP_BASE[terrain](terrain)
            self.terrain = terrain
        self.update()

    def SpTerrainHandler_mirror(self):
        "sp proposing of sp terrains"
        if (self.spTerrainData[MIRROR]==[]):
            self.spTerrainData[MIRROR].append(self)
            self.__selected = True
        else:
            self.__mapGrid = MAP_BASE[MIRROR](MIRROR,
                                            self.spTerrainData[MIRROR][0].MapPos())
            self.terrain = MIRROR
            self.spTerrainData[MIRROR][0].__selected = False
            self.spTerrainData[MIRROR].pop()
        # first select a place where the mirror goes out, and then select where
        # the mirror places. when using this function, don't use the symmetry!

    def DisplayItem(self):
        "item used for display"
        if (self.terrain==MIRROR):
            return Ui_ExitCursor(self.__mapGrid.out)

    def DragStopEvent(self, args):
        dragUnit, info = args
        dragUnit.setPos(info.nowCoor-DRAG_SPOT)
        # handles the drag move event
        dragUnit.unsetCursor()
        # unset the cursor
        return True

    def paint(self, painter, option, widget):
        Ui_MapUnit.paint(self, painter, option, widget)
        pen = QtGui.QPen()
        pen.setWidth(0)
        pen.setColor(QtGui.QColor(127, 127, 127))
        painter.setPen(pen)
        painter.drawLine(self.boundingRect().topLeft(), self.boundingRect().topRight())
        painter.drawLine(self.boundingRect().bottomLeft(), self.boundingRect().bottomRight())
        painter.drawLine(self.boundingRect().topLeft(), self.boundingRect().bottomLeft())
        painter.drawLine(self.boundingRect().topRight(), self.boundingRect().bottomRight())
        if (self.__selected): # sp terrain display
            brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
            brush.setColor(QtGui.QColor(255, 0, 0, 127))
            painter.setBrush(brush)
            painter.setPen(QtGui.QPen(0))
            painter.drawRect(self.boundingRect())
            

    spTerrainData = {MIRROR: []} # a special module for the sp terrains


class Ui_NewSoldierUnit(Ui_SoldierUnit):
    "soldier item used in editor"
    def __init__(self, idNum, unit, parent = None):
        Ui_SoldierUnit.__init__(self, idNum, unit, parent)
        self.__soldier = unit

    def GetData(self):
        "get data restored in the item"
        return self.__soldier

    def ChangeSoldierPos(self, pos):
        "change the soldier pos"
        views = self.scene().views()
        if (views[0].GetSoldierItemAt(pos)!=None):
            self.setPos(self.GetPos())
            return
        # if there is an unit on pos, return
        originPos = self.MapPos()
        self.SetMapPos(pos = pos)
        self.__soldier.position = pos
        if (not self.blockSignal):
            self.emit(QtCore.SIGNAL(self.DATA_CHANGE_SIGNAL),
                      (Ui_NewSoldierUnit.ChangeSoldierPos, originPos, (pos,), (True,)))
        # emit the data-changed signal

    def DisplayItem(self):
        return

    def DragStartEvent(self, info):
        return self
    def DragStopEvent(self, args):
        dragUnit, info = args
        info.accepted = False
        # reject
        dragUnit.setPos(info.nowCoor-DRAG_SPOT)
        # handles the drag move event
        if (dragUnit is not self):
            dragUnit.setCursor(QtCore.Qt.ForbiddenCursor)
        else:
            dragUnit.unsetCursor()
        # the cursor
        return True
    def DragComplete(self, info):
        for item in self.scene().items():
            item.unsetCursor()
        # unset cursor
        if (info.accepted):
            self.ChangeSoldierPos(info.nowPos)
            # set at new pos
        else:
            self.setPos(self.GetPos())
            # go back
    def DragFail(self, info):
        self.unsetCursor()
        self.setPos(self.GetPos())

    DATA_CHANGE_SIGNAL = "unitDataChagned"
    # signal name for data changed. the paremeter is: (func, pos, *args, needToChange)
    blockSignal = False # shows if needs to block the signal, used for avoiding infinite recursion

#units of map editor

LABEL_SIZE = QtCore.QSizeF(200, 124) # size of label
HOVER_REGION_SIZE = QtCore.QSizeF(250, 160) # size of region that accepts hover event
TERRAIN_INFO = ["平原", "山地", "森林", "障碍", "炮塔", "神庙", "镜子", "无"]
SOLDIER_INFO = ["剑士", "枪兵", "弓箭手", "龙骑士", "战士", "牧师", "英雄", "无"]

class Ui_MapEditorDockLabel(Ui_DockLabel):
    "dock label for info display"
    def __init__(self, parent = None):
        Ui_DockLabel.__init__(self, LABEL_SIZE, parent)
        self.__terrainInfo = -1
        self.__soldierInfo = -1
        #self.__spInfo = ""

    def SetInfo(self, terrain, soldier, spInfo = ""):
        "set info displayed"
        self.__terrainInfo = terrain
        self.__soldierInfo = soldier
        self.update()
        #self.__spInfo = spInfo

    def paint(self, painter, option, widget):
        pen = QtGui.QPen()
        pen.setWidth(2)
        pen.setColor(QtGui.QColor(255, 0, 0, 255))
        pen.setStyle(QtCore.Qt.SolidLine)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(0, 0, 255, 150))
        brush.setStyle(QtCore.Qt.SolidPattern)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRoundedRect(1, 1, 198, 122, 5, 5)
        # the edge
        font = QtGui.QFont("Times", 15, QtGui.QFont.Bold)
        pen.setColor(QtGui.QColor(0, 0, 0))
        brush.setColor(QtGui.QColor(0, 0, 0))
        painter.setFont(font)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawText(QtCore.QPointF(20, 50),
                         QtCore.QString.fromUtf8("单位： "+TERRAIN_INFO[self.__terrainInfo]))
        painter.drawText(QtCore.QPointF(20, 110),
                         QtCore.QString.fromUtf8("兵种： "+SOLDIER_INFO[self.__soldierInfo]))
        # the text

class Ui_ExitCursor(Ui_GridUnit):
    "the unit for displaying exit of mirror"
    def __init__(self, pos, parent = None):
        Ui_GridUnit.__init__(self, pos[0], pos[1], parent)
    def paint(self, painter, option, widget):
        pen = QtGui.QPen()
        pen.setWidth(5)
        pen.setColor(QtGui.QColor(0, 255, 0))
        pen.setCapStyle(QtCore.Qt.FlatCap)
        painter.setPen(pen)

        RMARGIN = 0.05 #rate of margin
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT),
                         QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT),
                         QtCore.QPointF(RMARGIN*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT))
       # the shape is a square

# info display

class Ui_MapEditor(Ui_FocusControllingView):
    "display widget in map editor"
    def __init__(self, scene, parent = None):
        Ui_FocusControllingView.__init__(self, scene, parent)
        self.newMapItem = []
        self.newUnitsItem = [[], []]
        self.__isClean = True
        # item of new map with data
        self.__terrainType = None # the currently selected terrain type
        self.__soldierType = None # the currently selected soldier type
        self.__soldierSide = 0 # the currently selected soldier side
        self.__symmType = self.NO_SYMMETRY # the symmetry type of map
        self.__symmFunc = (None,
                           self.GetHorizSymmetricPosOf,
                           self.GetVertiSymmetricPosOf,
                           self.GetCentroSymmetricPosOf)
        # available func used to get the func for finding symm pos's
        self.EditMapMode() # the mode of editor
        self.focusGridChange.connect(self.__focusChanged)
        self.setMouseTracking(True)
        # default settings
        self.__dockWindow = None
        # dockWindow
        self.__mapDispItem = None
        self.__unitDispItem = None

    def SetClean(self):
        self.__isClean = True
        
    def __defaultState(self):
        "renew the state"
        self.__isClean = True
        self.__terrainType = None
        self.__soldierType = None
        self.__soldierSide = 0
        self.__symmType = self.NO_SYMMETRY
        self.EditMapMode()
        # default parameter
        label = Ui_MapEditorDockLabel()
        self.__dockWindow = Ui_DockWindow(label, HOVER_REGION_SIZE, self)
        self.scene().addItem(self.__dockWindow)
        self.RegisterDockItem(self.__dockWindow)
        self.__mapDispItem = None
        self.__unitDispItem = None
        # items
        # caution: renew the widget when calling it!

    def NewMap(self, x = 0, y = 0):
        "new a map with size (x, y). the initial terrain is PLAIN."
        self.Initialize(x, y)
        self.newMapItem = []
        for i in range(x):
            newColumn = []
            for j in range(y):
                item = Ui_NewMapUnit((i, j), MAP_BASE[PLAIN](PLAIN))
                self.addItem(item, Ui_NewMapUnit.FLOOR_IN_VIEW)
                newColumn.append(item)
            self.newMapItem.append(newColumn)
        # new map data
        self.newUnitsItem = [[], []]
        # new soldier data
        self.__defaultState()
        self.__isClean = False

    def LoadMap(self, maps, units):
        "load map items from file"
        self.Initialize(len(maps), len(maps[0]))
        # data update
        self.newMapItem = []
        self.newUnitsItem = [[], []]
        for i in range(len(maps)):
            column = []
            for j in range(len(maps[0])):
                item = Ui_NewMapUnit((i, j), maps[i][j])
                self.addItem(item, Ui_NewMapUnit.FLOOR_IN_VIEW)
                column.append(item)
            self.newMapItem.append(column)
#                self.connect(item, QtCore.SIGNAL(Ui_NewSoldierUnit.DATA_CHANGE_SIGNAL),
#                             self.__changeSymmetricUnitData)
        for i in (0, 1):
            for j in range(len(units[i])):
                item = Ui_NewSoldierUnit((i, j), units[i][j])
                item.setEnabled(False)
                self.addItem(item, Ui_NewSoldierUnit.FLOOR_IN_VIEW)
                self.newUnitsItem[i].append(item)
                self.connect(item, QtCore.SIGNAL(Ui_NewSoldierUnit.DATA_CHANGE_SIGNAL),
                             self.__changeSymmetricUnitData)
        # new items and connecting
        self.__defaultState()
        ## not completely tested

    def GetMapData(self):
        "return the data of the new map"
        newMap = []
        newUnits = []
        getData = lambda item: item.GetData()
        for column in self.newMapItem:
            newMap.append(map(getData, column))
        for column in self.newUnitsItem:
            newUnits.append(map(getData, column))
        return newMap, newUnits

    def IsClean(self):
        return self.__isClean

    def ChangeTerrain(self, terrain = None):
        "change the current terrain type and set the view map-editing mode"
        self.__terrainType = terrain
        self.EditMapMode()
    def ChangeSoldierType(self, soldier = None):
        "change the current soldier type and set the view soldier-adding mode"
        self.__soldierType = soldier
        self.AddUnitMode()
    def ChangeSoldierSide(self, side = 0):
        "change the current soldeir side"
        self.__soldierSide = side

    def AddUnit(self, pos):
        "add unit at pos, return a bool showing if valid"
        if (self.__soldierType==None):
            return False
        soldier = Base_Unit(self.__soldierType, pos)
        idNum = (self.__soldierSide, len(self.newUnitsItem[self.__soldierSide]))
        # new soldier data
        if (self.GetSoldierItemAt(pos)!=None):
            return False
        else:
            item = Ui_NewSoldierUnit(idNum, soldier)
            item.setEnabled(False) # set it disabled to avoid dragging
            self.addItem(item, Ui_NewSoldierUnit.FLOOR_IN_VIEW)
            self.newUnitsItem[idNum[0]].append(item)
            self.connect(item, QtCore.SIGNAL(Ui_NewSoldierUnit.DATA_CHANGE_SIGNAL),
                         self.__changeSymmetricUnitData)
        # new soldier item and connecting
        self.__isClean =False
        return True
        
    def DelUnit(self, pos):
        "remove unit at pos, return a bool showing if valid."
        if (self.GetSoldierItemAt(pos)==None):
            return False
        else:
            item = self.GetSoldierItemAt(pos)
            self.newUnitsItem[item.idNum[0]].remove(item)
            self.removeItem(item)
            self.__isClean = False
            return True
        # remove item
            

    def GetMapItemAt(self, pos):
        "get the map item at pos"
        try:
            return self.unitMap[(pos, Ui_NewMapUnit.FLOOR_IN_VIEW)]
        except KeyError:
            return None
    def GetSoldierItemAt(self, pos):
        "get the soldier item at pos"
        try:
            return self.unitMap[(pos, Ui_NewSoldierUnit.FLOOR_IN_VIEW)]
        except KeyError:
            return None

    def EditMapMode(self):
        "map editing...."
        self.__mode = self.MAP_EDITING_MODE
        for item in self.scene().items():
            if (item.__class__ is Ui_NewSoldierUnit):
                item.SetUiEnabled(False)
        # set soldiers disabled
    def EditUnitMode(self):
        "soldier editing..."
        self.__mode = self.UNITS_EDITING_MODE
        for item in self.scene().items():
            if (item.__class__ is Ui_NewSoldierUnit):
                item.SetUiEnabled(True)
        # set solders enabled
    def AddUnitMode(self):
        "soldier adding..."
        self.__mode = self.UNITS_ADDING_MODE
        for item in self.scene().items():
            if (item.__class__ is Ui_NewSoldierUnit):
                item.setEnabled(False)
        # set soldiers disabled
    def DeleteUnitMode(self):
        "soldier deleting..."
        self.__mode = self.UNITS_DELETING_MODE
        for item in self.scene().items():
            if (item.__class__ is Ui_NewSoldierUnit):
                item.setEnabled(False)
        # set soldiers disabled
    def __changeMode(self, mode):
        "change mode"
        self.__mode = mode
    # function to change the mode

    MAP_EDITING_MODE = 100
    SP_TERRAIN_EDITING_MODE = 101
    UNITS_EDITING_MODE = 150
    UNITS_ADDING_MODE = 151
    UNITS_DELETING_MODE = 152
    # mode of editing

    def SetSymmetry(self, symmType = 0):
        "set the symmmetry type of map"
        self.__symmType = symmType

    def GetVertiSymmetricPosOf(self, pos):
        return (pos[0], self.mapSize[1]-1-pos[1])
    def GetHorizSymmetricPosOf(self, pos):
        return (self.mapSize[0]-1-pos[0], pos[1])
    def GetCentroSymmetricPosOf(self, pos):
        return (self.mapSize[0]-1-pos[0], self.mapSize[1]-1-pos[1])
    # func for getting point symmetric to a given point

    NO_SYMMETRY = 0
    VERITCAL_SYMMETRY = 2
    HORIZONTAL_SYMMETRY = 1
    CENTRO_SYMMETRY = 3

    def __changeSymmetricUnitData(self, change):
        "connected with signal unitDataChanged. modify the symmetric unit's data"
        #print "symm called"#for test
        self.__isClean = False
        symmFunc = self.__symmFunc[self.__symmType]
        if (symmFunc!=None):
            func, originPos, args, needToChange = change
            pos = symmFunc(originPos)
            unit = self.GetSoldierItemAt(pos)
            if (unit==None or unit is self.sender() or pos==originPos):
                return
            # when no unit lies on the symm pos || unit moves to its symm pos, return
            symmChange = lambda x, f: (f and symmFunc(x)) or x
            newArgs = map(symmChange, args, needToChange)
            # get new args
            #print self.sender().MapPos()#for test
            #print unit#for test
            #print unit.MapPos()#for test
            Ui_NewSoldierUnit.blockSignal = True
            # to avoid infinite recursion
            apply(func, [unit,]+list(newArgs))
            # change the data of symmetric unit
            Ui_NewSoldierUnit.blockSignal = False
    ## the behavior of the symmetry is obscure, the user need be given more implications.
    # symmetry

    def mousePressEvent(self, event):
        info = self.MouseEventHandler(event)
        # customed view event handler
        if (info.isValid):
            self.SetFocusGrid(QtCore.QPoint(info.nowPos[0], info.nowPos[1]))
        # set focus
        QtGui.QGraphicsView.mousePressEvent(self, event)
    def mouseReleaseEvent(self, event):
        info = self.MouseEventHandler(event)
        QtGui.QGraphicsView.mouseReleaseEvent(self, event)
    def mouseMoveEvent(self, event):
        info = self.MouseEventHandler(event)
        QtGui.QGraphicsView.mouseMoveEvent(self, event)
    # mouse event

    #need a clear function to clear the selected state?
    #DATA_DIRTY = False

    def __focusChanged(self, pos):
        "slot of signal focus_changed"
        self.ShowCursor((pos.x(), pos.y())) # show the cursor at the focus grid
        self.__changeData(pos)
        self.__displayInfo(pos)
    def __changeData(self, pos):
        "modify data"
        if (self.__mode==self.MAP_EDITING_MODE):
            if (self.__terrainType!=None):
                self.GetMapItemAt((pos.x(), pos.y())).ChangeTerrain(self.__terrainType)
                self.__isClean = False
                # change terrain
                func = self.__symmFunc[self.__symmType]
                if (func!=None):
                    self.GetMapItemAt(func((pos.x(), pos.y()))).ChangeTerrain(self.__terrainType)
                # the symmetry
        elif (self.__mode==self.UNITS_ADDING_MODE):
            if (not self.AddUnit((pos.x(), pos.y()))):
                QtGui.QMessageBox.warning(self, QtCore.QString("Error!"),
                                          QtCore.QString("Cannot add a soldier here."))
                return
            # add units
            func = self.__symmFunc[self.__symmType]
            if (func!=None and func((pos.x(), pos.y()))!=(pos.x(), pos.y())):
                self.__soldierSide = 1-self.__soldierSide
                if (not self.AddUnit(func((pos.x(), pos.y())))):
                    QtGui.QMessageBox.warning(self, QtCore.QString("Error!"),
                                              QtCore.QString("Cannot add a soldier at the point symmetric to the selected point."))
                self.__soldierSide = 1-self.__soldierSide
            # the symmetry
        elif (self.__mode==self.UNITS_DELETING_MODE):
            if (not self.DelUnit((pos.x(), pos.y()))):
                QtGui.QMessageBox.warning(self, QtCore.QString("Error!"),
                                          QtCore.QString("No units lie here."))
            # delete units
            func = self.__symmFunc[self.__symmType]
            if (func!=None):
                self.DelUnit(func((pos.x(), pos.y())))
            # the symmetry
    def __displayInfo(self, pos):
        "display info"
        mapItem = self.GetMapItemAt((pos.x(), pos.y()))
        terrain = mapItem.terrain
        soldierItem = self.GetSoldierItemAt((pos.x(), pos.y()))
        if (soldierItem==None):
            soldier = -1
        else:
            soldier = soldierItem.type
        self.__dockWindow.label.SetInfo(terrain, soldier)
        # show dock label
        self.__mapDispItem and self.scene().removeItem(self.__mapDispItem)
        self.__unitDispItem and self.scene().removeItem(self.__unitDispItem)
        self.__mapDispItem = mapItem.DisplayItem()
        if (self.__unitDispItem):
            self.__unitDispItem = soldierItem.DisplayItem()
        self.__mapDispItem and self.scene().addItem(self.__mapDispItem)
        self.__unitDispItem and self.scene().addItem(self.__unitDispItem)
        # display items
