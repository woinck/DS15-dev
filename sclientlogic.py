# -*- coding: UTF-8 -*-
import socket, cPickle, sio, time, basic, main, threading, sys
import TestBattle_main

print 'logic'

conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
	conn.connect((sio.HOST,sio.LOGIC_PORT))
except:
	print 'failed to connect, the program will exit...'
	time.sleep(2)
	sys.exit(1)
	
print 'platform connected'

TestMain = main

gameMode = sio._recvs(conn)
if (gameMode == sio.TEST_BATTLE):
	level = sio._recvs(conn)
	if level == 1:
		TestMain = TestBattle_main.main1()
	elif level == 2:
		TestMain = TestBattle_main.main2()
	elif level == 3:
		TestMain = TestBattle_main.main3()
	elif level == 4:
		TestMain = TestBattle_main.main4()
	elif level == 5:
		TestMain = TestBattle_main.main5()
	elif level == 6:
		TestMain = TestBattle_main.main6()
	elif level == 7:
		TestMain = TestBattle_main.main7()


begin_Info = sio._recvs(conn)
base = begin_Info.base
whole_map = begin_Info.map
hero_type = begin_Info.hero_type
turn = 0; score = [0,0]; map_temple=[]; over = False

base[0].sort(); base[1].sort()
if base[0]:
	base[0] = [basic.Hero(hero_type[0], base[0][0].position)] + base[0][1:]
if base[1]:
	base[1] = [basic.Hero(hero_type[1], base[1][0].position)] + base[1][1:]

for i in range(0,len(whole_map)):
	for j in range(0,len(whole_map[i])):
		if whole_map[i][j].kind == basic.TEMPLE:
			map_temple += [[(i, j), 0]]
for i in range(0, 2):
	for j in range(0,len(base[i])):
		if whole_map[base[i][j].position[0]][base[i][j].position[1]].kind != basic.MIRROR:
			whole_map[base[i][j].position[0]][base[i][j].position[1]].effect(base, whole_map, (i, j), score)
while not over and turn < basic.TURN_MAX:
	turn += 1
	TestMain.perparation(whole_map, base, score, map_temple)
	for i in range(0, basic.SOLDIERS_NUMBER):
		for j in range(0,2):
			if i >= len(base[j]):
				continue
			if base[j][i].life > 0:
				move_range = TestMain.available_spots(whole_map, base, (j, i))
				roundBeginInfo = basic.Round_Begin_Info((j,i), move_range, base, map_temple)
				#发送每回合的开始信息：
				sio._sends(conn, roundBeginInfo)
				#接收AI的命令：
				try:
					roundCommand = sio._recvs(conn)
				except socket.timeout:
					sys.exit(1)
				roundEndInfo = TestMain.calculation(roundCommand, base, whole_map, move_range, map_temple, score, (j, i))
				over = True
				if turn == basic.TURN_MAX and j == 1:
					for k in range(i + 1, len(base[j])):
						if base[j][i].life > 0:
							over = False
					if over:
						roundEndInfo.over = over
						TestMain.end_score(score,base,turn)
						roundEndInfo.score = score
				#发送每回合结束时的信息：
				sio._sends(conn, roundEndInfo)
				over = roundEndInfo.over
				if over:
					break
		if over:
			break
		
winner = TestMain.end_score(score, base, turn)
print 'winner:',winner
sio._sends(conn, winner)
conn.close()
print 'logic end'
