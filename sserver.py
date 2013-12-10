# -*- coding: UTF-8 -*-
import basic, sio, socket, time, threading, os, subprocess, sys, field
import TestBattle_Map, TestBattle_AI, fieldTest
#import testbattle

def _SocketConnect(host,port,connName,list = 1):
	global gp
	result = []
	serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	try:
		serv.bind((host,port))
	except:
		print 'port occupied, the program will exit...'
		time.sleep(3)
		sys.exit(1)

	#设定AI连接最大时间
	if connName == 'AI':
		if sio.DEBUG_MODE:
			serv.settimeout(None)
		else:
			serv.settimeout(sio.AI_CONNECT_TIMEOUT)
	else:
		serv.settimeout(None)
	serv.listen(list)
	#print 'waiting for %s connection...\n' %(connName),
	
	for i in range(list):
		#进行连接
		if connName == 'AI' and gp.AI_Debug[i] == True:
			serv.settimeout(None)
		try:
			result.append(serv.accept())
		except socket.timeout:
			print connName,i,'connection failed',list
			time.sleep(3)
			sys.exit(1)
		
		#每有一个socket连接成功（两个AI算一个socket）则进程标记+1
		print '\n%s%d connected: %s\n' %(connName,i,result[-1][1]),
		if gp.gProc.acquire():
			gp.gProcess += 1
			gp.gProc.notifyAll()
			gp.gProc.release()
	
	#logic或ui返回
	if len(result) == 1:
		return result[0]
	else:
		return result


