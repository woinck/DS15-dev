#-*- coding:UTF-8 -*-
#message box

from PyQt4.QtGui import *
from PyQt4.QtCore import *

if __name__ == "__main__":
	import os, sys
	IMPORT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sys.path.append(IMPORT_PATH)
	import qrc_resource


class MessageBox(QDialog):
	Warning = 0
	Critical = 1
	Question = 2
	Ok = 0
	Cancel = 1
	Yes = 2
	No = 3
	ok_cancel_name = ["Ok", "Cancel", "Yes", "No"]
	#warningPix = ":"
	#criticalPix = ":"
	#questionPix = ":"
	def __init__(self, type, title, content, buttons1, buttons2, parent = None):
		super(MessageBox, self).__init__(parent)

		self.resize(320, 150)
		self.setFixedSize(self.size())
		self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
		width = self.width()
		height = self.height()

		self.setStyleSheet("QDialog{border-radius:4;}")
		self.titleLabel = QLabel(self)
		self.titleLabel.setText(QString.fromUtf8("  " + title))
		font = self.titleLabel.font()
		font.setBold(True)
		self.titleLabel.setFont(font)
		self.titleLabel.setGeometry(0, 0, width - 26, 25)
		self.titleLabel.setStyleSheet("border-radius:4;background:rgba(0, 197, 205, 220);")

		msg_label = QLabel(self)
 	 	msg_label.setGeometry(20, 50, 36, 36)
 		msg_label.setScaledContents(True)
 		"""if type == MessageBox.Warning:
 			msg_label.setPixmap(QPixmap(MessageBox.warningPix))
 		elif type == MessageBox.Critical:
 			msg_label.setPixmap(QPixmap(MessageBox:criticalPix))
 		else:
 			msg_label.setPixmap(QPixmap(MessageBox:questionPix))
"""
  		ask_label = QLabel(self)
  		ask_label.setGeometry(65, 60, width-100, 25*2)
  		ask_label.setWordWrap(True)
  		ask_label.setAlignment(Qt.AlignTop)
  		ask_label.setText(QString.fromUtf8(content))

  		close_button = QPushButton(self)
  		close_button.setStyleSheet("QPushButton{border-image: url(:exit0.png);}"
  									"QPushButton:hover{border-image: url(:exit1.png);}")
		
  		close_button.setFlat(True)
  		close_button.setGeometry(width - 25, 0, 25, 25)

  		ok_button = QPushButton(self)
  		ok_button.resize(70, 25)
  		ok_button.setText(MessageBox.ok_cancel_name[buttons1])
  		cancel_button = QPushButton(self)
  		cancel_button.resize(70, 25)
  		cancel_button.setText(MessageBox.ok_cancel_name[buttons2])
  		cancel_button.move(width - cancel_button.width() - 10, height - 30)
  		ok_button.move(width - ok_button.width() - cancel_button.width() - 20, height - 30)

  		self.connect(ok_button, SIGNAL("clicked()"), self, SLOT("accept()"))
  		self.connect(cancel_button, SIGNAL("clicked()"), self, SLOT("reject()"))
  		self.connect(close_button, SIGNAL("clicked()"), self, SLOT("reject()"))

  	def paintEvent(self, event):
  		painter = QPainter(self)
  		painter.setBrush(QBrush(QColor(190, 190, 190)))
  		painter.setPen(QPen(Qt.NoPen))
  		painter.drawRect(QRect(0, self.height() - 35, self.width(), 35))
  	#	painter.fillRect(QRect())

def messageBox(*arg):
	dlg = MessageBox(*arg)
	return dlg.exec_()


#for test
if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	print messageBox(MessageBox.Warning, "shabi", "你是个傻逼吗", MessageBox.Ok, MessageBox.Cancel)
	app.exec_()