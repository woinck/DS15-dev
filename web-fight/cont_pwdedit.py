#-*-coding:UTF-8 -*-

class PassWordEdit(QLineEdit):
	def __init__(self, parent = None):
		super(PassWordEdit, self).__init__(parent)
		
		self.setEchoMode(QLineEdit.Password)
		self.setPlaceholderText(QString.fromUtf8("密码"))
		self.setContextMenuPolicy(Qt.NoContextMenu)
		self.setMaxLength(30)
		self.setStyleSheet("QLineEdit{border-width: 1px; border-radius: 4px; font-size:12px; background-color: lightgrey;color: white; border:1px solid gray;}"
							"QLineEdit:hover{border-width: 1px; border-radius: 4px; font-size:12px; color: white;background-color:grey; border:1px solid rgb(70, 200, 50);}");
	def keyPressEvent(self, event):
		if event.matches(QKeySequence.SelectAll):
			return
		elif event.matches(QKeySequence.Copy):
			return   
		elif event.matches(QKeySequence.Paste):
			return      
		else :
			QLineEdit.keyPressEvent(self, event)

