# -*- coding: utf-8 -*-


#edited at 2013-10-03-21:44

from Ui_Units import *
import math



STAFF_TEXT_COLOR = QtGui.QColor(0, 0, 0, 255)
STAFF_EDGE_COLOR = QtGui.QColor(0, 0, 255, 255)
STAFF_FOCUS_BRUSH_COLOR = QtGui.QColor(170, 170, 170, 255)

STAFF_Z_VALUE = 1.0
CORNER_Z_VALUE = 2.0
CURSOR_Z_VALUE = 2.0

TIME_FOR_VIEWPORT_MOVE = 0.7 # the viewport will stop at gridPos
                             # in the last 30% of animation
TIME_PER_STEP = 1000 # time for one-step moving of soldiers
TIME_FOR_WAITING = 500 # the soldier will wait for a period of time
                       # when the animation starts
TIME_FOR_CURSOR = 500 # time for showing the cursor
TIME_FOR_ATTACKING = 2000 # time duration of attacking aniamtion
TIME_FOR_MOVING = 500 # time for the soldier moves to the attack pos
TIME_WHEN_RESETING = 1900 # time when the soldier returns back from the attack pos
TIME_FOR_DYING = 500 # time when the soldier dies

# constants

class Ui_MapStaff(QtGui.QGraphicsItem):
    "the super-class of map staffs"
    def __init__(self, length, parent = None):
        QtGui.QGraphicsItem.__init__(self, parent)
        self.size = length
        self.__focus = None # the focus grid
        self.setZValue(STAFF_Z_VALUE)
    def SetFocusGrid(self, num):
        "sets the focus grid"
        self.__focus = num
        self.update()
    def GetFocusGrid(self):
        "returns the focus grid"
        return self.__focus

class Ui_HorizontalMapStaff(Ui_MapStaff):
    "horizontal staff of the map"
    def __init__(self, length, parent = None):
        Ui_MapStaff.__init__(self, length, parent)
        self.setPos(0, 0-MARGIN_WIDTH) # set its initial pos (upleft corner)
    def boundingRect(self):
        return QtCore.QRectF(0-PEN_WIDTH, 0-PEN_WIDTH,
                             self.size*UNIT_WIDTH+PEN_WIDTH, MARGIN_WIDTH+PEN_WIDTH)
    def paint(self, painter, option, widget):
        font = QtGui.QFont("Times New Roman", 15)
        painter.setFont(font)
        pen = QtGui.QPen()
        pen.setWidth(2)
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        if (self.GetFocusGrid()!=None and 0<=self.GetFocusGrid()<self.size):
            brush.setColor(STAFF_FOCUS_BRUSH_COLOR)
            painter.setBrush(brush)
            painter.drawRect(QtCore.QRect(self.GetFocusGrid()*UNIT_WIDTH, 0,
                                          UNIT_WIDTH, MARGIN_WIDTH))
            # draw to show the focus pos
        brush.setColor(BACKGROUND_COLOR)
        painter.setBrush(brush)
        for i in range(self.size):
            if (i!=self.GetFocusGrid()):
                pen.setColor(STAFF_EDGE_COLOR)
                painter.setPen(pen)
                painter.drawRect(QtCore.QRect(i*UNIT_HEIGHT, 0,
                                              UNIT_WIDTH, MARGIN_WIDTH))
            pen.setColor(STAFF_TEXT_COLOR)
            painter.setPen(pen)
            painter.drawText(QtCore.QPointF((i+0.5)*UNIT_WIDTH, MARGIN_WIDTH), str(i))
            #draw the staff
class Ui_VerticalMapStaff(Ui_MapStaff):
    "vertical staff of the map"
    def __init__(self, length, parent = None):
        Ui_MapStaff.__init__(self, length, parent)
        self.setPos(0-MARGIN_WIDTH, 0) # set its initial pos (upleft corner)
    def boundingRect(self):
        return QtCore.QRectF(0-PEN_WIDTH, 0-PEN_WIDTH,
                             MARGIN_WIDTH+PEN_WIDTH, self.size*UNIT_HEIGHT+PEN_WIDTH)
    def paint(self, painter, option, widget):
        font = QtGui.QFont("Times New Roman", 15)
        painter.setFont(font)
        pen = QtGui.QPen()
        pen.setWidth(2)
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        if (self.GetFocusGrid()!=None):
            brush.setColor(STAFF_FOCUS_BRUSH_COLOR)
            painter.setBrush(brush)
            painter.drawRect(QtCore.QRect(0, self.GetFocusGrid()*UNIT_HEIGHT,
                                          MARGIN_WIDTH, UNIT_HEIGHT))
            # draw to show the focus pos
        brush.setColor(BACKGROUND_COLOR)
        painter.setBrush(brush)
        for i in range(self.size):
            if (i!=self.GetFocusGrid()):
                pen.setColor(STAFF_EDGE_COLOR)
                painter.setPen(pen)
                painter.drawRect(QtCore.QRect(0, i*UNIT_HEIGHT,
                                              MARGIN_WIDTH, UNIT_HEIGHT))
            pen.setColor(STAFF_TEXT_COLOR)
            painter.setPen(pen)
            painter.drawText(QtCore.QPointF(0, (i+0.5)*UNIT_HEIGHT), str(i))
            #draw the staff

