#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#我的人机对战回放界面单位定义
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import basic
import qrc_resource
UNIT_WIDTH = 40
UNIT_HEIGHT = 40
EDGE_WIDTH = 3
EXTRA_WIDTH = 3
MAX_OPACITY = 0.8

FILE_UNIT = ["saber", "lancer", "archer", "dragon_rider", "warrior",
             "wizard", "hero_1", "hero_2", "hero_3"]
FILE_MAP = ["plain", "mountain", "forest", "barrier", "turret",
                     "trap", "temple", "gear","mirror"]


def GetPos(x, y, flag = True):
    if flag:
        return QPointF(x * (UNIT_WIDTH + EDGE_WIDTH), y * (UNIT_HEIGHT + EDGE_WIDTH))
    else:
        return QPoint(x * (UNIT_WIDTH + EDGE_WIDTH), y * (UNIT_HEIGHT + EDGE_WIDTH))

class AbstractUnit(QGraphicsObject):
    """界面上元素的基类"""

    def __init__(self, x, y, parent):
        super(AbstractUnit, self).__init__(parent)
        self.setOpacity(MAX_OPACITY)
        self.corX = x
        self.corY = y
    def boundingRect(self):
        return QRectF(0, 0, UNIT_WIDTH+EDGE_WIDTH,
                       UNIT_HEIGHT+EDGE_WIDTH)
    def setPos(self, *pos):
        if len(pos) == 1:
            pos = pos[0]
        self.corX = pos[0]
        self.corY = pos[1]
        QGraphicsObject.setPos(self,GetPos(pos[0], pos[1]))
    def getPos(self):
        return (self.corX, self.corY)

    def getParent(self):
        return self.scene().views()[0]

#    pos = pyqtProperty(tuple, fget = getPos,
#                       fset = setPos_)
class MapUnit(AbstractUnit):
    """地形元素类"""
    def __init__(self, x, y, map_, parent = None):
        super(MapUnit, self).__init__(x, y, parent)

        self.obj = map_
#QGraphicsItem reimplement paint() rather than paintEvent
    def paint(self, painter, option, widget = None):
#        painter = QPainter()
        painter.save()
        filename = ":" + FILE_MAP[self.obj.kind] + ".png"
        image = QImage(filename).convertToFormat(QImage.Format_ARGB32)
        painter.drawImage(QPoint(EDGE_WIDTH/2, EDGE_WIDTH/2), image.scaled(UNIT_WIDTH, UNIT_HEIGHT,
                                                      Qt.IgnoreAspectRatio))
        painter.setBrush(Qt.NoBrush)
        pen = QPen(QColor(255, 255, 255))
        pen.setWidth(EDGE_WIDTH)
        painter.setPen(pen)
        painter.drawRect(0, 0, UNIT_WIDTH + EDGE_WIDTH, UNIT_HEIGHT + EDGE_WIDTH)
        painter.restore()        

class SoldierUnit(AbstractUnit):
    """单位基类"""
    def __init__(self, unit,id_, parent = None):
        super(SoldierUnit, self).__init__(unit.position[0], unit.position[1], parent)
        self.idNum = id_
        self.obj = unit

        self.setZValue(0.5)

    def paint(self, painter, option, widget = None):
#        painter = QPainter()
        painter.save()
        filename = ":" + FILE_UNIT[self.obj.kind] + "%d.png"%(self.idNum[0])
        image = QImage(filename).convertToFormat(QImage.Format_ARGB32)
       # painter.setCompositionMode(QPainter.CompositionMode_Multiply)
        painter.drawImage(QPoint(EDGE_WIDTH/2, EDGE_WIDTH/2), image.scaled(UNIT_WIDTH, UNIT_HEIGHT,
                                                                           Qt.IgnoreAspectRatio))
        painter.restore()


class MouseIndUnit(AbstractUnit):
    """光标"""
    def __init__(self, x, y ,parent = None):
        super(MouseIndUnit, self).__init__(x, y, parent)
        self.timer = QTimer()
        self.connect(self.timer, SIGNAL("timeout()"), self.timeOut)

        self.setZValue(0.6)
    def setVis(self, vis):
        if vis:
            self.timer.start(600)
        else:
            self.timer.stop()

    def timeOut(self):
        self.setVisible(not self.isVisible())
