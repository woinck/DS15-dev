# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from lib.editor.Ui_mapeditor import *
from basic import *
import sio
from lib.editor.Ui_Map import *
#import qrc_resource
#reload(sys)
#sys.setdefaultencoding("utf-8")

class Mapeditor(QtGui.QMainWindow):
	def __init__(self, parent = None):
		super(Mapeditor, self).__init__(parent)
		self.ui = Ui_Mapeditor()
		self.ui.setupUi(self)
		self.ui.comboBox.addItem(QString.fromUtf8("无对称性"))
		self.ui.comboBox.addItem(QString.fromUtf8("左右对称"))
		self.ui.comboBox.addItem(QString.fromUtf8("上下对称"))
		self.ui.comboBox.addItem(QString.fromUtf8("中心对称"))
		self.ui.comboBox_2.addItems(["%d" %x for x in range(5, 25)])
		self.ui.comboBox_3.addItems(["%d" %x for x in range(5, 25)])
		self.ui.comboBox_2.setCurrentIndex(15)
		self.ui.comboBox_3.setCurrentIndex(15)
		self.ui.comboBox_4.addItems(["%d" %x for x in (0, 1)])
		self.side = 0
		self.mode = 0
		self.filename = None
		self.X = 20
		self.Y = 20
		self.scene = QtGui.QGraphicsScene()
		self.view = Ui_MapEditor(self.scene, self)
		self.ui.viewLayout.addWidget(self.view)
		self.ui.tab_1.setStyleSheet("QTabWidget::pane{border:0;}"
									"QWidget{background-color: rgba(255, 255, 255, 20%)}")
		self.setStyleSheet("QPushButton{border:0;}")
		self.ui.newButton.setStyleSheet("*{border-image: url(:newMap00.png);}"
									"*:hover{border-image: url(:newMap01.png);}")
		self.ui.saveButton.setStyleSheet("*{border-image: url(:saveMap0.png);}"
									"*:hover{border-image: url(:saveMap1.png);}")
		self.ui.saveasButton.setStyleSheet("*{border-image: url(:saveAs0.png);}"
									"*:hover{border-image: url(:saveAs1.png);}")
		self.ui.openButton.setStyleSheet("*{border-image: url(:openMap00.png);}"
									"*:hover{border-image: url(:openMap01.png);}")
		self.ui.exitButton.setStyleSheet("*{border-image: url(:returnPre0.png);}"
									"*:hover{border-image: url(:returnPre1.png);}")
		
		self.map = []
		self.unit = [[],[]]
		QtCore.QObject.connect(self.ui.newButton,\
							   QtCore.SIGNAL('clicked()'), self.NewFile)
		QtCore.QObject.connect(self.ui.openButton,\
							   QtCore.SIGNAL('clicked()'), self.Open)
		QtCore.QObject.connect(self.ui.saveButton,\
							   QtCore.SIGNAL('clicked()'), self.Save)
		QtCore.QObject.connect(self.ui.saveasButton,\
							   QtCore.SIGNAL('clicked()'), self.SaveAs)
		#QtCore.QObject.connect(self.ui.exitButton,\
		#					   QtCore.SIGNAL('clicked()'), self.Close)
		QtCore.QObject.connect(self.ui.cancelButton_2,\
							   QtCore.SIGNAL('clicked()'), self.delunit)
		QtCore.QObject.connect(self.ui.moveButton,\
							   QtCore.SIGNAL('clicked()'), self.view.EditUnitMode)
		
		QtCore.QObject.connect(self.ui.comboBox,\
							   QtCore.SIGNAL('currentIndexChanged(int)'), self.view.SetSymmetry)
		QtCore.QObject.connect(self.ui.comboBox_2,\
							   QtCore.SIGNAL('currentIndexChanged(int)'), self.changeX)
		QtCore.QObject.connect(self.ui.comboBox_3,\
							   QtCore.SIGNAL('currentIndexChanged(int)'), self.changeY)
		QtCore.QObject.connect(self.ui.comboBox_4,\
							   QtCore.SIGNAL('currentIndexChanged(int)'), self.changeside)

		QtCore.QObject.connect(self.ui.Button1_0,\
							   QtCore.SIGNAL('clicked()'), self.button1_0)
		QtCore.QObject.connect(self.ui.Button1_1,\
							   QtCore.SIGNAL('clicked()'), self.button1_1)
		QtCore.QObject.connect(self.ui.Button1_2,\
							   QtCore.SIGNAL('clicked()'), self.button1_2)
		QtCore.QObject.connect(self.ui.Button1_3,\
							   QtCore.SIGNAL('clicked()'), self.button1_3)
		QtCore.QObject.connect(self.ui.Button1_4,\
							   QtCore.SIGNAL('clicked()'), self.button1_4)
		QtCore.QObject.connect(self.ui.Button1_5,\
							   QtCore.SIGNAL('clicked()'), self.button1_5)
		QtCore.QObject.connect(self.ui.Button1_6,\
							   QtCore.SIGNAL('clicked()'), self.button1_6)

		QtCore.QObject.connect(self.ui.Button2_0,\
							   QtCore.SIGNAL('clicked()'), self.button2_0)
		QtCore.QObject.connect(self.ui.Button2_1,\
							   QtCore.SIGNAL('clicked()'), self.button2_1)
		QtCore.QObject.connect(self.ui.Button2_2,\
							   QtCore.SIGNAL('clicked()'), self.button2_2)
		QtCore.QObject.connect(self.ui.Button2_3,\
							   QtCore.SIGNAL('clicked()'), self.button2_3)
		QtCore.QObject.connect(self.ui.Button2_4,\
							   QtCore.SIGNAL('clicked()'), self.button2_4)
		QtCore.QObject.connect(self.ui.Button2_5,\
							   QtCore.SIGNAL('clicked()'), self.button2_5)
		QtCore.QObject.connect(self.ui.Button2_6,\
							   QtCore.SIGNAL('clicked()'), self.button2_6)

		QtCore.QObject.connect(self.ui.tab_1,\
							   QtCore.SIGNAL('currentChanged(int)'), self.changemode)

	def paintEvent(self, event):
		paint = QPainter(self)
		paint.drawPixmap(0,0,1024,768,QPixmap(":mapback.png"))
		paint.drawPixmap(25,10,130,150,QPixmap(":LOGO.png"))
		if self.mode == 0:
			paint.drawPixmap(self.ui.Button1_0.x() + self.ui.tab_1.x() +140, self.ui.Button1_0.y()
							 + self.ui.tab_1.y() + 20, 30, 30, QPixmap(":plain.png"))
			paint.drawPixmap(self.ui.Button1_1.x() + self.ui.tab_1.x() +140, self.ui.Button1_1.y()
							 + self.ui.tab_1.y() + 20, 30, 30, QPixmap(":mountain.png"))
			paint.drawPixmap(self.ui.Button1_2.x() + self.ui.tab_1.x() +140, self.ui.Button1_2.y()
							 + self.ui.tab_1.y() + 20, 30, 30, QPixmap(":forest.png"))
			paint.drawPixmap(self.ui.Button1_3.x() + self.ui.tab_1.x() +140, self.ui.Button1_3.y()
							 + self.ui.tab_1.y() + 20, 30, 30, QPixmap(":barrier.png"))
			paint.drawPixmap(self.ui.Button1_4.x() + self.ui.tab_1.x() +140, self.ui.Button1_4.y()
							 + self.ui.tab_1.y() + 20, 30, 30, QPixmap(":turret.png"))
			paint.drawPixmap(self.ui.Button1_5.x() + self.ui.tab_1.x() +140, self.ui.Button1_5.y()
							 + self.ui.tab_1.y() + 20, 30, 30, QPixmap(":temple.png"))
			paint.drawPixmap(self.ui.Button1_6.x() + self.ui.tab_1.x() +140, self.ui.Button1_6.y()
							 + self.ui.tab_1.y() + 20, 30, 30, QPixmap(":mirror.png"))
		else:
			paint.drawPixmap(self.ui.Button2_0.x() + self.ui.tab_1.x() +140, self.ui.Button2_0.y()
							 + self.ui.tab_1.y() + 20, 30, 30, QPixmap(":saber0.png"))
			paint.drawPixmap(self.ui.Button2_1.x() + self.ui.tab_1.x() +140, self.ui.Button2_1.y()
							 + self.ui.tab_1.y() + 20, 30, 30, QPixmap(":lancer0.png"))
			paint.drawPixmap(self.ui.Button2_2.x() + self.ui.tab_1.x() +140, self.ui.Button2_2.y()
							 + self.ui.tab_1.y() + 20, 30, 30, QPixmap(":archer0.png"))
			paint.drawPixmap(self.ui.Button2_3.x() + self.ui.tab_1.x() +140, self.ui.Button2_3.y()
							 + self.ui.tab_1.y() + 20, 30, 30, QPixmap(":dragon_rider0.png"))
			paint.drawPixmap(self.ui.Button2_4.x() + self.ui.tab_1.x() +140, self.ui.Button2_4.y()
							 + self.ui.tab_1.y() + 20, 30, 30, QPixmap(":warrior0.png"))
			paint.drawPixmap(self.ui.Button2_5.x() + self.ui.tab_1.x() +140, self.ui.Button2_5.y()
							 + self.ui.tab_1.y() + 20, 30, 30, QPixmap(":wizard0.png"))
			paint.drawPixmap(self.ui.Button2_6.x() + self.ui.tab_1.x() +140, self.ui.Button2_6.y()
							 + self.ui.tab_1.y() + 20, 30, 30, QPixmap(":hero_10.png"))

	def redefault(self):
		self.ui.tab_1.setCurrentIndex(0)
		self.ui.comboBox.setCurrentIndex(0)
		self.view.SetClean()
		self.ui.moveButton.click()
		self.ui.Button1_0.click()
		
	def delunit(self):
		self.view.DeleteUnitMode()

	def Close(self):
		if self.isSaved():
			self.close()
		else:
			choose = QMessageBox.question(self, "Save", "Do you want to save the changes?",
										  QMessageBox.Save|QMessageBox.Discard|
										  QMessageBox.Cancel)
			if choose == QMessageBox.Save:
				self.Save()
				self.close()
			elif choose == QMessageBox.Discard:
				self.close()
			else:
				pass
	   
	def changeX(self, x):
		self.X = x + 5

	def changeY(self, y):
		self.Y = y + 5

	def changeside(self, side):
		self.side = side
		self.view.ChangeSoldierSide(side)

	def changemode(self, mode):
		self.mode = mode
		if(mode == 0):
			self.view.EditMapMode()
		if(mode == 1):
			self.view.EditUnitMode()
		self.update()
			
	def button1_0(self):
		self.view.ChangeTerrain(0)

	def button1_1(self):
		self.view.ChangeTerrain(1)

	def button1_2(self):
		self.view.ChangeTerrain(2)

	def button1_3(self):
		self.view.ChangeTerrain(3)

	def button1_4(self):
		self.view.ChangeTerrain(4)

	def button1_5(self):
		self.view.ChangeTerrain(5)

	def button1_6(self):
		self.view.ChangeTerrain(6)

	def button2_0(self):
		self.view.ChangeSoldierType(0)

	def button2_1(self):
		self.view.ChangeSoldierType(1)

	def button2_2(self):
		self.view.ChangeSoldierType(2)

	def button2_3(self):
		self.view.ChangeSoldierType(3)

	def button2_4(self):
		self.view.ChangeSoldierType(4)

	def button2_5(self):
		self.view.ChangeSoldierType(5)

	def button2_6(self):
		self.view.ChangeSoldierType(6)
		
	def SetMap(self):
		self.map, self.unit = self.view.GetMapData()
		sio._WriteFile((self.map, self.unit), "%s"%self.filename)

	def OpenFile(self):
		self.map, self.unit = sio._ReadFile("%s"%self.filename)
	
	def couldSave(self):
		return True

	def isSaved(self):
		return self.view.IsClean()

	def Save(self):
		if self.couldSave():
			if not self.isSaved():
				if self.filename == "Untitled.map":
					self.filename = QFileDialog.getSaveFileName(self, "Save",
															"/.", "*.map")
				if self.filename != QString(""):
					self.SetMap()
					self.view.SetClean()
				else:
					pass#raise error
		else:
			box = QMessageBox(QMessageBox.Warning, "Error", "The document can't be saved!")
			box.exec_()

	def Open(self):	   
		if self.isSaved():
			self.filename = QFileDialog.getOpenFileName(self, "Open File",
														"/.", "*.map")
			if self.filename != QString(""):
				self.OpenFile()
				self.view.LoadMap(self.map, self.unit)
				self.X = len(self.map)
				self.ui.comboBox_2.setCurrentIndex(self.X - 5)
				self.Y = len(self.map[0])
				self.ui.comboBox_3.setCurrentIndex(self.Y - 5)
				self.redefault()
			else:
				pass#raise error
		else:
			choose = QMessageBox.question(self, "Save", "Do you want to save the changes?",
										  QMessageBox.Save|QMessageBox.Discard|
										  QMessageBox.Cancel)
			if choose == QMessageBox.Save:
				self.Save()
				self.filename = QFileDialog.getOpenFileName(self, "Open File",
														"/.", "*.map")
				if self.filename != QString(""):
					self.OpenFile()
					self.view.LoadMap(self.map, self.unit)
					self.X = len(self.map)
					self.ui.comboBox_2.setCurrentIndex(self.X - 5)
					self.Y = len(self.map[0])
					self.ui.comboBox_3.setCurrentIndex(self.Y - 5)
					self.redefault()
				else:
					pass#raise error
			elif choose == QMessageBox.Discard:
				self.filename = QFileDialog.getOpenFileName(self, "Open File",
														"/.", "*.map")
				if self.filename != QString(""):
					self.OpenFile()
					self.view.LoadMap(self.map, self.unit)
					self.X = len(self.map)
					self.ui.comboBox_2.setCurrentIndex(self.X - 5)
					self.Y = len(self.map[0])
					self.ui.comboBox_3.setCurrentIndex(self.Y - 5)
					self.redefault()
				else:
					pass#raise error
			else:
				pass

	def NewFile(self):
		if self.isSaved():
			self.filename = "Untitled.map"
			self.setWindowTitle(self.filename)
			self.view.NewMap(self.X, self.Y)
			self.redefault()
		else:
			choose = QMessageBox.question(self, "Save", "Do you want to save the changes?",
										  QMessageBox.Save|QMessageBox.Discard|
										  QMessageBox.Cancel)
			if choose == QMessageBox.Save:
				self.Save()
				self.filename = "Untitled.map"
				self.setWindowTitle(self.filename)
				self.view.NewMap(self.X, self.Y)
				self.redefault()
			elif choose == QMessageBox.Discard:
				self.filename = "Untitled.map"
				self.setWindowTitle(self.filename)
				self.view.NewMap(self.X, self.Y)
				self.redefault()
			else:
				pass

	def SaveAs(self):
		if self.couldSave():
			self.filename = QFileDialog.getSaveFileName(self, "Save",
														"/.", "*.map")
			if self.filename != QString(""):
				self.SetMap()
				self.view.SetClean()
			else:
				pass#raise error
		else:
			box = QMessageBox(QMessageBox.Warning, "Error", "The document can't be saved!")
			box.exec_()

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	mapapp = Mapeditor()
	mapapp.show()   
	sys.exit(app.exec_())
