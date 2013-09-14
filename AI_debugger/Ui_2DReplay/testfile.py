#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from Ui_MapEditor import Ui_MapEditor
from testdata import *
import sys


if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    scene = QtGui.QGraphicsScene()
    view = Ui_MapEditor(scene)
    view.Initialize(5, 5)
    view.AddUnit(1, (1, 3))
    view.AddUnit(1, (1, 4))
    view.AddUnit(1, (3, 2))
    view.AddUnit(0, (2, 2))
    view.AddUnit(0, (1, 2))#bug

    view.show()
    sys.exit(app.exec_())
