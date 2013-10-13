from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Style(QCommonStyle):
    def __init__(self):
        super(Style, self).__init__()
        

    def drawControl(self, ele, option, painter, widget = None):
        if ele == QStyle.CE_PushButton:
            painter.save()
            painter.setBrush(QBrush(QPixmap("image/button.png").scaled(142,32)))
            painter.setPen(QColor(0,0,0,0))
            painter.drawRect(option.rect)
            pal = QPalette()
            pal.setBrush(QPalette.WindowText, QColor(255, 255, 255))
            self.drawItemText(painter,option.rect.adjusted(1,1,-1,-1), Qt.AlignCenter,pal,
                                 True, option.text,QPalette.WindowText )
            painter.restore()
        else:
            QCommonStyle.drawControl(self,ele,option,painter, widget)
            
    def drawPrimitive(self, pe, option, painter, widget = None):
        if pe == QStyle.PE_IndicatorArrowDown:
            painter.save()
            point = []
            rect = option.rect
            if not option.state & QStyle.State_UpArrow:
                x = rect.left() + rect.width()/4
                y = rect.top() + rect.height()/4
                point.append(QPoint(x, y))
                x = rect.left() + rect.width() * 3 / 4
                point.append(QPoint(x, y))
                x = rect.left() + rect.width() / 2
                y = rect.bottom() - rect.height() / 4
                point.append(QPoint(x, y))
            else:
                x = rect.left() + rect.width() / 4
                y = rect.bottom() - rect.height()/4
                point.append(QPoint(x, y))
                x = rect.right() - rect.width() / 4
                point.append(QPoint(x, y))
                x = rect.left() + rect.width() / 2
                y = rect.top() + rect.height() / 2
                point.append(QPoint(x, y))
            painter.setPen(QColor(50, 0, 0, 60))
            painter.setBrush(QBrush(QColor(0, 50, 200)))
            painter.drawPolygon(QPolygon(point))
            painter.restore()
        else:
            QCommonStyle.drawPrimitive(self, pe, option, painter, widget)

    def drawComplexControl(self, ele, option, painter, widget = None):
        if ele == QStyle.CC_ComboBox:
            painter.setBrush(QBrush(QColor(200,200,200,0.5)))
            buttonRect = option.rect
#            buttonRect.setWidth(buttonRect.width())

            buttonOpt = QStyleOption(option)
            
            pal = QPalette(QColor(255,255,255))
            buttonOpt.palette = pal

            painter.setClipRect(buttonRect, Qt.IntersectClip)
#            if not option.activeSubControls & QStyle.SC_ComboBoxArrow:
#               buttonOpt.state &= ~(QStyle.State_MouseOver | QStyle.State_On | QStyle.State_Sunken)
            self.drawComboButton(buttonOpt, painter)

            arrowOpt = QStyleOption(buttonOpt)
            arrowOpt.rect = self.subControlRect(QStyle.CC_ComboBox, option, QStyle.SC_ComboBoxArrow).adjusted(+3, +3, -3, -3)
            if arrowOpt.rect.isValid():
                self.drawPrimitive(QStyle.PE_IndicatorArrowDown, arrowOpt, painter)

        else:
            QCommonStyle.drawComplexControl(self, ele, option, painter, widget)

    def subControlRect(self, control, option, subcontrol, widget = None):
        if control == QStyle.CC_ComboBox:
            frameWidth = self.pixelMetric(QStyle.PM_DefaultFrameWidth, option,
                                         widget)
            buttonWidth = 16
            
            if subcontrol == QStyle.SC_ComboBoxFrame:
                return option.rect
            elif subcontrol == QStyle.SC_ComboBoxEditField:
                return option.rect.adjusted(0, +frameWidth,
                                            -buttonWidth-frameWidth,0)
            elif subcontrol == QStyle.SC_ComboBoxArrow:
                #        case QStyle.SC_ComboBoxArrow:
                return self.visualRect(option.direction, option.rect,
                                       QRect(option.rect.right() - buttonWidth,
                                             option.rect.y(),
                                             buttonWidth,
                                             option.rect.height()))
            else:
                return QCommonStyle.subControlRect(self, control, option,
                                                    subcontrol, widget)
        
        else:
            return QCommonStyle.subControlRect(self, control, option,
                                               subcontrol, widget)


    def pixelMetric(self, which, option, widget = None):

        if which == QStyle.PM_ButtonDefaultIndicator:
            return 0
        elif which ==  QStyle.PM_IndicatorWidth or which ==  QStyle.PM_IndicatorHeight:
            return 16
        elif which ==  QStyle.PM_CheckBoxLabelSpacing:
            return 8
        elif which ==  QStyle.PM_DefaultFrameWidth:
            return 2
        else:

            return QCommonStyle.pixelMetric(self, which, option, widget)

    def drawComboButton(self, option, painter):


        buttonColor = option.palette.button().color()

#        penWidth = 1.0
#        if option.features & QStyleOptionButton.DefaultButton:
#            penWidth = 2.0
        painter.save()
        roundRect = option.rect.adjusted(+1, +1, -1, -1)
        if not roundRect.isValid():
            return

        diameter = 12
        cx = 100 * diameter / roundRect.width()
        cy = 100 * diameter / roundRect.height()
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(buttonColor)
        painter.drawRoundRect(roundRect, cx, cy)

#        if option.state & (QStyle.State_On | QStyle.State_Sunken):
#            slightlyOpaqueBlack = QColor(0, 0, 0, 63)
#            painter.setBrush(slightlyOpaqueBlack)
#            painter.drawRoundRect(roundRect, cx, cy)
    

#        painter.setRenderHint(QPainter.Antialiasing, True)
#        painter.setPen(QPen(option.palette.foreground(), penWidth))
#        painter.setBrush(Qt.NoBrush)
#        painter.drawRoundRect(roundRect, cx, cy)
        painter.restore()
