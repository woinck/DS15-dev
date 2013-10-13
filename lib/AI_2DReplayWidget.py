#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# composite Ui_2DreplayWidget and provide a slider controling the playing


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from functools import partial
from Humanai_Replay_event import *
import time

class CtrlSlider(QWidget):
    XMARGIN = 12.0
    YMARGIN = 5.0
    WSTRING = "999"
    def __init__(self, parent = None):
        super(CtrlSlider, self).__init__(parent)

        self.pausePoint = []
        self.nowRound = 0
        self.totalRound = 0
        self.nowStatus = 1
        self.totalStatus = 1
        self.setFocusPolicy(Qt.NoFocus)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,
                                       QSizePolicy.Fixed))

    def sizeHint(self):
        return self.minimumSizeHint()


    def minimumSizeHint(self):
        font = QFont(self.font())
        font.setPointSize(font.pointSize() - 1)
        fm = QFontMetricsF(font)
        return QSize(fm.width(CtrlSlider.WSTRING) * \
                     self.totalRound,
                     (fm.height() * 4) + CtrlSlider.YMARGIN)

    def changeNowRound(self, round_, status):
        if round_ * 2 + status <= self.totalRound * 2 + self.totalStatus:
            if self.nowRound != round_ or self.nowStatus != status:
                self.nowRound = round_
                self.nowStatus = status
                self.repaint()
                self.emit(SIGNAL("nowChanged(int, int)"), self.nowRound, self.nowStatus)


    def addPausePoint(self, round_):
        if not round_ in self.pausePoint:
            self.pausePoint.append(round_)
            self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moveSlider(event.x())
            event.accept()
        else:
            QWidget.mousePressEvent(self, event)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        pauseAction = menu.addAction("add pause point")
        span = self.width() - (CtrlSlider.XMARGIN * 2)
        offset =  event.pos().x() - CtrlSlider.XMARGIN
        round_ = int(round(float(offset) / span * self.totalRound))
        self.connect(pauseAction, SIGNAL("triggered()"), partial(self.addPausePoint, round_))
        menu.exec_(event.globalPos())

    def mouseMoveEvent(self, event):
        self.moveSlider(event.x())

    def moveSlider(self, x):
        span = self.width() - (CtrlSlider.XMARGIN * 2)
        offset = x - CtrlSlider.XMARGIN
        round_ = int(round(float(offset) / span * (2 * (self.totalRound-1)+ self.totalStatus)))
        round_ = max(0, min(round_, (self.totalRound-1)*2+self.totalStatus))
        nowround = int(1 + round_ / 2)
        nowstatus = round_ % 2                       #0回合开始,1回合结束
        self.changeNowRound(nowround, nowstatus)

      
    def changeTotalRound(self):
        if not self.totalStatus:
            self.totalStatus = 1
        else:
            self.totalRound += 1
            self.totalStatus = 0
        self.emit(SIGNAL("totalChanged()"))
        self.update()

    def reset(self):
        self.totalRound = self.nowRound = 0
        self.totalStatus = self.nowStatus = 1
        self.update()

    def paintEvent(self, event=None):
        font = QFont(self.font())
        font.setPointSize(font.pointSize() - 1)
        fm = QFontMetricsF(font)
        fracWidth = fm.width(CtrlSlider.WSTRING)
        span = self.width() - (CtrlSlider.XMARGIN * 2)
        if self.totalRound == 0 or (self.totalRound == 1 and
                                    self.totalStatus == 0):
            value = 0
        else:
            value = ((self.nowRound-1) * 2 + self.nowStatus) / float((self.totalRound-1) * 2 + self.totalStatus)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setPen(self.palette().color(QPalette.Mid))
        painter.setBrush(self.palette().brush(QPalette.AlternateBase))
        painter.drawRect(self.rect())
        segColor = QColor(Qt.green).dark(120)
        segLineColor = segColor.dark()                                #回合开始线
        segEndColor = QColor(Qt.red).dark(120)                        #回合结束线
        painter.setPen(segLineColor)
        painter.setBrush(segColor)
        painter.drawRect(CtrlSlider.XMARGIN,
                         CtrlSlider.YMARGIN, span, fm.height())
        textColor = self.palette().color(QPalette.Text)
        if self.totalRound == 1 and self.totalStatus == 0:
            segWidth = span
        else:
            segWidth = span / ((self.totalRound-1) * 2 + self.totalStatus)
        segHeight = fm.height() * 2
        nRect = fm.boundingRect(CtrlSlider.WSTRING)
        x = CtrlSlider.XMARGIN
        yOffset = segHeight + fm.height()
        painter.setBrush(QColor(Qt.red))
        for i in range(1, self.totalRound + 1):
            painter.setPen(segLineColor)
            painter.drawLine(x, CtrlSlider.YMARGIN, x, segHeight)
            painter.setPen(textColor)
            y = segHeight
            rect = QRectF(nRect)
            rect.moveCenter(QPointF(x, y + fm.height() / 2.0))
            painter.drawText(rect, Qt.AlignCenter, QString.number(i))
            if i in self.pausePoint:
                rect.setHeight(rect.height() / 2)
                rect.setWidth(rect.width() / 2)
                rect.moveCenter(QPointF(x, CtrlSlider.YMARGIN))
                painter.drawEllipse(rect)
            x += segWidth
            if i == self.totalRound and self.totalStatus == 0:
                break
            else:
                painter.setPen(segEndColor)
                painter.drawLine(x, CtrlSlider.YMARGIN, x, segHeight)
                painter.setPen(textColor)
                rect.setHeight(rect.height() * 2)
                rect.setWidth(rect.width() * 2)
                rect.moveCenter(QPointF(x, y + fm.height() / 2.0))
                painter.drawText(rect, Qt.AlignCenter, QString.number(i))
                x += segWidth
        
        span = int(span)
        y = CtrlSlider.YMARGIN - 0.5
        triangle = [QPointF(value * span, y),
                    QPointF((value * span) + \
                            (2 * CtrlSlider.XMARGIN), y),
                    QPointF((value * span) + \
                            CtrlSlider.XMARGIN, fm.height())]
        painter.setPen(Qt.yellow)
        painter.setBrush(Qt.darkYellow)
        painter.drawPolygon(QPolygonF(triangle))


