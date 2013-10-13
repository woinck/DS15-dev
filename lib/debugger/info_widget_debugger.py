#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#Fox Ning
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import basic

#Three dictionaries for show types of map or unit
NumToMapType = {0:"平原",1:"山地",2:"森林",3:"屏障",4:"炮塔",
				 5:"遗迹",6:"传送门"}
NumToUnitType = {0:"剑士",1:"突击手",2:"狙击手",3:"战斗机",
				4:"肉搏者", 5:"治疗师", 6:"狂战士", 7:"暗杀者",
				8:"大法师"}
NumToActionType = {0:"待机", 1:"攻击", 2:"技能"}
NumToTempleType = {0:"无神符", 1:"力量神符", 2:"敏捷神符", 3:"防御神符"}
NumToEffectType = {0:"未命中", 1:"命中", -1:"未进行"}
StyleSheet = """
QLineEdit{
background-color: rgb(255, 255, 127);
color: darkblue;
}
"""
class InfoWidget(QTabWidget):
	def __init__(self, parent =None):
		super(InfoWidget, self).__init__(parent)

		self.infoWidget_Game = InfoWidget1()
		self.infoWidget_Unit = InfoWidget2()
		self.infoWidget_Map = InfoWidget3()
		self.addTab(self.infoWidget_Game, "Game info")
		self.addTab(self.infoWidget_Unit, "Unit info")
		self.addTab(self.infoWidget_Map, "Map info")
		self.setTabToolTip(1, "the global infos and game runing infos")
		self.setTabToolTip(2, "the selected unit's infos")
		self.setTabToolTip(3, "the selected map-grid's infos")

	#reimplement close event:仅仅设置它不可见,而不是关闭
	def closeEvent(self, event):
		self.hide()
		event.ignore()
	#为了同步主界面窗口菜单的显示加入的event handler
	def hideEvent(self, event):
		self.emit(SIGNAL("hided()"))
	#展现战斗信息
	def beginRoundInfo(self, beginfo):
		self.infoWidget_Game.resetEnd()
		self.infoWidget_Game.setUnitinfo("Team %d Soldier %d" %(beginfo.id[0],beginfo.id[1]))
		self.beg_Flag = 1
	def endRoundInfo(self, cmd, endinfo):
		self.infoWidget_Game.setCmdinfo(QString.fromUtf8("移动至%s,%s" %(cmd.move,
															 NumToActionType[cmd.order]
															 )))
		if cmd.order != 0:
			self.infoWidget_Game.setTargetinfo(QString.fromUtf8("%d队%d号单位" %(cmd.target[0], cmd.target[1])))
		self.infoWidget_Game.setEffectinfo(QString.fromUtf8("攻击%s，反击%s" %(NumToEffectType[endinfo.effect[0]],
															  NumToEffectType[endinfo.effect[1]])))
		self.infoWidget_Game.setTimeInfo("%d ms" %endinfo.timeused)
		#self.infoWidget_Game.setScoreinfo("%d : %d" %(endinfo.score[0],endinfo.score[1]))
		self.beg_Flag = 0
	def on_goToRound(self, _round, status, begInfo, endInfo):
		self.infoWidget_Game.info_round.setText("%d" %_round)
		self.beginRoundInfo(begInfo)
		if endInfo:
			self.endRoundInfo(*endInfo)

		#待实现,在跳转回合时从回放里设置的类传出的信号设置
	#展现单位,地形信息
	def newUnitInfo(self, base_unit):
		self.infoWidget_Unit.info_type.setText(QString.fromUtf8(NumToUnitType[base_unit.kind]))
		self.infoWidget_Unit.info_life.setText("%d" %base_unit.life)
		self.infoWidget_Unit.info_attack.setText("%d" %base_unit.strength)
		self.infoWidget_Unit.info_defence.setText("%d" %base_unit.defence)
		#self.infoWidget_Unit.info_speed.setText("%d" %base_unit.agility)
		self.infoWidget_Unit.info_moverange.setText("%d" %base_unit.move_range)
		self.infoWidget_Unit.info_attackrange.setText("%s" %base_unit.attack_range)

	def newMapInfo(self, map_basic, tp):
		self.infoWidget_Map.info_type.setText(QString.fromUtf8(NumToMapType[map_basic.kind]))
		self.infoWidget_Map.info_score.setText("%d" %map_basic.score)
		self.infoWidget_Map.info_consumption.setText("%d" %map_basic.move_consumption)
		if isinstance(map_basic, basic.Map_Temple):
			self.infoWidget_Map.info_temple.setText(QString.fromUtf8("%s"%NumToTempleType[tp]))
