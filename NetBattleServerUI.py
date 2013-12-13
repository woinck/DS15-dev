# -*- coding: utf-8 -*-
import socket,cPickle,sio,time,threading,basic
print 'ui'


conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
	conn.connect((sio.HOST,sio.UI_PORT))
except:
	print 'failed to connect, the program will exit...'
	time.sleep(2)
	exit(1)
	
gameMode = sio.NET_GAME_SERVER
gameMapPath = u'C:\\Users\\woinck\\Documents\\GitHub\\DS15-dev\\new_map.map'

gameAIPath=[]
#若某方（1P,2P）由玩家控制，请将其AIPath设为 None
aiPath = u'C:\\Users\\woinck\\Documents\\GitHub\\DS15-dev\\sclientai.py'
gameAIPath.append(aiPath)
gameAIPath.append(None)

sio._sends(conn,(gameMode,gameMapPath,gameAIPath))

if gameMode == sio.PLAYER_VS_PLAYER or gameMode == sio.PLAYER_VS_AI:
	conn.recv(1)
	cpu_0 = UI_Player(0)
	cpu_0.start()
	if gameMode == sio.PLAYER_VS_PLAYER:
		conn.recv(1)
		cpu_1 = UI_Player(1)
		cpu_1.start()

#接收AI与地图信息
(mapInfo,base,aiInfo) = sio._recvs(conn)
print 'map recv'


#接收每回合信息
rbInfo = sio._recvs(conn)
#展示
rCommand,reInfo = sio._recvs(conn)
while not reInfo.over:
	print 'rInfo recv'
	print 'over=',reInfo.over
	#展示
	rbInfo = sio._recvs(conn)
	rCommand,reInfo = sio._recvs(conn)
winner = sio._recvs(conn)
print 'Player ',winner,' win!'
	
conn.close()
raw_input('ui end')

