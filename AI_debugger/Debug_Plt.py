#!/usr/bin/env python
# -*-coding: UTF-8 -*-
#for testing ai_debugger using data in Ui_2DReplay/testdata.py

import socket,sio,time,Ui_2DReplay.testdata

serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#try:
serv.bind((sio.HOST,sio.UI_PORT))
#except:
 #   print 'port occupied, the program will exit...'
  #  time.sleep(3)
  #  exit(1)

serv.listen(1)
connUI, address = serv.accept()
(gameMode,gameMapPath,gameAIPath)=sio._recvs(connUI)
print gameMode,gameMapPath,gameAIPath
aiInfo = []

sio._sends(connUI, (Ui_2DReplay.testdata.maps,aiInfo,Ui_2DReplay.testdata.units0))
#Round 1
sio._sends(connUI, Ui_2DReplay.testdata.begInfo0)
time.sleep(3)
sio._sends(connUI, (Ui_2DReplay.testdata.cmd0, Ui_2DReplay.testdata.endInfo0))
print "re1 send"
time.sleep(8)

#Round 2
sio._sends(connUI, Ui_2DReplay.testdata.begInfo2_)
time.sleep(3)
#Ui_2DReplay.testdata.cmd0 = Ui_2DReplay.testdata.Command(0,(0,0))
sio._sends(connUI, (Ui_2DReplay.testdata.cmd2_, Ui_2DReplay.testdata.endInfo2_))
print "re2 send"
time.sleep(10)

#Round 3
sio._sends(connUI, Ui_2DReplay.testdata.begInfo1)
time.sleep(3)
sio._sends(connUI, (Ui_2DReplay.testdata.cmd1, Ui_2DReplay.testdata.endInfo1))
print "re3 send"
time.sleep(10)
winner = "side1"
sio._sends(connUI,winner)
connUI.close()
serv.close()
