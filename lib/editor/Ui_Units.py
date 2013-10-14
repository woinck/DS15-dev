# -*- coding: utf-8 -*-


#edited at 2013-10-03-21:44

"""
the module of basic units in game ui.
classes:
    Ui_GridUnit
    Ui_SoldierUnit
    Ui_MapUnit
    Ui_Cursor
    Ui_GridLabel
    Ui_CustomedView
funtions:
    GetPos()
    GetGrid()
constances:
    UNIT_WIDTH
    UNIT_HEIGHT
"""

from PyQt4 import QtGui, QtCore
from basic import *



AVAILABLE_TERRAIN = (PLAIN, MOUNTAIN, FOREST, BARRIER, TURRET, TEMPLE, MIRROR)
MAP_BASE = (Map_Basic, Map_Basic, Map_Basic, Map_Basic, Map_Turret, Map_Temple, Map_Mirror)

AVAILABLE_UNIT_TYPE = (SABER, LANCER, ARCHER, DRAGON_RIDER, WARRIOR, WIZARD,
                       HERO_1, HERO_2, HERO_3)
AVAILABLE_HERO_TYPE = (HERO_1, HERO_2, HERO_3)

MAP_IMAGE_ROUTE = (":plain.png",
                   ":mountain.png",
                   ":forest.png",
                   ":barrier.png",
                   ":turret.png",
                   ":temple.png",
                   ":mirror.png")
SOLDIER_IMAGE_ROUTE = (":saber0.png",
                       ":lancer0.png",
                       ":archer0.png",
                       ":dragon_rider0.png",
                       ":warrior0.png",
                       ":wizard0.png",
                       ":hero_10.png",
                       ":hero_20.png",
                       ":hero_30.png")

SOLDIER_IMAGE_ROUTE2 = (":saber1.png",
                       ":lancer1.png",
                       ":archer1.png",
                       ":dragon_rider1.png",
                       ":warrior1.png",
                       ":wizard1.png",
                       ":hero_11.png",
                       ":hero_21.png",
                       ":hero_31.png")

# types of map grid, unit defined by ui

UNIT_WIDTH = 28 # width of map grids(1st dimension)
UNIT_HEIGHT = 28 # height of map grids(2nd dimension)
PEN_WIDTH = 0.5 # pen width
LABEL_WIDTH = 100 # width of labels for displaying
LABEL_HEIGHT = 30 # height of labels for displaying
MARGIN_WIDTH = 20 # width of the margin of the display window
LABEL_LEFT_MARGIN = 26 # distance between the item origin and the downleft corner of labels

BACKGROUND_COLOR = QtGui.QColor(255, 255, 255, 255) # the background color

DRAG_SPOT = QtCore.QPoint(40, 40) # the spot of dragging
GRID_CENTER = QtCore.QPointF(UNIT_WIDTH/2, UNIT_HEIGHT/2)
# the center of the grid, for the convenience of calculating
LEAST_PRESS_TIME_FOR_DRAG = 200 # if the time you press the mouse button is less than it,
                               # no customed DAD event will be triggered.

# some constants

####################################################################

def GetPos(mapX = 0, mapY = 0, pos = None):
    "convert the map grid coord. to scene coord."
    if (pos!=None):
        return GetPos(pos[0], pos[1])
    return QtCore.QPointF(mapX*UNIT_WIDTH, mapY*UNIT_HEIGHT)
def GetGrid(corX = 0, corY = 0, pos = None):
    "convert the scene coord. to the map grid coord."
    if (pos!=None):
        return GetGrid(pos.x(), pos.y())
    x = int(corX/UNIT_WIDTH)
    y = int(corY/UNIT_HEIGHT)
    return x, y

