# -*- coding: UTF-8 -*-

from distutils.core import setup
import py2exe,glob

includes = ["encodings", "encodings.*", "qjpeg4"]	


py2exe_options = {
		"includes": ["sip", "PyQt4.QtNetwork"],#pyqt
		#'dll_excludes': ['w9xpopen.exe', 'msvcp90.dll',  # 不使用popen，更不用需要支持win98
        #    "mswsock.dll", "powrprof.dll", "MSVCP90.dll"],
		'dll_excludes': ['w9xpopen.exe',
            "mswsock.dll", "powrprof.dll"],#, "MSVCP90.dll"],
		"compressed": 1,
		"optimize": 2,
		"ascii": 0,
		"bundle_files": 1,
		}
 
setup(console=["MirroW.py", "sclientlogic.py","sserver.py", "ai_debugger.py"],
	windows=[{"script": "ai_debugger.py", "icon_resources":[(42, "image\\aidebugger.ico")]},
	{"script":"MirroW.py", "icon_resources":[(1, "image\\mirror.ico")]},
	#{"script":"sclientlogic.py"},
	#{"script":"sserver.py"},
	{"script":"ai_debugger.py"}
	], 
	#"icon_resources": [(1, "myicon.ico")]}],#,{"script":"replayer.py"}],
	options={'py2exe': py2exe_options},
	data_files=[#("lib\\human\\image",   
				   ("mapFiles",glob.glob("Maps\\*.map")),

				   #("music",glob.glob('music\\*.*')),
				   #('phonon_backend',['C:\Python27\Lib\site-packages\PyQt4\plugins\phonon_backend\\phonon_ds94.dll']),

				]
				   
	)
				   
				   
