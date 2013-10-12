# -*- coding: UTF-8 -*-

from distutils.core import setup
import py2exe,glob

includes = ["encodings", "encodings.*", "qjpeg4"]	 

py2exe_options = {
		"includes": ["sip"],#pyqt
		'dll_excludes': ['w9xpopen.exe', 'msvcp90.dll',  # 不使用popen，更不用需要支持win98
            "mswsock.dll", "powrprof.dll", "MSVCP90.dll"],
		"compressed": 1,
		"optimize": 2,
		"ascii": 0,
		"bundle_files": 3,
		}
 
setup(console=["Sample_AI.py","runMain.py","Uihumanvsai.py","sclientlogic.py","sserver.py","replayer.py"],
	windows=[{"script":"runMain.py"}], 
	#"icon_resources": [(1, "myicon.ico")]}],#,{"script":"replayer.py"}],
	options={'py2exe': py2exe_options},
	zipfile=None,
	data_files=[#("lib\\human\\image",   
				  # glob.glob("lib\\human\\image\\*.*")),
				   ("mapFiles",["mapwithturret.map"])])
				   
				   