class Ui_BlankCorner(QtGui.QGraphicsItem):
    "for the beautification of the staff. lies on the upleft corner of viewport"
    def __init__(self, parent = None):
        QtGui.QGraphicsItem.__init__(self, parent)
        self.setPos(0-MARGIN_WIDTH, 0-MARGIN_WIDTH)
        self.setZValue(CORNER_Z_VALUE)
    def boundingRect(self):
        return QtCore.QRectF(0-PEN_WIDTH, 0-PEN_WIDTH,
                             MARGIN_WIDTH+PEN_WIDTH, MARGIN_WIDTH+PEN_WIDTH)
    def paint(self, painter, option, widget):
        pen = QtGui.QPen()
        pen.setColor(BACKGROUND_COLOR)
        painter.setPen(pen)
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        brush.setColor(BACKGROUND_COLOR)
        painter.setBrush(brush)
        painter.drawRect(QtCore.QRect(0, 0, MARGIN_WIDTH-1, MARGIN_WIDTH-1))

# about the staffs of the map

########################################################################

class Ui_ViewportControllingView(Ui_CustomedView):
    "an advanced view including the control of viewport pos"
    def __init__(self, scene, parent = None):
        Ui_CustomedView.__init__(self, scene, parent = parent)
#        //self.__hStaff = None # the horizontal staff of map
#        //self.__vStaff = None # the vertical staff of map
        self.__dockItem = [] # the items moving along with the viewport

    def Initialize(self, mapSizeX, mapSizeY):
        "initialize"
        Ui_CustomedView.Initialize(self, mapSizeX, mapSizeY)
        self.scene().setSceneRect(QtCore.QRectF(0, 0,
                                                UNIT_WIDTH*mapSizeX, UNIT_HEIGHT*mapSizeY))
        self.centerOn(QtCore.QPointF(0, 0))
        # initialize the viewport pos
#        self.__hStaff = Ui_HorizontalMapStaff(mapSizeX)
#        self.scene().addItem(self.__hStaff)
#        self.__vStaff = Ui_VerticalMapStaff(mapSizeY)
#        self.scene().addItem(self.__vStaff)
#        self.__corner = Ui_BlankCorner()
#        self.scene().addItem(self.__corner)
        # add stuffs
        self.__dockItem = []

    def GetViewportPos(self):
        "get the center of the scene now"
        rect = self.geometry()
        return self.mapToScene(QtCore.QPoint(0, 0))+QtCore.QPointF(rect.width(), rect.height())/2
    def SetViewportPos(self, point):
        "make the scene focus on a point"
        self.centerOn(point)
    viewportPos = QtCore.pyqtProperty(QtCore.QPointF, fget = GetViewportPos,
                                      fset = SetViewportPos)
    # property of focus

    def SetCenterGrid(self, x = 0, y = 0, pos = None):
        "set the focus grid od staffs. interface"
        if (pos!=None):
            return self.SetCenterGrid(pos[0], pos[1])
#        self.__hStaff.SetFocusGrid(x)
#        self.__vStaff.SetFocusGrid(y)

    def ViewportMoveAnimation(self, gridPos, time, beginPos = None):
        "returns an animation of gradual movement of the viewport pos"
        centerAnim = QtCore.QPropertyAnimation(self, "viewportPos")
        centerAnim.setDuration(time)
        if (beginPos!=None):
            centerAnim.setStartValue(GetPos(pos = beginPos)+GRID_CENTER)
        centerAnim.setKeyValueAt(TIME_FOR_VIEWPORT_MOVE, GetPos(pos = gridPos)+GRID_CENTER)
        centerAnim.setEndValue(GetPos(pos = gridPos)+GRID_CENTER)
        return centerAnim

    def RegisterDockItem(self, item):
        "add item in dockItem, making it move along with scene"
        self.__dockItem.append(item)
    def scrollContentsBy(self, dx, dy):
        "control the staff movement"
        Ui_CustomedView.scrollContentsBy(self, dx, dy)
        upleftCorner = self.mapToScene(QtCore.QPoint(0, 0))
        for item in self.__dockItem:
            item and item.setPos(upleftCorner)
        # move the dock items
