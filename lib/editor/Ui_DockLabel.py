#

#

from PyQt4 import QtGui, QtCore

LABEL_Z_VALUE = 3.0

class Ui_DockLabel(QtGui.QGraphicsItem):
    "the dock label used to display imformation"
    def __init__(self, size, parent = None):
        QtGui.QGraphicsItem.__init__(self, parent)
        self.size = size

    def boundingRect(self):
        return QtCore.QRectF(QtCore.QPointF(0, 0), self.size)

class _Ui_DockItem(QtGui.QGraphicsItem):
    "the dock item giving signal of hovering"
    def __init__(self, size, cornerId, window):
        QtGui.QGraphicsItem.__init__(self, window)
        self.size = size
        self.window = window
        if (cornerId==0):
            self.setPos(QtCore.QPointF(0, 0))
        elif (cornerId==1):
            self.setPos(QtCore.QPointF(window.size.width()-size.width(), 0))
        elif (cornerId==2):
            self.setPos(QtCore.QPointF(window.size.width()-size.width(),
                                       window.size.height()-size.height()))
        elif (cornerId==3):
            self.setPos(QtCore.QPointF(0, window.size.height()-size.height()))
        # set the hover region

    def boundingRect(self):
        return QtCore.QRectF(QtCore.QPointF(0, 0), self.size)
    def paint(self, painter, option, widget):
        pass

    def hoverEnterEvent(self, event):
        self.window.CornerIdInc()
        # change the pos of dock label

class Ui_DockWindow(QtGui.QGraphicsItem):
    "the dock window of scene"
    def __init__(self, label, itemSize, view, parent = None):
        QtGui.QGraphicsItem.__init__(self, parent)
        self.size = QtCore.QSizeF(view.geometry().size())
        self.label = label
        self.label.setParentItem(self)
        self.__itemCorners = [QtCore.QPointF(0, 0),
                              QtCore.QPointF(self.size.width()-label.size.width(), 0),
                              QtCore.QPointF(self.size.width()-label.size.width(),
                                             self.size.height()-label.size.height()),
                              QtCore.QPointF(0, self.size.height()-label.size.height())]
        self.__nowCorner = 0
        self.label.setPos(self.__itemCorners[self.__nowCorner])
        # set label on the item
        self.setPos(view.mapToScene(QtCore.QPoint(0, 0)))
        # set item in the window
        self.__hoverItem = []
        for i in range(4):
            self.__hoverItem.append(_Ui_DockItem(itemSize, i, self))
        self.__hoverItem[0].setAcceptHoverEvents(True)
        self.__hoverItem[1].setAcceptHoverEvents(False)
        self.__hoverItem[2].setAcceptHoverEvents(False)
        self.__hoverItem[3].setAcceptHoverEvents(False)
        # set hover region
        self.setZValue(LABEL_Z_VALUE)

    def CornerIdInc(self):
        "change the pos of dock label"
        newId = (self.__nowCorner+1)%4
        self.__hoverItem[newId].setAcceptHoverEvents(True)
        self.__hoverItem[self.__nowCorner].setAcceptHoverEvents(False)
        # block event of the old item
        self.label.setPos(self.__itemCorners[newId])
        self.__nowCorner = newId

    def boundingRect(self):
        return QtCore.QRectF(QtCore.QPointF(0, 0), self.size)
    def paint(self, painter, option, widget):
        pass
