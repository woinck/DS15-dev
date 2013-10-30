# -*- coding: UTF-8 -*-
import socket, cPickle, sio, time, basic, main, threading


print 'logic'
serv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
	serv.bind((sio.HOST,sio.LOGIC_PORT))
except:
	print 'port occupied, the program will exit...'
	time.sleep(3)
	exit(1)
serv.listen(1)
print 'waiting for platform connection...\n',
conn,address = serv.accept()
print 'platform connected: %s' %(str(address))

begin_Info = sio._recvs(conn)
base = begin_Info.base
whole_map = begin_Info.map
hero_type = begin_Info.hero_type
turn = 0; score = [0,0]; map_temple=[]; over = False

base[1] = [basic.Hero(hero_type[1], base[1][0].position)]
while not over and turn < basic.TURN_MAX:
	turn += 1
	main.perparation(whole_map, base, score, map_temple)
	i = 0; j = 1
	move_range = main.available_spots(whole_map, base, (j, i))
	roundBeginInfo = basic.Round_Begin_Info((j,i), move_range, base, map_temple)
	#发送每回合的开始信息：
	sio._sends(conn, roundBeginInfo)
	#接收AI的命令：
	roundCommand = sio._recvs(conn)
	roundEndInfo = main.calculation(roundCommand, base, whole_map, move_range, map_temple, score, (j, i))
	if turn == basic.TURN_MAX:
		over =  True
	else:
		over = False
	if over:
		roundEndInfo.over = over
	#发送每回合结束时的信息：
	sio._sends(conn, roundEndInfo)		
winner = main.end_score(score, base, turn)
print 'winner:',winner
sio._sends(conn, winner)
conn.close()
print 'logic end'
