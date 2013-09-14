#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#选择英雄dialog

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import ui_herotypedlg


class GetHeroTypeDlg(QDialog, ui_herotypedlg.Ui_HeroTypeDlg):
    def __init__(self, parent = None):
        super(GetHeroTypeDlg, self).__init__(parent)

        self.setupUi(self)
        self.choice = []
        self.buttons = [self.heroButton1, self.heroButton2, self.heroButton3]
        pal = self.heroButton1.palette()
        for button in self.buttons:
            pal.setBrush(QPalette.Window,QBrush(QPixmap(":hero_%d.png"\
                                                            %(self.buttons.index(button)+1))\
                                                    .scaled(80,80, Qt.IgnoreAspectRatio,
                                                            Qt.SmoothTransformation)))
            button.setPalette(pal)
            self.connect(button, SIGNAL("toggled(bool)"), self.updateUi,Qt.QueuedConnection)

    def updateUi(self, checked):
        button = self.sender()
        if isinstance(button, QPushButton):
            if checked:
                self.choice.append(self.buttons.index(button) + 6)
                if len(self.choice) > 2:
                    button_to_uncheck = self.buttons[self.choice[0] - 6]
                    #有更好的方法没
                    button_to_uncheck.setChecked(False)
                    self.choice.pop(0)
            else:
                if int(self.buttons.index(button)+6) in self.choice:
                    self.choice.pop(self.choice.index(self.buttons.index(button) + 6))



#for test
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = GetHeroTypeDlg()
    form.show()
    app.exec_()
