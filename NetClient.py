# -*- coding: UTF-8 -*-
import basic, sio, socket, time, threading, os, subprocess, sys, field


class Net_Client():
	global gp
	result = []
	connAI = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	try:
		connAI.bind(gp.connAIerInfo)
	except:
		print 'port occupied, the program will exit...'
		time.sleep(3)
		sys.exit(1)

	aiConn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	aiConn.connect(sio.HOST,sio.AI_PORT)

	#设定AI连接最大时间
	connAI.settimeout(sio.AI_CONNECT_TIMEOUT)
	connAI.listen(1)
	
	try:
		result.append(connAI.accept())
	except socket.timeout:
		time.sleep(3)
		sys.exit(1)

	return result[0]
















		#与AI进行socket连接
		(connAI2,address2) = _SocketConnect(sio.HOST,sio.AI_PORT,'AI',1)
		
		#设置命令限时
		connAI[i].settimeout(sio.AI_CMD_TIMEOUT)

		#向AI传输游戏初始信息并接收AI的反馈
		while gp.gProc.acquire():
			if gp.gProcess != sio.MAP_SET:
				gp.gProc.wait()
			else:
				for i in range(2):
					if gp.gameMode == sio.TEST_BATTLE and i == 0:
						gp.heroType.append(gp.testBattleGetHeroType(gp.mapInfo,gp.base))
						gp.aiInfo.append('TestBattle_%s' % str(gp.testBattleStage))
					else:
						try:
							if sio.USE_CPP_AI and (gp.gameAIPath[i] != None):
								sio._cpp_sends_begin(connAI[i],i,gp.mapInfo,(len(gp.base[0]),len(gp.base[1])),gp.base)
							else:
								sio._sends(connAI[i],(gp.mapInfo,gp.base))
						except sio.ConnException:
							gp.aiConnErr[i] = True
						try:
							if sio.USE_CPP_AI and (gp.gameAIPath[i] != None):
								gp.aiInfoTemp,gp.heroTypeTemp = sio._cpp_recvs_begin(connAI[i])
							else:
								gp.aiInfoTemp,gp.heroTypeTemp = sio._recvs(connAI[i])
							gp.aiInfo.append(gp.aiInfoTemp)
							gp.heroType.append(gp.heroTypeTemp)
						except socket.timeout:
							print 'fail to receive AI',i,'\'s information, default settings will be used...'
							gp.aiInfo.append('Player'+str(i))
							gp.heroType.append(6)
						
				#调节游戏进度标记
				gp.gProcess = sio.HERO_TYPE_SET
				gp.gProc.notifyAll()
				gp.gProc.release()
				break
			gp.gProc.release()

		#初始化完毕，进入回合==============================================================

		print 'ai in game'#for test 

		#游戏回合阶段
		roundNum = 0
		while gp.gProcess < sio.OVER:
			roundNum =  roundNum + 1
			#将回合开始信息发送至AI，并接收AI的命令
			while gp.rProc.acquire():
				if gp.rProcess != sio.RBINFO_SENT_TO_UI:
					gp.rProc.wait()
				else:
					#清空接收区缓存（其中可能有因超时而没收到的上一回合的命令）
					if connAI[gp.rbInfo.id[0]] != None:
						connAI[gp.rbInfo.id[0]].settimeout(0)
					
						try:
							connAI[gp.rbInfo.id[0]].recv(1024)
						except:
							pass
							
						if gp.timeoutSwitch[gp.rbInfo.id[0]]==1:
							connAI[gp.rbInfo.id[0]].settimeout(sio.AI_CMD_TIMEOUT)
						else:
							connAI[gp.rbInfo.id[0]].settimeout(None)
							
					#计分，用于传输
					if roundNum <= 2:
						tempScore = [0,0]
					else:
						tempScore = gp.reInfo.score
					
					#发送回合信息
					if gp.gameMode != sio.TEST_BATTLE or gp.rbInfo.id[0] == 1:
						try:
							if sio.USE_CPP_AI and gp.gameAIPath[gp.rbInfo.id[0]] != None:
								sio._cpp_sends(connAI[gp.rbInfo.id[0]],gp.rbInfo.id[1],len(gp.rbInfo.temple),gp.rbInfo.temple,(len(gp.rbInfo.base[0]),len(gp.rbInfo.base[1])),gp.rbInfo.base,roundNum,tempScore)
							else:
								sio._sends(connAI[gp.rbInfo.id[0]],gp.rbInfo)
						except sio.ConnException:
							#AI连接错误，标记至connErr中
							gp.aiConnErr[gp.rbInfo.id[0]] = True
						except:
							gp.aiConnErr[gp.rbInfo.id[0]] = True
						

					if gp.aiConnErr[gp.rbInfo.id[0]] == True:
						gp.rCommand = basic.Command()

					elif gp.gameMode == sio.TEST_BATTLE and gp.rbInfo.id[0] == 0:
						gp.rCommand = gp.testBattleAI(gp.mapInfo,gp.rbInfo)

					else:
						try:
							gp.cmdBegin = time.clock()
							if sio.USE_CPP_AI and gp.gameAIPath[gp.rbInfo.id[0]] != None:
								gp.rCommand = sio._cpp_recvs(connAI[gp.rbInfo.id[0]])
								if gp.rCommand.order == 1:
									gp.rCommand.target = [1-gp.rbInfo.id[0],gp.rCommand.target]
								else:
									gp.rCommand.target = [gp.rbInfo.id[0],gp.rCommand.target]
							
							else:
								gp.rCommand = sio._recvs(connAI[gp.rbInfo.id[0]])
							gp.cmdEnd = time.clock()
							#print 'AI',gp.rbInfo.id[0],'\'s command:'
							#sio.cmdDisplay(gp.rCommand)
						except socket.timeout:
							print 'fail to receive cmd, default will be used..',gp.rbInfo.id[0]
							gp.rCommand = basic.Command()
						except sio.ConnException:
							print 'in gp.aiConnErr!!!!!!!!!!!!'
							gp.aiConnErr[gp.rbInfo.id[0]] = True
							gp.rCommand = basic.Command()

					gp.rProcess = sio.RCOMMAND_SET
					gp.rProc.notifyAll()
					gp.rProc.release()
					break
				gp.rProc.release()
			
			#调整回合进度标记
			while gp.rProc.acquire():
				if gp.rProcess == sio.RCOMMAND_SET:
					gp.rProc.wait()
				else:
					gp.rProc.release()
					break
				gp.rProc.release()
			
		#向AI发送结束标志
		if gp.reInfo.over == sio.NORMAL_OVER:
			for i in range(2):
				if connAI[i] != None:
					connAI[i].send('|')
					connAI[i].shutdown(socket.SHUT_RDWR)