#        try:
#            self.__hStaff and self.__hStaff.setPos(0, upleftCorner.y())
#            self.__vStaff and self.__vStaff.setPos(upleftCorner.x(), 0)
#            self.__corner and self.__corner.setPos(upleftCorner)
#        except AttributeError:
#            pass
        # move the staffs
        self.scene().update()

class Ui_FocusControllingView(Ui_ViewportControllingView):
    "an advanced view including the function of focus controlling"
    def __init__(self, scene, parent = None):
        Ui_ViewportControllingView.__init__(self, scene, parent)
        self.__focusGrid = (0, 0) # the grid holding the focus
        self.__gridCursor = Ui_Cursor()
        self.__targetCursor = Ui_TargetCursor()
        # the cursors for directing of view, sets them invisible

    def Initialize(self, mapSizeX, mapSizeY):
        Ui_ViewportControllingView.Initialize(self, mapSizeX, mapSizeY)
        self.__gridCursor.setZValue(CURSOR_Z_VALUE)
        self.__targetCursor.setZValue(CURSOR_Z_VALUE)
        self.__gridCursor.SetUiEnabled(False)
        self.__targetCursor.SetUiEnabled(False)
        self.scene().addItem(self.__gridCursor)
        self.scene().addItem(self.__targetCursor)
        # set the cursors invisible
    def GetFocusGrid(self):
        "get the focus grid"
        return QtCore.QPoint(self.__focusGrid[0], self.__focusGrid[1])
    def SetFocusGrid(self, gridPos):
        "set the focus grid"
        self.focusGridChange.emit(gridPos)
        self.__focusGrid = (gridPos.x(), gridPos.y())
        self.SetCenterGrid(pos = self.__focusGrid)

    focusGridChange = QtCore.pyqtSignal(QtCore.QPoint)
    # emited when fset is called, with a parameter of the new focus grid
    focusGrid = QtCore.pyqtProperty(QtCore.QPoint, fget = GetFocusGrid,
                                    fset = SetFocusGrid, notify = focusGridChange)
    #property of the grid holding the focus

    def ShowCursor(self, pos = None):
        "show cursor at pos. if pos==None, show it at the focus grid"
        if (pos==None):
            pos = self.__focusGrid
        self.__gridCursor.SetMapPos(pos = pos)
        self.__gridCursor.SetUiEnabled(True)
    def HideCursor(self):
        "hide the cursor"
        self.__gridCursor.SetUiEnabled(False)
"""
    def FocusChangeAnimation(self, gridPos, time, beginPos = None, cursorType = 0):
        "returns an animation of the focus change (with oprional cursors)"
        centerAnim = self.ViewportMoveAnimation(gridPos, time, beginPos)
        # viewport anim
        focusAnim = BoolAnimation(self, "focusGrid")
        focusAnim.setDuration(time)
        if (beginPos!=None):
            focusAnim.setStartValue(QtCore.QPoint(beginPos[0], beginPos[1]))
        focusAnim.setKeyValueAt(TIME_FOR_VIEWPORT_MOVE,
                                QtCore.QPoint(gridPos[0], gridPos[1]))
        focusAnim.setEndValue(QtCore.QPoint(gridPos[0], gridPos[1]))
        # focus anim
        if (cursorType==self.TYPE_GRID_CURSOR):
            cursor = self.__gridCursor
        elif (cursorType==self.TYPE_TARGET_CURSOR):
            cursor = self.__targetCursor
        cursor.SetMapPos(pos = gridPos)
        posAnim = BoolAnimation(cursor, "pos")
        visAnim = BoolAnimation(cursor, "enability")
        posAnim.setDuration(time)
        visAnim.setDuration(time)
        posAnim.setKeyValueAt(max(time-TIME_FOR_CURSOR, 0)/float(time),
                              cursor.GetPos())
        posAnim.setKeyValueAt(0.999, GetPos(pos = gridPos))
        visAnim.setKeyValueAt(max(time-TIME_FOR_CURSOR, 0)/float(time), True)
        visAnim.setKeyValueAt(0.999, False)
        # cursor anim
        anim = QtCore.QParallelAnimationGroup()
        anim.addAnimation(centerAnim)
        anim.addAnimation(focusAnim)
        anim.addAnimation(posAnim)
        anim.addAnimation(visAnim)
        return anim
    def FocusChangeAnimation_withCursors(self, duration, timelist, gridlist, cursorList):
        raise NotImplementedError

    TYPE_GRID_CURSOR = 1
    TYPE_TARGET_CURSOR = 2
    # enum of cursor types
"""