class AiReplayWidget(QWidget):
    def __init__(self, scene, parent = None):
        QWidget.__init__(self, parent)

        self.playMode = 1#默认连续播放模式0, 逐回合暂停模式为1
        self.isPaused = False
        self.started = False
        self.replayWidget = HumanReplay(scene, parent)
        self.ctrlSlider = CtrlSlider()
        self.totalLabel = QLabel("total round:")
        self.nowLabel = QLabel("now round:")
        self.totalInfo = QLCDNumber()
        self.totalInfo.display(0)
        self.totalInfo.setSegmentStyle(QLCDNumber.Flat)
        self.totalStatusInfo = QLabel("At begin")
        self.nowInfo = QLineEdit("")
        self.nowInfo.setText("0")
        self.pauseButton = QPushButton("Pause")
        self.pauseLabel = QLabel("")
        self.totalStatusInfo.setSizePolicy(QSizePolicy(QSizePolicy.Fixed|QSizePolicy.Fixed))
        self.pauseLabel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed|QSizePolicy.Fixed))

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.totalLabel)
        hlayout.addWidget(self.totalInfo)
        hlayout.addWidget(self.totalStatusInfo)
        hlayout.addWidget(self.nowLabel)
        hlayout.addWidget(self.nowInfo)
        hlayout.addWidget(self.pauseButton)
        hlayout.addStretch()
        hlayout.addWidget(self.pauseLabel)

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.replayWidget)
        vlayout.addWidget(self.ctrlSlider)
        vlayout.addLayout(hlayout)

        self.setLayout(vlayout)

        self.connect(self.ctrlSlider, SIGNAL("nowChanged(int,int)"),
                     self.setNowRound,Qt.QueuedConnection)
        self.connect(self.ctrlSlider, SIGNAL("totalChanged()"),
                     self.updateUI)
        self.connect(self.nowInfo, SIGNAL("textEdited(QString)"), self.check)
        self.connect(self.pauseButton, SIGNAL("clicked()"), self.pauseGame)
        self.replayWidget.moveAnimEnd.connect(self.__test)#partial(self.ctrlSlider.changeNowRound,
                                                      #self.ctrlSlider.nowRound+1,
                                                      #not self.ctrlSlider.nowStatus))
        self.updateUI()
    def __test(self):
        self.ctrlSlider.changeNowRound(self.ctrlSlider.nowRound, 1)

    #validate nowInfo的输入
    def check(self):
        now = unicode(self.nowInfo.text())
        if len(now) == 0:
            self.nowInfo.setText(QString.number(self.ctrlSlider.nowRound))
            self.nowInfo.selectAll()
            self.nowInfo.setFocus()
        elif now.isdigit() and 0 < int(now) <= self.ctrlSlider.totalRound:
            self.ctrlSlider.changeNowRound(int(now),0)                #修改nowlineedit默认跳转到该回合开始阶段
        else:
            self.nowInfo.setText(QString.number(self.ctrlSlider.nowRound))
            self.nowInfo.selectAll()
            self.nowInfo.setFocus()

    def updateUI(self):
        self.totalInfo.display(self.ctrlSlider.totalRound)
        self.nowInfo.setText(QString.number(self.ctrlSlider.nowRound))
        totalstatus = "At begin" if self.ctrlSlider.totalStatus == 0 else "At end"
        self.totalStatusInfo.setText(totalstatus)