#    def hideEvent(self):
#        self.setVisible(False)
#        self.killTimer(self.timer)
#    def showEvent(self):
#        self.setVisible(True)
#        self.timer.start()

    def paint(self, painter, option, widget = None):
        painter.save()
        RLINE = 0.4 #rate of line
        pen = QPen()
        pen.setWidth(EDGE_WIDTH)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setColor(QColor(Qt.blue).lighter())
        painter.setPen(pen)
#        painter.setCompositionMode(QPainter.CompositionMode_Multiply)
        painter.drawLine(QPointF(0, 0),
                         QPointF(0, RLINE*(UNIT_HEIGHT + EDGE_WIDTH)))
        painter.drawLine(QPointF(0, 0),
                         QPointF(RLINE*(UNIT_WIDTH + EDGE_WIDTH), 0))
        painter.drawLine(QPointF(UNIT_WIDTH + EDGE_WIDTH, 0),
                         QPointF(UNIT_WIDTH + EDGE_WIDTH, RLINE*(UNIT_HEIGHT + EDGE_WIDTH)))
        painter.drawLine(QPointF(UNIT_WIDTH + EDGE_WIDTH, 0),
                         QPointF((1-RLINE)*(UNIT_WIDTH + EDGE_WIDTH), 0))
        painter.drawLine(QPointF(0, (UNIT_HEIGHT + EDGE_WIDTH)),
                         QPointF(0, (1-RLINE)*(UNIT_HEIGHT + EDGE_WIDTH)))
        painter.drawLine(QPointF(0, (UNIT_HEIGHT + EDGE_WIDTH)),
                         QPointF(RLINE*(UNIT_WIDTH + EDGE_WIDTH), (UNIT_HEIGHT + EDGE_WIDTH)))
        painter.drawLine(QPointF(UNIT_WIDTH + EDGE_WIDTH, (UNIT_HEIGHT + EDGE_WIDTH)),
                         QPointF(UNIT_WIDTH + EDGE_WIDTH, (1-RLINE)*(UNIT_HEIGHT + EDGE_WIDTH)))
        painter.drawLine(QPointF(UNIT_WIDTH + EDGE_WIDTH, (UNIT_HEIGHT + EDGE_WIDTH)),
                         QPointF((1-RLINE)*(UNIT_WIDTH + EDGE_WIDTH), (UNIT_HEIGHT + EDGE_WIDTH)))
        painter.restore()

class MouseFocusUnit(AbstractUnit):
    def __init__(self, x, y, parent = None):
        super(MouseFocusUnit, self).__init__(x, y, parent)
        self.setZValue(0.9)

    def paint(self, painter, option, widget = None):
        painter.save()
        pen = QPen()
        pen.setWidth(EDGE_WIDTH)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setColor(QColor(Qt.blue).darker())
        painter.setPen(pen)
        painter.setCompositionMode(QPainter.CompositionMode_Multiply)
        painter.drawRect(QRect(0, 0, UNIT_WIDTH + EDGE_WIDTH, UNIT_HEIGHT + EDGE_WIDTH))
        painter.restore()

class ArrangeIndUnit(AbstractUnit):
    def __init__(self, x, y, parent = None):
        super(ArrangeIndUnit, self).__init__(x, y, parent)
        self.setZValue(1)
#        self.setOpacity(1)

    def paint(self, painter, option, widget = None):
        painter.save()
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor(0,0,100,30))
        painter.setBrush(brush)
        painter.drawRect(QRect(EDGE_WIDTH/2, EDGE_WIDTH/2, UNIT_WIDTH + EDGE_WIDTH/2, UNIT_HEIGHT + EDGE_WIDTH/2))
        painter.restore()
        
class RouteIndUnit(AbstractUnit):

    def __init__(self, x, y, parent = None):
        super(RouteIndUnit, self).__init__(x, y, parent)
        self.setZValue(0.9)

    def paint(self, painter, option, widget = None):
        painter.save()