class Sui(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = 'Thread-UI'
		
	def run_AI(self, conn, AIPath, num):
		if AIPath == None:
			if gp.gameMode == sio.TEST_BATTLE or gp.gameMode == sio.NET_GAME_CLIENT:
				while gp.gProc.acquire():
					gp.gProcess += 1
					gp.gProc.notifyAll()
					gp.gProc.release()
					break
				return None
			if conn != None:
				try:
					conn.send('|')
				except:
					conn.shutdown(socket.SHUT_RDWR)
					sys.exit(1)
		else:
			if sio.DEBUG_MODE or gp.AI_Debug[num]:
				return None
			else:
				return sio.Prog_Run(AIPath,True)
	def run(self):
		global gp
		
		if len(sys.argv) > 1:
			if gp.gProc.acquire():
				gp.gProcess += 1
				gp.gProc.notifyAll()
				gp.gProc.release()
			connUI = None

		else:
			#与UI连接
			connUI,address = _SocketConnect(sio.HOST,sio.UI_PORT,'UI')
			connUI.settimeout(1)
		
			#接收游戏模式、地图和AI信息
			gp.gameMode, gp.gameMapPath, gp.gameAIPath, gp.AI_Debug = sio._recvs(connUI)

			if gp.gameMode == sio.TEST_BATTLE:
				gp.testBattleStage = sio._recvs(connUI)
				gp.TestBattleStageInit()
			elif gp.gameMode == sio.NET_GAME_CLIENT:
				gp.serverInfo = sio._recvs(connUI) #[IP,PORT]
				try:
					gp.netClient.connect(serverInfo)
				except:
					print 'Connecting to game host failed'


		#设置AI超时开关
		for i in range(2):
			if gp.gameAIPath[i] == None or gp.AI_Debug[i]:
				gp.timeoutSwitch[i] = 0
			else:
				gp.timeoutSwitch[i] = 1
		
		if gp.gameMode <= sio.NET_GAME_SERVER:
			if not sio.DEBUG_MODE:
				LogicProg = sio.Prog_Run(os.getcwd() + sio.LOGIC_FILE_NAME)
				time.sleep(0.1)
			logic_thread.start()

		#读取地图

		if gp.gameMode <= sio.PLAYER_VS_PLAYER or gp.gameMode == sio.NET_GAME_SERVER:
			(gp.mapInfo,gp.base) = sio._ReadFile(gp.gameMapPath)
		elif gp.gameMode == sio.TEST_BATTLE:
			fieldTest.get_map(TestBattle_Map.testBattleMap[gp.testBattleStage],gp.mapInfo,gp.base)

		gp.base[0].sort()
		gp.base[1].sort()
		

		#运行AI线程及文件
		AIProg = []
		
		for i in range(2):
			while gp.gProc.acquire():
				if gp.gProcess != sio.LOGIC_CONNECTED + i:
					gp.gProc.wait()
				else:
					#运行AI连接线程
					if gp.gameMode == sio.NET_GAME_CLIENT:
						if not netai_thread.isAlive():
							netai_thread.start()
					else:	
						if not ai_thread.isAlive():
							ai_thread.start()
					#运行AI1

					AIProg.append(self.run_AI(connUI,gp.gameAIPath[i],i))
					gp.gProc.release()
					break
				gp.gProc.release()

		#所有连接建立后，将游戏进度前调
		while gp.gProc.acquire():
			if gp.gProcess != sio.CONNECTED:
				gp.gProc.wait()
			else:
				gp.gProcess = sio.MAP_SET
				gp.gProc.notifyAll()
				gp.gProc.release()
				break
			gp.gProc.release()

		#AI返回gp.heroType后将其传回界面
		while gp.gProc.acquire():
			if gp.gProcess != sio.HERO_TYPE_SET:
				gp.gProc.wait()
			else:
				try:
					if gp.gameMode != sio.TEST_BATTLE:
						sio._sends(connUI,(gp.mapInfo,gp.base,gp.aiInfo))
				except:
					connUI.shutdown(socket.SHUT_RDWR)
					sys.exit(1)
				gp.replayInfo.append((gp.mapInfo,gp.base,gp.aiInfo))
				gp.displayInfo += sio._display_begin(gp.mapInfo, gp.base, gp.aiInfo)
				gp.gProcess = sio.ROUND
				gp.gProc.notifyAll()
				gp.gProc.release()
				break
			gp.gProc.release()
		

		
		#初始化完毕，进入回合==============================================================
		#print 'ui in game'#for test
		gp.uiOverFlag = False

		if gp.gameMode != sio.NET_GAME_CLIENT:

			#等待回合初始信息产生完毕
			while gp.gProcess < sio.OVER:
				while gp.rProc.acquire():
					if gp.rProcess != sio.RBINFO_SET:
						gp.rProc.wait()
					else:
						#发送回合信息
						try:
							if gp.gameMode != sio.TEST_BATTLE:
								sio._sends(connUI,gp.rbInfo)
						except:
							connUI.shutdown(socket.SHUT_RDWR)
							sys.exit(1)
						gp.rProcess = sio.RBINFO_SENT_TO_UI
						gp.rProc.notifyAll()
						gp.rProc.release()
						break
					gp.rProc.release()
				
				#等待回合所有信息产生完毕
				while gp.rProc.acquire():
					if gp.rProcess != sio.REINFO_SET:
						gp.rProc.wait()
					else:
						gp.reInfo.timeused = (gp.cmdEnd - gp.cmdBegin) * 1000
						
						#发送回合信息
						try:
							if gp.gameMode != sio.TEST_BATTLE:
								sio._sends(connUI,(gp.rCommand,gp.reInfo))
						except:
							connUI.shutdown(socket.SHUT_RDWR)
							sys.exit(1)
						#回合信息存至回放列表中
						gp.replayInfo.append([gp.rbInfo,gp.rCommand,gp.reInfo])
						gp.displayInfo += sio._display_round(gp.rbInfo, gp.rCommand, gp.reInfo)
						gp.rProcess = sio.START
						gp.rProc.notifyAll()
						#若游戏结束则跳出循环
						if gp.reInfo.over:
							gp.uiOverFlag = True
						gp.rProc.release()
						break
					gp.rProc.release()
				if gp.uiOverFlag:
					break
		
		#向UI发送胜利方
		while gp.gProc.acquire():
			if gp.gProcess != sio.WINNER_SET:
				gp.gProc.wait()
			else:
				try:
					if gp.gameMode == sio.TEST_BATTLE:
						sio._sends(connUI,gp.reInfo.score[1])
					elif gp.gameMode == sio.NET_GAME_CLIENT:
						sio._sends(connUI,gp.reInfo)
					sio._sends(connUI,gp.winner)

				except:
					connUI.shutdown(socket.SHUT_RDWR)
					sys.exit(1)
				try:
					connUI.settimeout(None)
				except:
					pass

				if gp.gameMode == sio.TEST_BATTLE or gp.gameMode == sio.NET_GAME_CLIENT:
					replay_mode = False
				else:
					replay_mode = sio._recvs(connUI)
					replay_mode = True

				gp.gProc.notifyAll()
				gp.gProc.release()
				break
			gp.gProc.release()
		
		#存回放文件
		if replay_mode == True:	
			#检验回放文件目录
			try:
				os.mkdir(os.getcwd() + sio.REPLAY_FILE_PATH)
			except:
				pass
			#写入回放
			sio._WriteFile(gp.replayInfo,os.getcwd() + sio.REPLAY_FILE_PATH + sio._ReplayFileName(gp.aiInfo))
			f = file('chusai.txt','a')
			f.write(sys.argv[1]+' '+sys.argv[2]+' '+str(gp.winner)+'\n')
			f.close()
			sio._WriteCppFile(gp.displayInfo, os.getcwd() + sio.DISPLAY_FILE_PATH + sio._ReplayFileName(gp.aiInfo,1))

		for i in AIProg:
			if i != None:
				i.kill()
		try:
			LogicProg.kill()
			connUI.shutdown(socket.SHUT_RDWR)
		except:
			pass


class Slogic(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = 'Thread-Logic'
	
	def run(self):
		global gp
		try:
			connLogic,address = _SocketConnect(sio.HOST,sio.LOGIC_PORT,'Logic')
			#print 'Logic connected'
		except:
			print 'logic connection failed, the program will exit...'
			time.sleep(2)
			sys.exit(1)
		#发送游戏初始信息

		while gp.gProc.acquire():
			if gp.gProcess < sio.HERO_TYPE_SET:
				gp.gProc.wait()
			else:
				sio._sends(connLogic,gp.gameMode)
				if gp.gameMode == sio.TEST_BATTLE:
					sio._sends(connLogic,gp.testBattleStage)
				sio._sends(connLogic,basic.Begin_Info(gp.mapInfo,gp.base,gp.heroType))
				gp.gProc.release()
				break
			gp.gProc.release()	

		#等待其他线程初始化完毕
		while gp.gProc.acquire():
			if gp.gProcess != sio.ROUND:
				gp.gProc.wait()
			else:
				gp.gProc.release()
				break
			gp.gProc.release()

		#初始化完毕，进入回合==============================================================	
		#print 'logic in game'#for test
		
		while gp.gProcess != sio.OVER:
			#接收回合开始信息
			if gp.gameMode != sio.AI_VS_AI and gp.gameMode != sio.TEST_BATTLE:
				time.sleep(1) #time delay
			while gp.rProc.acquire():
				if gp.rProcess != sio.START:
					gp.rProc.wait()
				else:
					gp.rbInfo = sio._recvs(connLogic)
					
					gp.rProcess = sio.RBINFO_SET
					gp.rProc.notifyAll()
					gp.rProc.release()
					break
				gp.rProc.release()
				
			#将命令发送至AI
			while gp.rProc.acquire():
				if gp.rProcess != sio.RCOMMAND_SET:
					gp.rProc.wait()
				else:	
					sio._sends(connLogic,gp.rCommand)
					gp.reInfo = sio._recvs(connLogic)
					
					if gp.aiConnErr[gp.rbInfo.id[0]]:
						gp.reInfo.over = sio.AI_BREAKDOWN
					gp.rProc.release()
					break
				gp.rProc.release()

			#判断游戏是否结束，并调整游戏进度标记
			if gp.reInfo.over != sio.CONTINUE:
				gp.gProc.acquire()
				gp.gProcess = sio.OVER
				gp.gProc.notifyAll()
				gp.gProc.release()

			#调整回合进度标记
			while gp.rProc.acquire():
				gp.rProcess = sio.REINFO_SET
				gp.rProc.notifyAll()
				gp.rProc.release()
				break	
		
		if gp.reInfo.over == sio.NORMAL_OVER:
			gp.winner = sio._recvs(connLogic)
		if gp.reInfo.over == sio.AI_BREAKDOWN:
			for i in range(2):
				if gp.aiConnErr[i] == True:
					gp.winner = 1 - i
		
		#接收胜利方信息
		gp.gProc.acquire()
		gp.gProcess = sio.WINNER_SET
		gp.gProc.notifyAll()
		gp.gProc.release()
		
		connLogic.shutdown(socket.SHUT_RDWR)

class Sai(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = 'Thread-AI'
		self.connErr = False
	
	def run(self):
		global gp

		#与AI进行socket连接
		if gp.gameMode == sio.TEST_BATTLE or gp.gameMode == sio.NET_GAME_CLIENT:
			(connAI2,address2) = _SocketConnect(sio.HOST,sio.AI_PORT,'AI',1)
			connAI1 = None
			address1 = None
		else:
			[(connAI1,address1),(connAI2,address2)] = _SocketConnect(sio.HOST,sio.AI_PORT,'AI',2)
		connAI=[connAI1,connAI2]

		#设置命令限时
		for i in range(2):
			if connAI[i] == None:
				continue
			if gp.timeoutSwitch[i]==1:
				connAI[i].settimeout(sio.AI_CMD_TIMEOUT)
			else:
				connAI[i].settimeout(None)

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
							print 'ConnErr in sending beginInfo'
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

		#print 'ai in game'#for test 

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
						gp.rCommand = basic.Command(0, gp.base[gp.rbInfo.id[0]][gp.rbInfo.id[1]].position, [0, 0])

					elif gp.gameMode == sio.TEST_BATTLE and gp.rbInfo.id[0] == 0:
						gp.rCommand = gp.testBattleAI(gp.mapInfo,gp.rbInfo)

					else:
						try:
							gp.cmdBegin = time.clock()
							if sio.USE_CPP_AI and gp.gameAIPath[gp.rbInfo.id[0]] != None:
								gp.rCommand = sio._cpp_recvs(connAI[gp.rbInfo.id[0]])
								if gp.rCommand.order == 1:
									gp.rCommand.target = [1 - gp.rbInfo.id[0],gp.rCommand.target]
								else:
									gp.rCommand.target = [gp.rbInfo.id[0],gp.rCommand.target]
							
							else:
								gp.rCommand = sio._recvs(connAI[gp.rbInfo.id[0]])
							gp.cmdEnd = time.clock()
							#print 'AI',gp.rbInfo.id[0],'\'s command:'
							#sio.cmdDisplay(gp.rCommand)
						except socket.timeout:
							print 'fail to receive cmd, default will be used..',gp.rbInfo.id[0]
							gp.rCommand = basic.Command(0, gp.base[gp.rbInfo.id[0]][gp.rbInfo.id[1]].position, [0, 0])
						except sio.ConnException:
							print 'in gp.aiConnErr!!!!!!!!!!!!'
							gp.aiConnErr[gp.rbInfo.id[0]] = True
							gp.rCommand = basic.Command(0, gp.base[gp.rbInfo.id[0]][gp.rbInfo.id[1]].position, [0, 0])

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
			
		while gp.gProc.acquire():
			if gp.gProcess < sio.WINNER_SET:
				gp.gProc.wait()
			else:
				gp.gProc.notifyAll()
				gp.gProc.release()
				break
			gp.rProc.release()

		#向AI发送结束标志
		if gp.reInfo.over == sio.NORMAL_OVER:
			for i in range(2):
				if connAI[i] != None:
					connAI[i].send('|')
					if gp.gameMode == sio.NET_GAME_SERVER and i == 1:
						sio._sends(connAI[i],gp.reInfo.score)
						sio._sends(connAI[i],gp.winner)
					connAI[i].shutdown(socket.SHUT_RDWR)


class Netai(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = 'Thread-NetAI'
		self.connErr = False
	
	def run(self):
		global gp

		#与AI进行socket连接
		(connAI,address) = _SocketConnect(sio.HOST,sio.AI_PORT,'AI',1)

		#设置命令限时
		connAI.settimeout(sio.AI_CMD_TIMEOUT)

		#向AI传输游戏初始信息并接收AI的反馈
		while gp.gProc.acquire():
			if gp.gProcess != sio.MAP_SET:
				gp.gProc.wait()
			else:
				
				try:
					gp.mapInfo,gp.base = sio._recvs(gp.netClient)
				except:
					print 'net client recv beginInfo failed'

				try:
					sio._cpp_sends_begin(connAI,1,gp.mapInfo,(len(gp.base[0]),len(gp.base[1])),gp.base)
				except sio.ConnException:
					gp.aiConnErr[i] = True
					print 'ConnErr in sending beginInfo'

				try:
					
					gp.aiInfoTemp,gp.heroTypeTemp = sio._cpp_recvs_begin(connAI[i])	
					gp.aiInfo.append(gp.aiInfoTemp)
					gp.heroType.append(gp.heroTypeTemp)
					
					#发送AI信息
					sio._sends(gp.netClient,(gp.aiInfoTemp,gp.heroTypeTemp))
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


		#游戏回合阶段
		while True:
			gp.rbInfo = sio._recvs(netClient)
			roundNum = sio._recvs(netClient)
			if gp.rbInfo != '|':
				#清空接收区缓存（其中可能有因超时而没收到的上一回合的命令）
				connAI.settimeout(0)
				try:
					connAI.recv(1024)
				except:
					pass
				connAI.settimeout(sio.AI_CMD_TIMEOUT)
					
					
				#发送回合信息
				
				try:
					sio._cpp_sends(connAI[gp.rbInfo.id[0]],gp.rbInfo.id[1],len(gp.rbInfo.temple),gp.rbInfo.temple,(len(gp.rbInfo.base[0]),len(gp.rbInfo.base[1])),gp.rbInfo.base,roundNum,tempScore)
				except sio.ConnException:
					#AI连接错误，标记至connErr中
					gp.aiConnErr[gp.rbInfo.id[0]] = True
				except:
					gp.aiConnErr[gp.rbInfo.id[0]] = True
				
				if gp.aiConnErr[gp.rbInfo.id[0]] == True:
					gp.rCommand = basic.Command()
				else:
					try:
						gp.cmdBegin = time.clock()
						
						gp.rCommand = sio._cpp_recvs(connAI[gp.rbInfo.id[0]])
						if gp.rCommand.order == 1:
							gp.rCommand.target = [1 - gp.rbInfo.id[0],gp.rCommand.target]
						else:
							gp.rCommand.target = [gp.rbInfo.id[0],gp.rCommand.target]
												
						gp.cmdEnd = time.clock()
						
					except socket.timeout:
						print 'fail to receive cmd, default will be used..',gp.rbInfo.id[0]
						gp.rCommand = basic.Command()
					except sio.ConnException:
						print 'in gp.aiConnErr!!!!!!!!!!!!'
						gp.aiConnErr[gp.rbInfo.id[0]] = True
						gp.rCommand = basic.Command()

				sio._sends(gp.netClient,gp.rCommand)
			else:
				break
				
		gp.reInfo = sio._recvs(netClient)
		gp.winner = sio._recvs(netClient)

		gp.gProc.acquire()
		gp.gProcess = sio.WINNER_SET
		gp.gProc.notifyAll()
		gp.gProc.release()


###########################################################################################################


	
class gameParameter():
	def __init__(self):
		self.gameMode = sio.AI_VS_AI
		self.gameAIPath = []
		self.gameMapPath = None
		self.testBattleStage = 0
		self.serverInfo = ['127.0.0.1',sio.AI_PORT]
		self.replayInfo=[] #定义回放列表用于生成回放文件，每个元素储存一个回合的信息
		self.displayInfo = '' #展示组的回放文件
		self.timeoutSwitch = [1,1]
		self.AI_Debug = [False,False]

		self.testBattleAI = None
		self.testBattleGetHeroType = None
		
		self.mapInfo = []
		self.base = [[], []]
		self.aiInfo = []
		self.heroType = []
		self.aiConnErr = [False,False]
		self.winner = -1
		self.uiOverFlag = False
		
		#回合阶段变量
		self.rbInfo = None
		self.reInfo = None
		self.rCommand = None
		self.cmdBegin = 0
		self.cmdEnd = 0

		#设置进度标记
		self.gProcess = sio.START
		self.rProcess = sio.START
		self.gProc = threading.Condition()
		self.rProc = threading.Condition()

	def TestBattleStageInit(self):
		if (self.testBattleStage == 1):
			self.testBattleAI = TestBattle_AI.AI_1
			self.testBattleGetHeroType = TestBattle_AI.GetHeroType_1
		elif (self.testBattleStage == 2):
			self.testBattleAI = TestBattle_AI.AI_2
			self.testBattleGetHeroType = TestBattle_AI.GetHeroType_2
		elif (self.testBattleStage == 3):
			self.testBattleAI = TestBattle_AI.AI_3
			self.testBattleGetHeroType = TestBattle_AI.GetHeroType_3
		elif (self.testBattleStage == 4):
			self.testBattleAI = TestBattle_AI.AI_4
			self.testBattleGetHeroType = TestBattle_AI.GetHeroType_4
		elif (self.testBattleStage == 5):
			self.testBattleAI = TestBattle_AI.AI_5
			self.testBattleGetHeroType = TestBattle_AI.GetHeroType_5
		elif (self.testBattleStage == 6):
			self.testBattleAI = TestBattle_AI.AI_6
			self.testBattleGetHeroType = TestBattle_AI.GetHeroType_6
		elif (self.testBattleStage == 7):
			self.testBattleAI = TestBattle_AI.AI_7
			self.testBattleGetHeroType = TestBattle_AI.GetHeroType_7
if __name__ == "__main__":
	
	gp = gameParameter()

	if len(sys.argv) > 1:
		gp.gameAIPath.append(sys.argv[1])
		gp.gameAIPath.append(sys.argv[2])
		gp.gameMapPath = sys.argv[3]

	#运行线程		
	ui_thread = Sui()
	ai_thread = Sai()
	netai_thread = Netai()
	logic_thread = Slogic()

	ai_thread.daemon = True
	logic_thread.daemon = True

	ui_thread.start()
	ui_thread.join()
