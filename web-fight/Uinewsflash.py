#-*- coding:UTF-8 -*-
#flash widget

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from functools import partial

import os,sys
if __name__ == "__main__":
	IMPORT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sys.path.append(IMPORT_PATH)
import qrc_resource
FLASH_WIDTH = 400
FLASH_HEIGHT = 200
BUTTON_WIDTH = 15
BUTTON_MARGIN = 40
BUTTON_MARGIN_DOWN = 35
NOTE_HEIGHT = 50
NOTE_POS_X = 20
NOTE_POS_Y = 10

StateList = []
StateDict = {}
NoteList = []
def StyleSheetProc(styleString, *args):
	for arg in args:
		styleString = styleString.replace(arg[0], arg[1])
	print styleString
	return styleString

class FlashPixmap(QGraphicsObject):
	def __init__(self, pixmap, parent = None):
		super(FlashPixmap, self).__init__(parent)
		self.pixmap = QImage(pixmap)

	def boundingRect(self):
		return QRectF(0, 0, FLASH_WIDTH, FLASH_HEIGHT)
	
	def paint(self, painter, option, widget = None):
		painter.save()
		painter.drawImage(self.boundingRect(), self.pixmap)
		painter.restore()

class FlashButton(QGraphicsProxyWidget):
	def __init__(self, num, parent = None):
		super(FlashButton, self).__init__(parent)

		self.num = num
		self.button = QPushButton()
		self.button.resize(BUTTON_WIDTH, BUTTON_WIDTH)
		#self.image0 = ":flashicon0%d.png" %self.num
		#self.image1 = ":flashicon1%d.png" %self.num
		self.image0 = ":start0.png"
		self.image1 = ":start1.png"
		self.button.setStyleSheet(StyleSheetProc("QPushButton{background: transparent;}"))
		#										"QPushButton{border-image:url(@imagename0);border:0;}"
		#								"QPushButton:checked{border-image:url(@imagename1);border:0;}",["@imagename0",self.image0],
		#							["@imagename1", self.image1]))
		self.setNowChoosed(False)
		self.setWidget(self.button)

	def setNowChoosed(self, nowChoose):	
		if nowChoose:
			self.button.setIcon(QIcon(QPixmap(self.image1).scaled(BUTTON_WIDTH, BUTTON_WIDTH)))
		else:
			self.button.setIcon(QIcon(QPixmap(self.image0).scaled(BUTTON_WIDTH, BUTTON_WIDTH)))



class FlashButtonGroup(QGraphicsObject):
	buttonClicked = pyqtSignal(int)
	def __init__(self, number, parent = None):
		super(FlashButtonGroup, self).__init__(parent)
		
		self.number = number
		self.buttons = []
		for i in range(number):
			new_button = FlashButton(i, self)
			new_button.setPos(QPointF(i * 2.5 * BUTTON_WIDTH ,0))
			self.buttons.append(new_button)
			self.connect(new_button.button, SIGNAL("clicked()"), partial(self.emitS, i))

	def click(self, num):
		self.buttons[num].button.click()

	def paint(self, painter, option,widget = None):
		pass

	def boundingRect(self):
		return QRectF(0, 0, (self.number * 2.5 + 1) * BUTTON_WIDTH, BUTTON_WIDTH)

	def emitS(self, num):	
		self.buttonClicked.emit(num)

		
class NoteItem(QGraphicsTextItem):
	def __init__(self, text, parent = None):
		super(NoteItem, self).__init__(text, parent)

		self.setTextInteractionFlags(Qt.TextBrowserInteraction | Qt.LinksAccessibleByMouse)
		self.setHtml(text)
		self.setDefaultTextColor(QColor(0, 255, 255))
		self.setFlag(QGraphicsItem.ItemIsSelectable, False)
		self.connect(self, SIGNAL("linkActivated(QString)"), self.goToUrl)
		
	def goToUrl(self, url):
		QDesktopServices.openUrl(QUrl(url))

	#def paint(self, painter, option, widget = None):
	#	option.state &= ~QStyle.State_Selected
	#	QGraphicsTextItem.paint(self, painter, option, widget)

class NoteBar(QGraphicsRectItem):
	def __init__(self, parent = None):
		super(NoteBar, self).__init__(parent)
	
	def boundingRect(self):
		return QRectF(0, 0, FLASH_WIDTH, NOTE_HEIGHT)

	def paint(self, painter, option, widget = None):
		painter.save()	

		brush = QBrush(Qt.SolidPattern)
		brush.setColor(QColor(205, 205, 201, 200))
		painter.setBrush(brush)
		painter.setPen(QPen(Qt.NoPen))
		painter.drawRect(self.boundingRect())

		painter.restore()

class StateTransition(QSignalTransition):
	def __init__(self, number, sender, signal, parent = None):
		super(StateTransition, self).__init__(sender, signal, parent)
		
		self.number = number

	def eventTest(self, event):
		if not QSignalTransition.eventTest(self, event):
			return False
		targetNum = event.arguments()[0].toInt()[0]

		if targetNum == self.number:
			return False
		self.setTargetState(StateList[targetNum])
		animation = TransitionAnimation(self.number, targetNum)
		if self.animations():
			self.removeAnimation(self.animations()[0])
		self.addAnimation(animation)
		return True
	