#        pen = QPen()
#        pen.setWidth(EDGE_WIDTH)
#        pen.setCapStyle(Qt.RoundCap)
#        pen.setJoinStyle(Qt.RoundJoin)
#        pen.setColor(QColor(Qt.blue).darker())
#        painter.setPen(pen)



        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor(200, 0, 0))
        painter.setBrush(brush)
 #       painter.setCompositionMode(QPainter.CompositionMode_Multiply)#QPainter.CompositionMode_Destination)#QPainter.CompositionMode_Multiply)
        painter.drawEllipse(QPointF((UNIT_WIDTH + EDGE_WIDTH) / 2, (UNIT_HEIGHT + EDGE_WIDTH) / 2), 5, 5)
        painter.restore()

class AttackIndUnit(AbstractUnit):
    def __init__(self, x,y,file_, parent = None):
        super(AttackIndUnit, self).__init__(x,y,parent)
        self.image = QImage(file_).scaled(UNIT_WIDTH/2, UNIT_HEIGHT/2)
#        self.setOpacity(0)
    def paint(self, painter, option, widget = None):
        painter.save()
        painter.setCompositionMode(QPainter.CompositionMode_Multiply)
        painter.drawImage(QPointF(UNIT_WIDTH/4, UNIT_HEIGHT/4),self.image)
        painter.restore()

class TargetIndUnit(AbstractUnit):
    def __init__(self, x,y,parent = None):
        super(TargetIndUnit, self).__init__(x,y,parent)
        self.setZValue(1)
    def paint(self, painter, option, widget = None):
        painter.save()        
        pen = QPen()
        pen.setWidth(EDGE_WIDTH)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setColor(QColor(Qt.red))
        painter.setPen(pen)
#        painter.setCompositionMode(QPainter.CompositionMode_Multiply)
        painter.drawRect(QRect(0, 0, UNIT_WIDTH + EDGE_WIDTH, UNIT_HEIGHT + EDGE_WIDTH))
        painter.restore()
class EffectIndUnit(QGraphicsTextItem):
    def __init__(self, text, parent = None):
        super(EffectIndUnit, self).__init__(text, parent)
        self.text = text
        font = self.font()
        if text[0] == "+" or text[0] == '-':
            font.setPointSize(font.pointSize() * 2)
            font.setBold(True)
        self.setFont(font)
        self.setDefaultTextColor(QColor(Qt.red).darker())

class DieIndUnit(AbstractUnit):
    def __init__(self, x = 0, y = 0, parent = None):
        super(DieIndUnit, self).__init__(x, y, parent)

    def paint(self, painter, option, widget = None):
        painter.save()
#        painter.begin(self.scene().views()[0])
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor(200,0,0,70))
        painter.setBrush(brush)
        painter.drawRect(QRect(0, 0, UNIT_WIDTH + EDGE_WIDTH, UNIT_HEIGHT + EDGE_WIDTH))
#        
        painter.restore()
        
class TransIndUnit(AbstractUnit):
    #flag为1为目的地
    def __init__(self, flag, x = 0, y = 0, parent = None):
        super(TransIndUnit, self).__init__(x, y, parent)
        self.pixmap = QImage(":trans%d.png" %flag).scaled(UNIT_WIDTH, UNIT_HEIGHT)
        self.setOpacity(0.3)

    def paint(self, painter, option, widget = None):
        painter.drawImage(QPoint(EDGE_WIDTH/2, EDGE_WIDTH/2), self.pixmap)

# just for test
if __name__ == "__main__":
    import sys,qrc_resource
    app = QApplication(sys.argv)
    view = QGraphicsView()
    scene = QGraphicsScene()
    view.setScene(scene)
    items = [DieIndUnit(),TargetIndUnit(0,0),ArrangeIndUnit(0,0),AttackIndUnit(0,0,":attack_ind1.png")]#,# AttackIndUnit(0,0)]
    for i in range(len(items)):
        scene.addItem(items[i])
        items[i].setPos(i, 0)
    view.show()
    app.exec_()
    