#cd = basic.TEMPLE_UP_TIME - map_basic.time if (basic.TEMPLE_UP_TIME - map_basic.time) > 0 else 0
#			self.infoWidget_Map.info_cd.setText("%d" %cd)
		else:
			self.infoWidget_Map.info_temple.setText("")

#展示游戏基础信息
class InfoWidget1(QWidget):
	def __init__(self, parent = None):
		super(InfoWidget1, self).__init__(parent)

		self.label_aifile = QLabel("AI file path:")
		self.info_aifile1 = QLineEdit("")
		self.info_aifile1.setReadOnly(True)
		self.info_aifile2 = QLineEdit("")
		self.info_aifile2.setReadOnly(True)
		self.label_mapfile = QLabel("MAP file path:")
		self.info_mapfile = QLineEdit("")
		self.info_mapfile.setReadOnly(True)
		self.label_round = QLabel(QString.fromUtf8("回合数:"))
		self.info_round = QLineEdit("")
		self.info_round.setReadOnly(True)
		self.label_unit = QLabel(QString.fromUtf8("行动单位:"))
		self.info_unit = QLineEdit("")
		self.info_unit.setReadOnly(True)
		self.label_time = QLabel(QString.fromUtf8("用时:"))
		self.info_time = QLineEdit("")
		self.info_time.setReadOnly(True)
		self.label_cmd = QLabel(QString.fromUtf8("命令:"))
		self.info_cmd = QLineEdit("")
		self.info_cmd.setReadOnly(True)
		self.label_target = QLabel(QString.fromUtf8("目标:"))
		self.info_target = QLineEdit("")
		self.info_cmd.setReadOnly(True)
		self.label_effect = QLabel(QString.fromUtf8("攻击效果:"))
		self.info_effect = QLineEdit("")
		self.info_effect.setReadOnly(True)
		#self.label_score = QLabel("socre:")
		#self.info_score = QLineEdit("0:0")
		#self.info_score.setReadOnly(True)

		self.layout = QGridLayout()
		self.layout.addWidget(self.label_aifile, 0, 0)
		self.layout.addWidget(self.info_aifile1, 0, 1)
		self.layout.addWidget(self.info_aifile2, 1, 1)
		self.layout.addWidget(self.label_mapfile, 2, 0)
		self.layout.addWidget(self.info_mapfile, 2, 1)
		self.layout.addWidget(self.label_time, 3, 0)
		self.layout.addWidget(self.info_time, 3, 1)
		self.layout.addWidget(self.label_round, 4, 0)
		self.layout.addWidget(self.info_round, 4, 1)
		self.layout.addWidget(self.label_unit, 5, 0)
		self.layout.addWidget(self.info_unit, 5, 1)
		self.layout.addWidget(self.label_cmd, 6, 0)
		self.layout.addWidget(self.info_cmd, 6, 1)
		self.layout.addWidget(self.label_target, 7, 0)
		self.layout.addWidget(self.info_target, 7, 1)
		self.layout.addWidget(self.label_effect, 8, 0)
		self.layout.addWidget(self.info_effect, 8, 1)
	#	self.layout.addWidget(self.label_score, 8, 0)
	#	self.layout.addWidget(self.info_score, 8, 1)

		self.setLayout(self.layout)
		self.setStyleSheet(StyleSheet)
	def setAiFileinfo(self, loaded_ai):
		self.info_aifile1.setText(loaded_ai[0])
		if len(loaded_ai) == 2:
			self.info_aifile2.setText(loaded_ai[1])
		else:
			self.info_aifile2.setText("Default")
			
	def setMapFileinfo(self, str):
		self.info_mapfile.setText(str)
	def setUnitinfo(self, str):
		self.info_unit.setText(str)
	def setTimeinfo(self, str):
		self.info_time.setText(str)
	def setCmdinfo(self, str):
		self.info_cmd.setText(str)
	def setTargetinfo(self, str):
		self.info_target.setText(str)
	def setEffectinfo(self,str):
		self.info_effect.setText(str)
	#def setScoreinfo(self, str):
	#	self.info_score.setText(str)
	def resetEnd(self):
		self.setTargetinfo("")
		self.setEffectinfo("")
		self.setCmdinfo("")
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
		#self.label_speed = QLabel(QString.fromUtf8("敏捷:"))
		#self.info_speed = QLabel("")
		#self.infos.append(self.info_speed)
		self.label_defence = QLabel(QString.fromUtf8("防御:"))
		self.info_defence = QLabel("")
		self.infos.append(self.info_defence)
		self.label_moverange = QLabel(QString.fromUtf8("移动力:"))
		self.info_moverange = QLabel("")
		self.infos.append(self.info_moverange)
		self.label_attackrange = QLabel(QString.fromUtf8("攻击范围:"))
		self.info_attackrange = QLabel("")
		self.infos.append(self.info_attackrange)

		labels = [self.label_type, self.label_attack, self.label_life, 
					self.label_defence, self.label_attackrange, self.label_moverange]

		#old_font = self.font()
		#new_font = QFont()
		#new_font.setBold(True)
		#new_font.setPointSize(old_font.pointSize() + 3)

		
		#pal = self.label_type.palette()
		#pal.setBrush(QPalette.WindowText, QColor(Qt.white))

		for info in self.infos:
	#		info.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
			info.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
	#		info.setFont(new_font)
	#		info.setPalette(pal)
	#	for label in labels:
	#		label.setFont(new_font)
			# label.setPalette(pal)

		self.layout = QGridLayout()
		self.layout.addWidget(self.label_type, 0, 0)
		self.layout.addWidget(self.info_type, 0, 1)
		self.layout.addWidget(self.label_life, 1, 0)
		self.layout.addWidget(self.info_life, 1, 1)
		self.layout.addWidget(self.label_attack, 2, 0)
		self.layout.addWidget(self.info_attack, 2, 1)
		self.layout.addWidget(self.label_defence, 3, 0)
		self.layout.addWidget(self.info_defence, 3, 1)
	#	self.layout.addWidget(self.label_speed, 4, 0)
