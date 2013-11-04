#-*- coding: UTF-8 -*-
#simple loading label

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os,sys
if __name__ == "__main__":
	IMPORT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	sys.path.append(IMPORT_PATH)
	print "hello"
	import qrc_resource
	print "hi"

class LoadingDialog(QDialog):
	def __init__(self, text, parent = None):
		super(LoadingDialog, self).__init__(parent)
  		self.setFixedSize(200, 80)
   		self.setWindowOpacity(0.8)
   		self.setStyleSheet("background-color: #523552")
   		self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
		self.label = QLabel(self)
		self.label.setStyleSheet("background-color: transparent")
		self.tip_label = QLabel(self)
		self.tip_label.setStyleSheet("color: white; background-color: transparent")
		self.label.setGeometry(20, 10, 60, 60)
		self.tip_label.setGeometry(100, 30, 80, 20)
		self.tip_label.setScaledContents(True)
		self.movie = QMovie(":loading.gif")
		self.label.setMovie(self.movie)
		self.timer = QTimer()
		self.timer.setInterval(1000)
		self.index = 0
		self.info = text
		self.tip_label.setText(QString.fromUtf8(text))
		self.connect(self.timer, SIGNAL("timeout()"), self.changeText)

	def startLoading(self):
		self.timer.start()
		self.movie.start()
		self.exec_()
	@pyqtSlot()
	def endLoading(self):
		self.index = 0
		self.timer.stop()
		self.movie.stop()
		self.accept()

	def changeText(self):
		self.index += 1
		endfix = ""
		endfix = (self.index % 4) * "."
		self.tip_label.setText(QString.fromUtf8(self.info + endfix))

#test
if __name__ == "__main__":
	app = QApplication(sys.argv)
	dlg = LoadingDialog("连接到房间")
	dlg.startLoading()
	QTimer.singleShot(5000, dlg, SLOT("endLoading()"))
	app.exec_()
