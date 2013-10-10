#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#Fox Ning
from PyQt4.QtGui import *
from PyQt4.QtCore import *


#Three dictionaries for show types of map or unit
NumToMapType = {0:"平原",1:"山地",2:"森林",3:"屏障",4:"炮塔",
				 5:"遗迹",6:"传送门"}
NumToUnitType = {0:"剑士",1:"突击手",2:"狙击手",3:"战斗机",
				4:"肉搏者", 5:"治疗师", 6:"HERO_1", 7:"HERO_2",
				8:"HERO_3"}
NumToActionType = {0:"待机", 1:"攻击", 2:"技能"}
#QTabWidget{
#background-color: rgb(255,255,255,0);
#StyleSheet = """
#QTabWidget{
#background: transparent;
#}
#QLineEdit{
#background-color: rgb(0, 0, 200,50);
#color: white;
#}
#"""

class InfoWidget(QTabWidget):
	def __init__(self, parent =None):
		super(InfoWidget, self).__init__(parent)

		self.setStyleSheet("QTabBar::tab { background: gray; color: white; padding: 5px; }"
							"QTabWidget::tab-bar {alignment: center;}"
									"QTabBar::tab:selected { background: lightgray; } "
									"QTabWidget::pane { border: 0; } "
									"QWidget { background: transparent; } ")
									#"QTabWidget:QWidget::QLineEdit {border:0px; background: white;}")
		old_font = self.font()
		new_font = QFont()
		new_font.setBold(True)
		new_font.setPointSize(old_font.pointSize() + 1)
		self.setFont(new_font)
		self.infoWidget_Unit = InfoWidget2()
		self.infoWidget_Map = InfoWidget3()
		self.addTab(self.infoWidget_Unit, "Unit info")
		self.addTab(self.infoWidget_Map, "Map info")
		self.setTabToolTip(1, "the button-pressed unit's infos")
		self.setTabToolTip(2, "the button-pressed map-grid's infos")

	#展现单位,地形信息
	def newUnitInfo(self, base_unit):
		self.infoWidget_Unit.info_type.setText(QString.fromUtf8(NumToUnitType[base_unit.kind]))
		self.infoWidget_Unit.info_life.setText("%d" %base_unit.life)
		self.infoWidget_Unit.info_attack.setText("%d" %base_unit.strength)
		self.infoWidget_Unit.info_defence.setText("%d" %base_unit.defence)
		self.infoWidget_Unit.info_speed.setText("%d" %base_unit.agility)
		self.infoWidget_Unit.info_moverange.setText("%d" %base_unit.move_range)
		self.infoWidget_Unit.info_attackrange.setText("%s" %base_unit.attack_range)

	def newMapInfo(self, map_basic):
		self.infoWidget_Map.info_type.setText(QString.fromUtf8(NumToMapType[map_basic.kind]))
		self.infoWidget_Map.info_score.setText("%d" %map_basic.score)
		self.infoWidget_Map.info_consumption.setText("%d" %map_basic.move_consumption)

#展示单位基础信息
class InfoWidget2(QWidget):
	def __init__(self, parent = None):
		super(InfoWidget2, self).__init__(parent)
		self.infos = []


		self.label_type = QLabel(QString.fromUtf8("类型:"))
		self.info_type = QLabel("")
		self.infos.append(self.info_type)
		self.label_life = QLabel(QString.fromUtf8("生命:"))
		self.info_life= QLabel("")
		self.infos.append(self.info_life)
		self.label_attack = QLabel(QString.fromUtf8("攻击:"))
		self.info_attack = QLabel("")
		self.infos.append(self.info_attack)
		self.label_speed = QLabel(QString.fromUtf8("敏捷:"))
		self.info_speed = QLabel("")
		self.infos.append(self.info_speed)
		self.label_defence = QLabel(QString.fromUtf8("防御:"))
		self.info_defence = QLabel("")
		self.infos.append(self.info_defence)
		self.label_moverange = QLabel(QString.fromUtf8("移动力:"))
		self.info_moverange = QLabel("")
		self.infos.append(self.info_moverange)
		self.label_attackrange = QLabel(QString.fromUtf8("攻击范围:"))
		self.info_attackrange = QLabel("")
		self.infos.append(self.info_attackrange)

		labels = [self.label_type, self.label_attack, self.label_life, self.label_speed,
					self.label_defence, self.label_attackrange, self.label_moverange]

		old_font = self.font()
		new_font = QFont()
		new_font.setBold(True)
		new_font.setPointSize(old_font.pointSize() + 3)

		
		pal = self.label_type.palette()
		pal.setBrush(QPalette.WindowText, QColor(Qt.white))

		for info in self.infos:
			info.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
			info.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
			info.setFont(new_font)
			info.setPalette(pal)
		for label in labels:
			label.setFont(new_font)
			label.setPalette(pal)

		self.layout = QGridLayout()
		self.layout.addWidget(self.label_type, 0, 0)
		self.layout.addWidget(self.info_type, 0, 1)
		self.layout.addWidget(self.label_life, 1, 0)
		self.layout.addWidget(self.info_life, 1, 1)
		self.layout.addWidget(self.label_attack, 2, 0)
		self.layout.addWidget(self.info_attack, 2, 1)
		self.layout.addWidget(self.label_defence, 3, 0)
		self.layout.addWidget(self.info_defence, 3, 1)
		self.layout.addWidget(self.label_speed, 4, 0)
		self.layout.addWidget(self.info_speed, 4, 1)
		self.layout.addWidget(self.label_moverange, 5, 0)
		self.layout.addWidget(self.info_moverange, 5, 1)
		self.layout.addWidget(self.label_attackrange, 6, 0)
		self.layout.addWidget(self.info_attackrange, 6, 1)

		self.setLayout(self.layout)


#展示地图基础信息
class InfoWidget3(QWidget):
	def __init__(self, parent = None):
		super(InfoWidget3, self).__init__(parent)
		self.infos = []
		self.label_type = QLabel(QString.fromUtf8("类型:"))
		self.info_type = QLabel("")
		self.infos.append(self.info_type)
		self.label_score = QLabel(QString.fromUtf8("分值:"))
		self.info_score= QLabel("")
		self.infos.append(self.info_score)
		self.label_consumption = QLabel(QString.fromUtf8("移动消耗:"))
		self.info_consumption = QLabel("")
		self.infos.append(self.info_consumption)

		labels = [self.label_type, self.label_consumption, self.label_score]

		old_font = self.font()
		new_font = QFont()
		new_font.setBold(True)
		new_font.setPointSize(old_font.pointSize() + 3)

		pal = self.label_type.palette()
		pal.setBrush(QPalette.WindowText, QColor(Qt.white))

		for info in self.infos:
			info.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
			info.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
			info.setFont(new_font)
			info.setPalette(pal)
		for label in labels:
			label.setFont(new_font)
			label.setPalette(pal)

		self.layout = QGridLayout()
		self.layout.addWidget(self.label_type, 0, 0)
		self.layout.addWidget(self.info_type, 0, 1)
		self.layout.addWidget(self.label_score, 1, 0)
		self.layout.addWidget(self.info_score, 1, 1)
		self.layout.addWidget(self.label_consumption, 2, 0)
		self.layout.addWidget(self.info_consumption, 2, 1)

		self.setLayout(self.layout)



#just for test
if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	form = InfoWidget()
	form.show()
	app.exec_()