#		self.layout.addWidget(self.info_speed, 4, 1)
		self.layout.addWidget(self.label_moverange, 4, 0)
		self.layout.addWidget(self.info_moverange, 4, 1)
		self.layout.addWidget(self.label_attackrange, 5, 0)
		self.layout.addWidget(self.info_attackrange, 5, 1)

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
		self.label_temple = QLabel(QString.fromUtf8("神符种类:"))
		self.info_temple = QLabel("")
		self.infos.append(self.info_temple)
	#	self.label_cd = QLabel(QString.fromUtf8("神符冷却:"))
	#	self.info_cd = QLabel("")
	#	self.infos.append(self.info_cd)
		labels = [self.label_type, self.label_consumption, self.label_score,self.label_temple]
#				self.label_cd]

		# old_font = self.font()
		# new_font = QFont()
	#	new_font.setBold(True)
	#	new_font.setPointSize(old_font.pointSize() + 3)

	#	pal = self.label_type.palette()
	#	pal.setBrush(QPalette.WindowText, QColor(Qt.white))

		for info in self.infos:
	#		info.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
			info.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
	#		info.setFont(new_font)
	#		info.setPalette(pal)
	#	for label in labels:
	#		label.setFont(new_font)
	#		label.setPalette(pal)

		self.layout = QGridLayout()
		self.layout.addWidget(self.label_type, 0, 0)
		self.layout.addWidget(self.info_type, 0, 1)
		self.layout.addWidget(self.label_score, 1, 0)
		self.layout.addWidget(self.info_score, 1, 1)
		self.layout.addWidget(self.label_consumption, 2, 0)
		self.layout.addWidget(self.info_consumption, 2, 1)
		self.layout.addWidget(self.label_temple, 3, 0)
		self.layout.addWidget(self.info_temple, 3 ,1)
	#	self.layout.addWidget(self.label_cd, 4, 0)
	#	self.layout.addWidget(self.info_cd, 4, 1)

		self.setLayout(self.layout)


#just for test
if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	form = InfoWidget()
	form.show()
	app.exec_()
