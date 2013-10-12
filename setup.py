# -*- coding: UTF-8 -*-

from distutils.core import setup
import py2exe,glob

includes = ["encodings", "encodings.*"]	 

py2exe_options = {
		"includes": ["sip"],#pyqt
		'dll_excludes': ['w9xpopen.exe', 'msvcp90.dll',  # 不使用popen，更不用需要支持win98
            "mswsock.dll", "powrprof.dll", "MSVCP90.dll"],
		"compressed": 1,
		"optimize": 2,
		"ascii": 0,
		"bundle_files": 1,
		}
 
setup(console=["Sample_AI.py","Uihumanvsai.py","sclientlogic.py","sserver.py","replayer.py"],
	windows=[{"script":"Uihumanvsai.py"},{"script":"replayer.py"}],
	options={'py2exe': py2exe_options},
	data_files=[#("lib\\human\\image",   
				  # glob.glob("lib\\human\\image\\*.*")),
				   ("Maps",["Sample_Map.map"])])
				   
				   
