#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from testdata import *
import sys

from Ui_2DReplaySceneNew import *

class Ui_NewMapUnit(Ui_MapUnit):
    def __init__(self, x, y, mapGrid, parent = None):
        Ui_MapUnit.__init__(self, x, y, mapGrid, parent)
    
    def MousePressEvent(self, info):
        if (self.IsEnabled()):
            self.selected = not self.selected
            return True
        else:
            return False
    def DragStopEvent(self, args):
        dragUnit, info = args
        dragUnit.unsetCursor()
        return True

class Ui_NewSoldierUnit(Ui_GridUnit):
    def __init__(self, pos, side, order, parent = None):
        Ui_GridUnit.__init__(self, pos[0], pos[1], parent)
        self.side = side
        self.order = order
    def paint(self, painter, option, widget):
        painter.drawRect(10, 10, 50, 50)#for test

    def DragStartEvent(self, info):
        if (self.IsEnabled):
            return self
    def DragStopEvent(self, args):
        dragUnit, info = args
        info.eventAccept = False
        if (dragUnit is not self):
            dragUnit.setCursor(QtCore.Qt.ForbiddenCursor)
        else:
            dragUnit.unsetCursor()
        return True
    def DragComplete(self, info):
        for item in self.scene().items():
            item.unsetCursor()
        if (info.eventAccept):
            self.SetMapPos(info.nowPos[0], info.nowPos[1])
        else:
            self.setPos(self.GetPos())
    def DragFail(self, info):
        self.unsetCursor()
        self.setPos(self.GetPos())
            
        
#units of map editor



class Ui_MapEditor(Ui_ReplayView):
    "display widget in map editor. \
    data: \
    newMap : Map \
    iniUnits : array of Units"
    def __init__(self, scene, parent = None):
        Ui_ReplayView.__init__(self, scene, parent)
        self.newMap = []
        #self.usableGrid = []
        self.iniUnits = [[], []]
        self.setAcceptDrops(True)

    def Initialize(self, x = 0, y = 0):
        "Initialize(int x = 0, int y = 0) -> void \
        create a new map(default terrain: PLAIN). \
        x and y is the size of the map. "
        self.newMap = []
        i = 0
        #self.usableGrid = []
        while (i<x):
            j = 0
            newColumn = []
            while (j<y):
                newColumn.append(Map_Basic(PLAIN))
                j += 1
            self.newMap.append(newColumn)
            i += 1
        Ui_ReplayView.Initialize(self, self.newMap, [], 0,
                                 Ui_NewMapUnit)
        self.iniUnits = [[], []]

    def ChangeTerrain(self, terrain):
        "ChangeTerrain(enum TERRAIN terrain) -> void \
        change the terrain of selected map grids "
        for i in range(len(self.newMap)):
            for j in range(len(self.newMap[i])):
                if (self.mapItem[i][j].selected):
                    self.mapItem[i][j].terrain = terrain
                    self.newMap[i][j] = Map_Basic(terrain)
                    self.mapItem[i][j].selected = False
        self.scene().update()

    def AddUnit(self, side, position = None):
        "AddUnit(enum(0, 1) side, Coord. position = None) -> Coord. newPos \
        add a new unit to a certain side returning the position it will placed at. \
        position indicates where the new unit should be set. \
        if it is None, a valid and random position will be distributed. \
        error will be raised if the position is invalid."
        usedGrid = []
        for s in (0, 1):
            usedGrid.extend(map(lambda unit: (unit.mapX, unit.mapY),
                                self.iniUnits[s]))
        if (position==None):
            for pos in [(i, j) for i in range(self.mapSize[0])
                        for j in range(self.mapSize[1])]:
                if (pos not in usedGrid):
                    usableGrid = pos
                    break
            else:
                raise Ui_Error, ("AddUnitError_0",
                                 ("class Ui_MapEditor", "func AddUnit"),
                                 "无合法的格点。")
        else:
            if (position not in usedGrid):
                usableGrid = position
            else:
                raise Ui_Error, ("AddUnitError_1",
                                 ("class Ui_MapEditor", "func AddUnit"),
                                 "所选格点不合法，或已有单位存在。")
        newUnit = Ui_NewSoldierUnit(usableGrid,
                                    side, len(self.iniUnits[side]))
        newUnit.setPos(newUnit.GetPos())
        self.AddItem(newUnit)
        self.iniUnits[side].append(newUnit)
        #self.scene().update()
        return usableGrid
    def DelUnit(self, side):
        "DelUnit(enum(0, 1) side) -> Coord. pos \
        delete the last unit of a certain side returning the position it was placed at. \
        error will be raised if no units is in this side."
        if (self.iniUnits[side]):
            delUnit = self.iniUnits[side].pop(-1)
            self.RemoveItem(delUnit)
            pos = (delUnit.mapX, delUnit.mapY)
            #self.scene().update()
            return pos
        else:
            raise Ui_Error, ("DelUnitError",
                             ("class Ui_MapEditor", "func DelUnit"),
                             "无可删除的单位。")

    def EditMapMode(self):
        "EditMapMode() -> void \
        set the widget in the map-editing mode."
        for column in self.mapItem:
            for item in column:
                item.SetEnabled(True)
        for side in (0, 1):
            for unit in self.iniUnits[side]:
                unit.SetEnabled(False)
    def EditUnitMode(self):
        "EditUnitMode() -> void \
        set the widget in the unit-placing mode."
        for column in self.mapItem:
            for item in column:
                item.SetEnabled(False)
        for side in (0, 1):
            for unit in self.iniUnits[side]:
                unit.SetEnabled(True)
    #function to change the mode

    #need a clear function to clear the selected state?



if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    scene = QtGui.QGraphicsScene()
    view = Ui_MapEditor(scene)
    view.Initialize(5, 5)
    view.AddUnit(1, (1, 3))
    view.AddUnit(1, (1, 4))
    view.AddUnit(1, (3, 2))
    view.AddUnit(0, (2, 2))
    view.AddUnit(0, (1, 2))#bug
    view.AddUnit(0, (0, 0))
    view.DelUnit(1)

    view.show()
    sys.exit(app.exec_())
