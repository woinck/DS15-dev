# -*- coding: UTF-8 -*-
import socket,cPickle,sio,time,basic,os
print 'ai'

#AI需要完成的函数有两个：GetHeroType() 与AI()
def GetHeroType(mapInfo,base):
	return 6
def distance(a,b):
	return abs(a[0]-b[0])+abs(a[1]-b[1])
def AI(whole_map,Info):
	team=Info.id[0]
	unit=Info.id[1]
	self=Info.base[team][unit]
	move=Info.range
	move_id=-1
	for position in move:
		for j in range(0,len(Info.base[1-team])):
			target = Info.base[1-team][j]
			if target.life>0 and (distance(target.position,position) in self.attack_range):
				move_id=j
				c=position
				break
		if move_id!=-1:
			break
	if move_id==-1:
		result = basic.Command(0,self.position,(0,0))
	else:
		result = basic.Command(1,c,(1-team, j))
	print result
	return result	

	
	
aiInfo='Sample'

#==================================================================

conn=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
	conn.connect((sio.HOST,sio.AI_PORT))
	print 'connected!'
except:
	print 'failed to connect, the program will exit...'
	time.sleep(2)
	exit(1)
mapInfo,base=sio._recvs(conn)
sio._sends(conn,(aiInfo,GetHeroType(mapInfo,base)))
print 'info sent'
while True:
	rBeginInfo=sio._recvs(conn)
	print 'rbInfo got'
	if rBeginInfo != '|':
		sio._sends(conn,AI(mapInfo,rBeginInfo))
		print 'cmd sent\n\n'
	else:
		break

conn.close()
print ('ai end')
time.sleep(10)