def TransitionAnimation(former, target):
	AniDuration = 1000
	former_item = StateDict[StateList[former]]
	target_item = StateDict[StateList[target]]
	former_note = NoteList[former]
	target_note = NoteList[target]
	target_item.setPos(QPointF(FLASH_WIDTH, 0))
	
	anigroup = QParallelAnimationGroup()
	ani1 = QPropertyAnimation(former_item, "pos")
	ani1.setDuration(AniDuration)
	ani1.setStartValue(QPointF(0, 0))
	ani1.setEndValue(QPointF(-FLASH_WIDTH, 0))
	ani1.setEasingCurve(QEasingCurve.InOutQuad)
	anigroup.addAnimation(ani1)

	ani2 = QPropertyAnimation(target_item, "pos")
	ani2.setDuration(AniDuration)
	ani2.setStartValue(QPointF(FLASH_WIDTH, 0))
	ani2.setEndValue(QPointF(0, 0))
	ani2.setEasingCurve(QEasingCurve.InOutQuad)
	anigroup.addAnimation(ani2)
	
	ani3 = QPropertyAnimation(former_note, "pos")
	ani3.setDuration(AniDuration / 2)
	ani3.setStartValue(former_note.pos())
	ani3.setEndValue(target_note.pos())
	ani3.setEasingCurve(QEasingCurve.InOutQuad)
	anigroup.addAnimation(ani3)
	
	ani4 = QPropertyAnimation(target_note, "pos")
	ani4.setDuration(AniDuration / 2)
	ani4.setStartValue(target_note.pos())
	ani4.setEndValue(former_note.pos())
	ani4.setEasingCurve(QEasingCurve.InOutQuad)
	anigroup.addAnimation(ani4)
	
	return anigroup
		
class FlashWidget(QGraphicsView):
	def __init__(self, pix_list, note_list, parent = None):
		super(FlashWidget, self).__init__(parent)
		
		self.grscene = QGraphicsScene(self)
		self.setScene(self.grscene)
		self.flash_list = []
		global NoteList
		#加载图片及文字说明
		for pix in pix_list:
			if QFile.exists(pix):
				new_pix = QPixmap(pix).scaled(FLASH_WIDTH, FLASH_HEIGHT)
				new_flashpix = FlashPixmap(new_pix)
				new_flashpix.setOpacity(0)
				self.grscene.addItem(new_flashpix)
				new_flashpix.setPos(QPointF(0,0))
				self.flash_list.append(new_flashpix)
				new_note = NoteItem(QString.fromUtf8(note_list[pix_list.index(pix)]))
				new_note.setOpacity(0)
				new_note.setPos(QPointF(NOTE_POS_X, NOTE_POS_Y + FLASH_HEIGHT - NOTE_HEIGHT))
				self.grscene.addItem(new_note)
				new_note.setZValue(0.5)
				NoteList.append(new_note)

		self.grscene.setSceneRect(self.grscene.itemsBoundingRect())

		self.num = len(self.flash_list)
		#按键
		self.buttonGroup = FlashButtonGroup(self.num)
		self.buttonGroup.setZValue(0.6)
		self.grscene.addItem(self.buttonGroup)
		self.buttonGroup.setPos(QPointF(FLASH_WIDTH - BUTTON_MARGIN - BUTTON_WIDTH * self.num * 2, FLASH_HEIGHT - BUTTON_MARGIN_DOWN))
		#图片文字说明栏
		self.noteBar = NoteBar()
		self.noteBar.setZValue(0.1)
		self.grscene.addItem(self.noteBar)
		self.noteBar.setPos(QPointF(0, FLASH_HEIGHT - NOTE_HEIGHT))
		
		#状态机初始化
		self.stateMac = QStateMachine(self)
		global StateDict, StateList
		for i in range(self.num):
			new_state = QState(self.stateMac)
			new_state.assignProperty(self, "nowActive", i)
			new_trans = StateTransition(i, self.buttonGroup, SIGNAL("buttonClicked(int)"))
			new_state.addTransition(new_trans)
			StateList.append(new_state)
			StateDict[new_state] = self.flash_list[i]
		self.stateMac.setInitialState(StateList[0])

		#timer初始化
		self.timer = QTimer(self)
		self.timer.setInterval(4000)
		self.timer.setSingleShot(True)
		self.connect(self.timer, SIGNAL("timeout()"), self.on_timeout)
		#当前展示的pic
		self.nowPic = 0
		for flash in self.flash_list:
			flash.setPos(QPointF(FLASH_WIDTH, 0))
			flash.setOpacity(1)
		for note in NoteList:
			note.setPos(QPointF(NOTE_POS_X, FLASH_HEIGHT + NOTE_POS_Y))
			note.setOpacity(1)
		self.flash_list[0].setPos(QPointF(0, 0))
		NoteList[0].setPos(QPointF(NOTE_POS_X, NOTE_POS_Y + FLASH_HEIGHT - NOTE_HEIGHT))
		self.stateMac.start()

	def getActivePage(self):
		return self.nowPic

	def setActivePage(self, num):
		self.timer.stop()
		self.nowPic = num
		for i in range(self.num):
			if i != num:
				self.buttonGroup.buttons[i].setNowChoosed(False)
			else:
				self.buttonGroup.buttons[i].setNowChoosed(True)
		self.timer.start()
	
	def on_timeout(self):
		self.buttonGroup.click((self.nowPic + 1) % self.num)
		
	def showEvent(self, event):
		self.timer.start()
		QGraphicsView.showEvent(self, event)

	def closeEvent(self, event):
		self.timer.stop()
		event.accept()
	nowActive = pyqtProperty('int', fget = getActivePage, fset = setActivePage)
		
#for test
if __name__ == "__main__":
	app = QApplication(sys.argv)
	form = FlashWidget([":login_back.png", ":mainWindow.png"], ["<a href='http://www.baidu.com'>测试赛</a>", "<b>平台2.718</b>"])
	form.show()
	
	app.exec_()
		