class Ui_GridUnit(QtGui.QGraphicsObject):
    def __init__(self, x = 0, y = 0, parent = None):
        QtGui.QGraphicsObject.__init__(self, parent)
        self.__mapX = x
        self.__mapY = y
        # map grid coord.
        self.floorInView = None # z value, if None, the unit isn't added in the view map
        self.selection = False # about the seleted state, default None
        self.SetMapPos(x, y)

    def MapPos(self):
        "return its map pos"
        return self.__mapX, self.__mapY
    def SetMapPos(self, x = 0, y = 0, pos = None):
        "set its map pos pos and the actual position"
        if (pos!=None):
            return self.SetMapPos(pos[0], pos[1])
        oldX, oldY = self.__mapX, self.__mapY
        self.__mapX = x
        self.__mapY = y
        self.setPos(self.GetPos())
        self.mapPosChanged.emit(oldX, oldY)
    mapPosChanged = QtCore.pyqtSignal(int, int)
    # notifies the change of map pos, telling the original pos of the unit
    # (if you want to get the new pos, use MapPos())
    
    def GetPos(self):
        "get its scene pos"
        return GetPos(self.__mapX, self.__mapY)

    def SetUiEnabled(self, flag):
        self.setVisible(flag)
        self.setEnabled(flag)
    def IsUiEnabled(self):
        return (self.isVisible() and self.isEnabled())
    enability = QtCore.pyqtProperty(bool, fget = IsUiEnabled,
                                    fset = SetUiEnabled)
    # the state of enability, deciding whether the unit accepts the customed event

    def boundingRect(self):
        return QtCore.QRectF(0-PEN_WIDTH, 0-PEN_WIDTH,
                             UNIT_WIDTH+PEN_WIDTH, UNIT_HEIGHT+PEN_WIDTH)
        #regard the upleft corner as origin
    def paint(self, painter, option, widget):
        pass

    def MousePressEvent(self, args):
        return False
    def MouseEnterEvent(self, args):
        return False
    def MouseLeaveEvent(self, args):
        return False
    def MouseReleaseEvent(self, args):
        return False
    def DragStartEvent(self, args):
        return None
    def DragStopEvent(self, args):
        return False
    def DragComplete(self, args):
        pass
    def DragFail(self, args):
        self.setPos(self.GetPos())
    #customed event processor



class Ui_MouseInfo:
    def __init__(self, mapSize, event, lastEvent = None):
        self.isValid = True
        self.nowCoor = Ui_CustomedView.view.mapToScene(event.pos()) # scene coord.
        if (lastEvent!=None):
            self.initPos = lastEvent.nowPos # the pos of the last event
        else:
            self.initPos = None
        self.nowPos = GetGrid(self.nowCoor.x(), self.nowCoor.y()) # pos of the new event
        if (self.nowPos[0]<0 or self.nowPos[1]<0 or
            self.nowPos[0]>=mapSize[0] or self.nowPos[1]>=mapSize[1]):
            # if the event happens out of the map:
            self.nowPos = self.initPos
            self.isValid = False
        self.eventType = event.type()
        self.eventButton = event.button()
        self.accepted = True # whether the event is accepted(used in DAD)
        if (lastEvent==None):
            self.validPress = None
        else:
            self.validPress = lastEvent.validPress # the pos of valid press or None if not pressing
        if (event.type()==QtCore.QEvent.MouseButtonPress and self.isValid):
            self.validPress = self.nowPos
        elif (event.type()==QtCore.QEvent.MouseButtonRelease):
            if (self.validPress==None):
                # if mouse releases while the press is not valid
                self.isValid = False
            self.validPress = None