# advanced views which can control its focus

#######################################################################
"""
class Ui_AnimatedSoldierUnit(Ui_SoldierUnit):
    def MoveAnimation(self, route = None):
        "returns the animation of soldiers moving"
        if (route==None):
            route = (self.MapPos(), )
        # regards the soldier static
        step = len(route)-1
        movAnim = QtCore.QPropertyAnimation(self, "pos")
        duration = TIME_FOR_WAITING+TIME_PER_STEP*step
        movAnim.setDuration(duration)
        movAnim.setStartValue(GetPos(pos = route[0]))
        for i in range(step):
            movAnim.setKeyValueAt(float(i*TIME_PER_STEP+TIME_FOR_WAITING)/duration,
                                  GetPos(pos = route[i+1]))
        movAnim.setEndValue(GetPos(pos = route[-1]))
        return movAnim

    def AttackAnimation(self, targetPos, atkPos = None):
        "returns the animation of soldiers attacking"
        if (atkPos==None):
            atkPos = self.MapPos()
        # regards the soldier static
        DIST = 0.3 # the distance the soldier moves
        r = DIST/math.sqrt((atkPos[0]-targetPos[0])**2+(atkPos[1]-targetPos[1])**2)
        pos = GetPos(pos = atkPos)*(1-r)+GetPos(pos = targetPos)*r
        # the position the soldier stays when attacking. beautification needed.
        atkMovAnim = QtCore.QPropertyAnimation(self, "pos")
        atkMovAnim.setDuration(TIME_FOR_ATTACKING)
        atkMovAnim.setKeyValueAt(0, GetPos(atkPos[0], atkPos[1]))
        atkMovAnim.setKeyValueAt(float(TIME_FOR_WAITING)/TIME_FOR_ATTACKING, GetPos(pos = atkPos))
        atkMovAnim.setKeyValueAt(float(TIME_FOR_MOVING)/TIME_FOR_ATTACKING, pos)
        atkMovAnim.setKeyValueAt(float(TIME_WHEN_RESETING)/TIME_FOR_ATTACKING, pos)
        atkMovAnim.setKeyValueAt(1, GetPos(atkPos[0], atkPos[1]))
        # the effect now:
        # the soldeir will move a small distance to the target's direction
        # and stop at the attack pos, and at last go back to its original pos.
        # when the soldier is at the attack pos, it is time for the damage animation.
        return atkMovAnim

    def MoveAndAttackAnimation(self, route, targetPos):
        "a combination of move and attack"
        anim = QtCore.QSequentialAnimationGroup()
        movAnim = self.MoveAnimation(route)
        atkAnim = self.AttackAnimation(targetPos, route[-1])
        anim.addAnimation(movAnim)
        anim.addAnimation(atkAnim)
        return anim

    def DamagedAnimation():
        raise NotImplementedError

    def DieAnimation():
        "animation of dying"
        dieAnim = Ui_Animation(self, "opacity")
        dieAnim.setDuration(TOTAL_TIME)
        dieAnim.setStartValue(1)
        dieAnim.setEndValue(0)
        return dieAnim

    def SkillAnimation():
        raise NotImplementedError

# animated units
"""
############################################################################

class Ui_TargetCursor(Ui_GridUnit):
    "the cursor used to point out the target. the shape is like []+X"
    def paint(self, painter, option, widget):
        pen = QtGui.QPen()
        pen.setWidth(5)
        pen.setCapStyle(QtCore.Qt.FlatCap)
        painter.setPen(pen)

        RMARGIN = 0.05 #rate of margin
        RLINE = 0.4 #rate of line
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))

class BoolAnimation(QtCore.QPropertyAnimation):
    "animation with a customed interpolator of leaping"
    def __init__(self, widget = None, prop = ""):
        QtCore.QPropertyAnimation.__init__(self, widget, prop)

    def interpolated(self, start, end, progress):
        return start

# other classes for animation