#        self.NowEqualTotal = (self.ctrlSlider.nowRound == self.ctrlSlider.totalRound
#                              and self.ctrlSlider.nowStatus == self.ctrlSlider.totalStatus)
        if self.isPaused:
            pausetext = "Paused"
        else:
            pausetext = "Runing"
        self.pauseLabel.setText(pausetext)
        self.pauseButton.setEnabled(self.started)
    def okToPlay(self):
        if self.ctrlSlider.nowRound == self.ctrlSlider.totalRound and self.ctrlSlider.totalStatus == 0:
            return False
        return True

    #如果在动画放映过程中通过进度条切换有没有问题?
    def setNowRound(self, a, b):
        #为了动画部分不出错
        if a * 2 + b <= self.ctrlSlider.totalRound * 2 + self.ctrlSlider.totalStatus:
            self.replayWidget.GoToRound(a-1,b)
            self.updateUI()
            #给主界面同步信息
            self.emit(SIGNAL("goToRound(int, int)"), a, b)
            if not self.isPaused:
                 if self.okToPlay():
                    if b == 0:
                        self.replayWidget.Play()
                    #自动跳到下一回合begin开始播放
                    elif self.ctrlSlider.totalRound > self.ctrlSlider.nowRound:
                        self.ctrlSlider.changeNowRound(a + 1, 0)
                    else:
                        self.isPaused = True
                        self.updateUI()
                #自动暂停播放
                 else:
                    self.isPaused = True
                    self.updateUI()


    def pauseGame(self):
        if not self.isPaused:
            self.replayWidget.GoToRound(self.ctrlSlider.nowRound-1, self.ctrlSlider.nowStatus)
            self.isPaused = True
        else:
            if not self.okToPlay():
                self.isPaused = True
                QMessageBox.warning(self, QString.fromUtf8("播放警告"),
                                    QString.fromUtf8("游戏数据更新不足，不能继续播放，请等待游戏数据更新后再继续播放。保持暂停状态"),
                                    QMessageBox.Ok,QMessageBox.NoButton)
            else:
                #判断是否可以播放
                if self.ctrlSlider.nowStatus == 1:
                    #判断是否要往下跳一回合继续播放
                    if self.ctrlSlider.totalRound > self.ctrlSlider.nowRound:
                        self.isPaused = False
                        self.updateUI()
                        self.ctrlSlider.changeNowRound(self.ctrlSlider.nowRound + 1, 0)
                    else:
                        self.isPaused = True
                        QMessageBox.warning(self, QString.fromUtf8("播放警告"),
                                            QString.fromUtf8("游戏数据更新不足，不能继续播放，请等待游戏数据更新后再继续播放。保持暂停状态"),
                                            QMessageBox.Ok,QMessageBox.NoButton)
                else:
                    self.isPaused = False
                    self.replayWidget.Play()
        self.updateUI()

    #下面三个方法在从平台获得信息时,从外部调用，
    #包装了回放界面的UpdateBeginInfo，UpdateEndInfo这些函数
    def updateIni(self, ini_info, beginfo):
        self.replayWidget.Initialize(ini_info, beginfo)
        self.ctrlSlider.changeTotalRound()
        #将now的信息设置好
        self.ctrlSlider.nowRound = 1
        self.ctrlSlider.nowStatus = 0
        self.updateUI()


    def updateBeg(self, beginfo):
        self.replayWidget.UpdateBeginData(beginfo)
        self.ctrlSlider.changeTotalRound()
        self.updateUI()

    def updateEnd(self, cmd, endinfo):
        self.replayWidget.UpdateEndData(cmd, endinfo)
        self.ctrlSlider.changeTotalRound()
        self.updateUI()
        #接收完第一回合数据后开始播放
        if self.ctrlSlider.nowStatus == 0 and self.ctrlSlider.nowRound == 1 and not self.isPaused:
            self.replayWidget.Play()


    #游戏结束时，清空所有游戏相关数据，重置进度条等。
    def reset(self):
        self.started = False
        #清空data
        self.replayWidget.reset()
        #重置进度条
        self.ctrlSlider.reset()
        self.updateUI()

#just for test
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    scene = QGraphicsScene()
    form = AiReplayWidget(scene)
    form.show()
    app.exec_()