class Ui_CustomedView(QtGui.QGraphicsView):
    def __init__(self, scene, floorNum = 4, parent = None):
        QtGui.QGraphicsView.__init__(self, scene, parent)
        if (Ui_CustomedView.view!=None):
            raise AttributeError, "more than one views are built."
        else:
            Ui_CustomedView.view = self
        # make sure only one view is in use
        self.unitMap = {} # its keys is (pos, floor)
        self.mapSize = (0, 0)
        # map info, unit info
        self.__maxFloor = floorNum # max num of floors
        self.__lastEventInfo = None # the last valid mouse event
        self.__dragUnit = None
        # drag event processor
        self.__dragTimerId = None
    def __del__(self):
        Ui_CustomedView.view = None
        QtGui.QGraphicsView.__del__(self)#?
    
    def RaiseEvent(self, pos, eventType, args):
        "customed event passing"
        for i in range(self.__maxFloor-1, -1, -1):
            try:
                if (not self.unitMap[(pos, i)].IsUiEnabled()):
                    continue
                if (eventType==self.MOUSE_PRESS_EVENT):
                    result = self.unitMap[(pos, i)].MousePressEvent(args)
                elif (eventType==self.MOUSE_RELEASE_EVENT):
                    result = self.unitMap[(pos, i)].MouseReleaseEvent(args)
                elif (eventType==self.ENTER_EVENT):
                    result = self.unitMap[(pos, i)].MouseEnterEvent(args)
                elif (eventType==self.LEAVE_EVENT):
                    result = self.unitMap[(pos, i)].MouseLeaveEvent(args)
                elif (eventType==self.DRAG_START_EVENT):
                    result = self.unitMap[(pos, i)].DragStartEvent(args)
                elif (eventType==self.DRAG_STOP_EVENT):
                    result = self.unitMap[(pos, i)].DragStopEvent(args)
                if (result):
                    return result
            except KeyError:
                pass
        return None
    def MouseEventHandler(self, event):
        "handles the customed mouse event and DAD event"
        info = Ui_MouseInfo(self.mapSize, event, self.__lastEventInfo)
        self.__lastEventInfo = info

        if (info.eventType==QtCore.QEvent.MouseButtonPress and
            info.eventButton==QtCore.Qt.LeftButton and info.isValid):
            self.RaiseEvent(info.nowPos, self.MOUSE_PRESS_EVENT, info)
            # mouse press event
        elif (info.eventType==QtCore.QEvent.MouseButtonRelease and
              info.eventButton==QtCore.Qt.LeftButton and info.isValid):
            self.RaiseEvent(info.nowPos, self.MOUSE_RELEASE_EVENT, info)
            # mouse release event
        elif (info.eventType==QtCore.QEvent.MouseMove and info.isValid):
            if (info.initPos!=info.nowPos):
                self.RaiseEvent(info.initPos, self.LEAVE_EVENT, info)
                self.RaiseEvent(info.nowPos, self.ENTER_EVENT, info)
            # mouse enter event, mouse release event
        # processing mouse event

        if (info.eventType==QtCore.QEvent.MouseButtonPress and
            info.eventButton==QtCore.Qt.LeftButton and info.isValid):
            self.__dragUnit = self.RaiseEvent(info.nowPos, self.DRAG_START_EVENT, info)
            if (self.__dragUnit!=None):
                self.__dragTimerId = self.startTimer(LEAST_PRESS_TIME_FOR_DRAG)
            # drag start event
        elif (info.eventType==QtCore.QEvent.MouseButtonRelease and
              info.eventButton==QtCore.Qt.LeftButton):
            if (self.__dragUnit!=None and self.__dragTimerId==None):
                if (self.RaiseEvent(info.nowPos, self.DRAG_STOP_EVENT, (self.__dragUnit, info))
                    and info.accepted):
                    self.__dragUnit.DragComplete(info)
                else:
                    self.__dragUnit.DragFail(info)
            if (self.__dragTimerId!=None):
                self.__dragTimerId = self.killTimer(self.__dragTimerId)
            self.__dragUnit = None
            # drag stop event, reset the drag unit
        elif (info.eventType==QtCore.QEvent.MouseMove and info.isValid):
            if (self.__dragUnit!=None and self.__dragTimerId==None):
                self.RaiseEvent(info.nowPos, self.DRAG_STOP_EVENT, (self.__dragUnit, info))
            #drag move event
        # processing DAD event
        self.scene().update()
        return info

    def addItem(self, item, floor = None):
        "overload, add items to scene and arrange them in the unit map"
        if (floor!=None and 0<=floor<self.__maxFloor):
            try:
                self.unitMap[(item.MapPos(), floor)]
                raise IndexError, "more than one units in "+str((item.MapPos(), floor))
            # no more than one units allowed in one place
            except:
                self.unitMap[(item.MapPos(), floor)] = item
                item.floorInView = floor
                item.mapPosChanged.connect(self.__updateMap)
                # add in the unit map
        self.scene().addItem(item)
    def removeItem(self, item):
        "overload, delete items in scene and its index in the unit map"
        try:
            if (self.unitMap[(item.MapPos(), item.floorInView)] is item):
                del self.unitMap[(item.MapPos(), item.floorInView)]
                item.floorInView = None
                item.mapPosChanged.disconnect(self.__updateMap)
                # remove the index
        except KeyError:
            pass
        self.scene().removeItem(item)
    def __updateMap(self, mapX, mapY):
        "update the index when the pos of units changes"
        floor = self.sender().floorInView
        if (floor!=None):
            try:
                if (self.unitMap[(mapX, mapY), floor] is self.sender()):
                    del self.unitMap[(mapX, mapY), floor]
            except KeyError:
                pass
            # delete the index before
            self.unitMap[self.sender().MapPos(), floor] = self.sender()
            # add the new index
    def CheckIndex(self, item):
        "check if the index of the item is right. just in case"
        try:
            return (self.unitMap[(item.MapPos(), item.floorInView)] is item)
        except KeyError:
            return False

    def Initialize(self, mapSizeX, mapSizeY):
        "initialize"
        for item in self.scene().items():
            self.scene().removeItem(item)
        # clear the original items
        self.mapSize = (mapSizeX, mapSizeY)
        self.unitMap.clear()
        sizeX = mapSizeX*UNIT_WIDTH
        sizeY = mapSizeY*UNIT_HEIGHT
        self.scene().setSceneRect(0-MARGIN_WIDTH, 0-MARGIN_WIDTH,
                                  sizeX+2*MARGIN_WIDTH, sizeY+2*MARGIN_WIDTH)
        # set the scene's region
        self.setBackgroundBrush(BACKGROUND_COLOR)
        # set the background color white

    def timerEvent(self, event):
        # timer for drag event
        if (self.__dragUnit!=None and event.timerId()==self.__dragTimerId):
            self.killTimer(self.__dragTimerId)
            self.__dragTimerId = None
        QtGui.QGraphicsView.timerEvent(self, event)

    
    view = None # the current view
    MOUSE_PRESS_EVENT = 1
    MOUSE_RELEASE_EVENT = 2
    DRAG_START_EVENT = 3
    DRAG_STOP_EVENT = 4
    LEAVE_EVENT = 5
    ENTER_EVENT = 6
    # event types

