# -*- coding: UTF-8 -*-

from distutils.core import setup
import py2exe,glob

includes = ["encodings", "encodings.*"]	 

setup(console=["Sample_AI.py","Uihumanvsai.py","sclientlogic.py","sserver.py"],
	options={"py2exe":{"includes":["sip"]}},
	data_files=[("lib\\human\\image",   
                   glob.glob("lib\\human\\*.*"))])