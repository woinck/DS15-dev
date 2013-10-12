# -*- coding: UTF-8 -*-
#animation used by main window

from PyQt4.QtGui import *
from PyQt4.QtCore import *

def MenuAnimation(formerWidget, aimWidget):
	if formerWidget:
		 y = formerWidget.widget().y()

	if formerWidget:
		DisWidget = QPropertyAnimation(formerWidget.widget(), "windowOpacity")
		DisWidget.setDuration(500)
		DisWidget.setKeyValueAt(1, 0)
		DisWidget.setEasingCurve(QEasingCurve.InOutQuad)

	if aimWidget:
		AppWidget = QPropertyAnimation(aimWidget.widget(), "windowOpacity")
		AppWidget.setDuration(1000)
		AppWidget.setKeyValueAt(1, 1)
		AppWidget.setEasingCurve(QEasingCurve.InOutQuad)

	if formerWidget:
		fPingWidget = QPropertyAnimation(formerWidget, "y")
		fPingWidget.setDuration(500)
		fPingWidget.setKeyValueAt(0, y)
		fPingWidget.setKeyValueAt(1, y-900)
		fPingWidget.setEasingCurve(QEasingCurve.InOutQuad)

	if aimWidget:
		aPingWidget = QPropertyAnimation(aimWidget, "y")
		aPingWidget.setDuration(1000)
		aPingWidget.setKeyValueAt(0.001, y - 900)
		aPingWidget.setKeyValueAt(0.5,y)
		for i in range(5):
			aPingWidget.setKeyValueAt(0.5 + 0.05 * (2 * i + 1 )  , y - 200 / (i + 1 ))
			aPingWidget.setKeyValueAt(0.5 + 0.1 * ( i + 1 ) , y)

		aPingWidget.setKeyValueAt(1,y)
		aPingWidget.setEasingCurve(QEasingCurve.InOutQuad)

	parallelWid = QParallelAnimationGroup()
	if formerWidget:
		parallelWid.addAnimation(DisWidget)
		parallelWid.addAnimation(fPingWidget)
	if aimWidget:
		parallelWid.addAnimation(AppWidget)
		parallelWid.addAnimation(aPingWidget)

	return parallelWid

def MenuToWindowAnimation(formerWidget, aimWidget):
	if formerWidget:
		y = formerWidget.widget().y()
	else:
		y = aimWidget.widget().y()

	if formerWidget:
		DisWidget = QPropertyAnimation(formerWidget.widget(), "windowOpacity")
		DisWidget.setDuration(500)
		DisWidget.setKeyValueAt(0, 1)
		DisWidget.setKeyValueAt(1, 0)
		DisWidget.setEasingCurve(QEasingCurve.InOutQuad)

	if aimWidget:
		AppWidget = QPropertyAnimation(aimWidget.widget(), "windowOpacity")
		AppWidget.setDuration(1000)
		AppWidget.setKeyValueAt(0, 0)
		AppWidget.setKeyValueAt(0.4, 0)
		AppWidget.setKeyValueAt(1, 1)
		AppWidget.setEasingCurve(QEasingCurve.InOutQuad)

	if formerWidget:
		fPingWidget = QPropertyAnimation(formerWidget, "y")
		fPingWidget.setDuration(500)
		fPingWidget.setKeyValueAt(0, y)
		fPingWidget.setKeyValueAt(1, y - 900)
		fPingWidget.setEasingCurve(QEasingCurve.InOutQuad)

	parallelWid = QParallelAnimationGroup()
	if formerWidget:
		parallelWid.addAnimation(DisWidget)
		parallelWid.addAnimation(fPingWidget)
	if aimWidget:
		parallelWid.addAnimation(AppWidget)

	return parallelWid

def WindowToMenuAnimation(formerWidget, aimWidget):
	if aimWidget:
		 y = aimWidget.widget().y()
	else:
		 y = formerWidget.widget().y()

	if formerWidget:
		DisWidget =  QPropertyAnimation(formerWidget.widget(), "windowOpacity")
		DisWidget.setDuration(500)
		DisWidget.setKeyValueAt(0.00001,1)
		DisWidget.setKeyValueAt(1,0)
		DisWidget.setEasingCurve(QEasingCurve.InOutQuad)

	if aimWidget:
		AppWidget =  QPropertyAnimation(aimWidget.widget(), "windowOpacity")
		AppWidget.setDuration(1000)
		AppWidget.setKeyValueAt(0.00001,0)
		AppWidget.setKeyValueAt(0.4,0)
		AppWidget.setKeyValueAt(1,1)
		AppWidget.setEasingCurve(QEasingCurve.InOutQuad)

	if aimWidget:
		aPingWidget =  QPropertyAnimation(aimWidget, "y")
		aPingWidget.setDuration(1000)
		aPingWidget.setKeyValueAt(0.00001,y-900)
		aPingWidget.setKeyValueAt(0.5,y)
		for i in range(5):
			aPingWidget.setKeyValueAt(0.5 + 0.05 * (2 * i + 1 )  , y - 200 / (i + 1 ))
			aPingWidget.setKeyValueAt(0.5 + 0.1 * ( i + 1 ) , y)

		aPingWidget.setKeyValueAt(1,y)
		aPingWidget.setEasingCurve(QEasingCurve.InOutQuad)


	parallelWid =  QParallelAnimationGroup()
	if formerWidget:
		parallelWid.addAnimation(DisWidget)
	if aimWidget:
		parallelWid.addAnimation(AppWidget)
		parallelWid.addAnimation(aPingWidget)

	return parallelWid

def WindowAnimation(formerWidget, aimWidget):
	if formerWidget:
		DisWidget =  QPropertyAnimation(formerWidget.widget(), "windowOpacity")
		DisWidget.setDuration(500)
		DisWidget.setStartValue(1)
		DisWidget.setKeyValueAt(0.00001,1)
		DisWidget.setKeyValueAt(1,0)
		DisWidget.setEasingCurve(QEasingCurve.InOutQuad)
		
	if aimWidget:
		AppWidget = QPropertyAnimation(aimWidget.widget(), "windowOpacity")
		AppWidget.setDuration(800)
		AppWidget.setKeyValueAt(0, 0)
		AppWidget.setKeyValueAt(0.4, 0)
		AppWidget.setKeyValueAt(1, 1)
		AppWidget.setEasingCurve(QEasingCurve.InOutQuad)
	
	parallelWid = QParallelAnimationGroup()
	if formerWidget:
		parallelWid.addAnimation(DisWidget)
	if aimWidget:
		parallelWid.addAnimation(AppWidget)
		
	return parallelWid