# structure of custumed view and item

####################################################################

class Ui_MapUnit(Ui_GridUnit):
    "the basic unit of the map."
    def __init__(self, pos, mapGrid, parent = None):
        Ui_GridUnit.__init__(self, pos[0], pos[1], parent)
        self.terrain = mapGrid.kind

    def paint(self, painter, option, widget):
        pixmap = QtGui.QPixmap(MAP_IMAGE_ROUTE[self.terrain])
        painter.drawPixmap(self.boundingRect().toRect(), pixmap, pixmap.rect())

    FLOOR_IN_VIEW = 0
    # default floor of this type of item

class Ui_SoldierUnit(Ui_GridUnit):
    "the basic unit of the soldiers."
    def __init__(self, idNum, unit, parent = None):
        Ui_GridUnit.__init__(self, unit.position[0], unit.position[1], parent)
        self.type = unit.kind
        self.idNum = idNum

    def paint(self, painter, option, widget):
        if self.idNum[0] == 0:
            pixmap = QtGui.QPixmap(SOLDIER_IMAGE_ROUTE[self.type])
        else:
            pixmap = QtGui.QPixmap(SOLDIER_IMAGE_ROUTE2[self.type])
        painter.drawPixmap(self.boundingRect().toRect(), pixmap, pixmap.rect())

    FLOOR_IN_VIEW = 1
    # default floor of this type of item

class Ui_Cursor(Ui_GridUnit):
    "the basic unit of the cursor"
    def paint(self, painter, option, widget):
        pen = QtGui.QPen()
        pen.setWidth(5)
        pen.setCapStyle(QtCore.Qt.FlatCap)
        painter.setPen(pen)

        RMARGIN = 0.05 #rate of margin
        RLINE = 0.4 #rate of line
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF(RMARGIN*UNIT_WIDTH, RLINE*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF(RLINE*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RLINE*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF((1-RLINE)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT),
                         QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RLINE)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT),
                         QtCore.QPointF(RLINE*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RLINE)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT),
                         QtCore.QPointF((1-RLINE)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
       # the shape is like the cursor in FE

    FLOOR_IN_VIEW = 2

class Ui_GridLabel(Ui_GridUnit):
    "used to show info on map grids"
    def __init__(self, text, pos, parent = None):
        Ui_GridUnit.__init__(self, pos[0], pos[1], parent)
        self.text = text

    def boundingRect(self):
        return QtCore.QRectF(LABEL_LEFT_MARGIN-PEN_WIDTH, 0-LABEL_HEIGHT-PEN_WIDTH,
                             LABEL_WIDTH+PEN_WIDTH, LABEL_HEIGHT+PEN_WIDTH)
        #regard the downleft corner as origin

    def paint(self, painter, option, widget):
        font = QtGui.QFont("Times New Roman", 20)
        painter.setFont(font)
        painter.drawText(QtCore.QPointF(LABEL_LEFT_MARGIN, 0), self.text)

# basic types of items

