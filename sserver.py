# -*- coding: UTF-8 -*-
import basic, sio, socket, time, threading, os, subprocess, sys

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
	print 'waiting for %s connection...\n' %(connName),
	
	for i in range(list):
		#进行连接
		if connName == 'AI' and gp.AI_Debug[i] == True:
			serv.settimeout(None)
		try:
			result.append(serv.accept())
		except socket.timeout:
			print connName,i,'connection failed'
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
		
		#与UI连接
		connUI,address = _SocketConnect(sio.HOST,sio.UI_PORT,'UI')
		connUI.settimeout(1)
		
		#接收游戏模式、地图和AI信息
		gp.gameMode, gp.gameMapPath, gp.gameAIPath, gp.AI_Debug=sio._recvs(connUI)
		
		#设置AI超时开关
		for i in range(2):
			if gp.gameAIPath[i] == None or gp.AI_Debug[i]:
				gp.timeoutSwitch[i] = 0
			else:
				gp.timeoutSwitch[i] = 1
		
		if gp.gameMode <= sio.PLAYER_VS_PLAYER:
			if not sio.DEBUG_MODE:
				sio.Prog_Run(os.getcwd() + sio.LOGIC_FILE_NAME)
				time.sleep(0.1)
			logic_thread.start()
			
		#读取地图
		(gp.mapInfo,gp.base)=sio._ReadFile(gp.gameMapPath)
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
		#等待回合初始信息产生完毕
		while gp.gProcess < sio.OVER:
			while gp.rProc.acquire():
				if gp.rProcess != sio.RBINFO_SET:
					gp.rProc.wait()
				else:
					#发送回合信息
					try:
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
					sio._sends(connUI,gp.winner)
				except:
					connUI.shutdown(socket.SHUT_RDWR)
					sys.exit(1)
				connUI.settimeout(None)
				replay_mode = sio._recvs(connUI)
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
			sio._WriteCppFile(gp.displayInfo, os.getcwd() + sio.DISPLAY_FILE_PATH + sio._ReplayFileName(gp.aiInfo))
		connUI.shutdown(socket.SHUT_RDWR)
		
class Slogic(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = 'Thread-Logic'
	
	def run(self):
		global gp
		try:
			connLogic,address = _SocketConnect(sio.HOST,sio.LOGIC_PORT,'Logic')
			print 'Logic connected'
		except:
			print 'logic connection failed, the program will exit...'
			time.sleep(2)
			sys.exit(1)
					
		#发送游戏初始信息
		while gp.gProc.acquire():
			if gp.gProcess < sio.HERO_TYPE_SET:
				gp.gProc.wait()
			else:
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
			if gp.gameMode != sio.AI_VS_AI:
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
				#print 'logic acquired',gp.rProcess
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
					gp.winner = i
		
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
		[(connAI1,address1),(connAI2,address2)] = _SocketConnect(sio.HOST,sio.AI_PORT,'AI',2)
		connAI=[connAI1,connAI2]
		
		#设置命令限时
		for i in range(2):
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
				if (gp.gameMode != TEST_BATTLE) and (sio.FREE_CHOOSE == 1):
					choice = [[0, 0], [-1, 0]]
					select = [[0, -1], [0, -1]]
					cnum = [0, 0]
					trn = 0
					nsoldier = len(gp.base[0]) - 1
					while (choice[0][cnum[0]-1] < nsoldier) or (choice[1][cnum[1]-1] < nsoldier):
						if trn == 0:
							if choice[0][0] == 0:
								choice[0] = [1, -1]	
								cnum[0] = 1	
							elif choice[0][0] == 1:
								choice[0] = [2, 3]
								cnum[0] = 2
							else:
								choice[0][0] += 2
								choice[0][1] += 2
								cnum[0] = 2
							if choice[0][1] > nsoldier:
								choice[0][1] = -1
								cnum[0] = 1
							if gp.gameAIPath[0] != None:
								sio._cpp_sends_choose(connAI[0], cnum[1], select[1], cnum[0], choice[0])
								sio._cpp_recvs_choose(connAI[0], cnum[0], gp.base, 0, choice[0])
								select[0] = [0, -1]
								for j in range(cnum[0]):
									select[0][j] = gp.base[0][choice[0][j]].kind
							else:
								sio._sends(connAI[0], gp.base)
								gp.base = sio._recvs(connAI[0])
								select[0] = [0, -1]
								for j in range(cnum[0]):
									select[0][j] = gp.base[0][choice[0][j]].kind
						else:
							choice[1][0] += 2
							choice[1][1] += 2
							cnum[1] = 2
							if choice[1][1] > nsoldier:
								choice[1][1] = -1
								cnum[1] = 1
							if gp.gameAIPath[1] != None:
								sio._cpp_sends_choose(connAI[1], cnum[0], select[0], cnum[1], choice[1])
								sio._cpp_recvs_choose(connAI[1], cnum[1], gp.base, 1, choice[1])
								select[1] = [0, -1]
								for j in range(cnum[1]):
									select[1][j] = gp.base[1][choice[1][j]].kind
							else:
								sio._sends(connAI[1], gp.base)
								gp.base = sio._recvs(connAI[1])
								select[1] = [0, -1]
								for j in range(cnum[1]):
									select[1][j] = gp.base[1][choice[1][j]].kind
						trn = 1 - trn
					connAI[0].send('|')
					connAI[0].recv(3)
					if gp.gameAIPath[1] != None:	
						connAI[1].send('|')
						connAI[1].recv(3)



				#调节游戏进度标记
				gp.gProcess = sio.HERO_TYPE_SET
				#print 'gp.heroType set'#for test
				
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
					try:
						if sio.USE_CPP_AI and gp.gameAIPath[gp.rbInfo.id[0]] != None:
							sio._cpp_sends(connAI[gp.rbInfo.id[0]],gp.rbInfo.id[1],len(gp.rbInfo.temple),gp.rbInfo.temple,(len(gp.rbInfo.base[0]),len(gp.rbInfo.base[1])),gp.rbInfo.base,roundNum,tempScore)
						else:
							sio._sends(connAI[gp.rbInfo.id[0]],gp.rbInfo)
						print 'Round BeginInfo sent to AI'
					except sio.ConnException:
						#AI连接错误，标记至connErr中
						gp.aiConnErr[gp.rbInfo.id[0]] = True
					except:
						gp.aiConnErr[gp.rbInfo.id[0]] = True
						
					if gp.aiConnErr[gp.rbInfo.id[0]] == True:
						gp.rCommand = basic.Command()
					else:
						try:
							print 'prepare to receive cmd'
							gp.cmdBegin = time.clock()
							if sio.USE_CPP_AI and gp.gameAIPath[gp.rbInfo.id[0]] != None:
								gp.rCommand = sio._cpp_recvs(connAI[gp.rbInfo.id[0]])
								if gp.rCommand.order == 1:
									gp.rCommand.target = [1-gp.rbInfo.id[0],gp.rCommand.target]
								else:
									gp.rCommand.target = [gp.rbInfo.id[0],gp.rCommand.target]
								print 'cpp cmd recv:::::::::'
								print gp.rCommand.target
							else:
								gp.rCommand = sio._recvs(connAI[gp.rbInfo.id[0]])
								print 'python cmd recv:::::::::'
								print gp.rCommand.target
							gp.cmdEnd = time.clock()
							#print 'AI',gp.rbInfo.id[0],'\'s command:'
							#sio.cmdDisplay(gp.rCommand)
						except socket.timeout:
							print 'fail to receive cmd, default will be used..'
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
				connAI[i].send('|')
				connAI[i].shutdown(socket.SHUT_RDWR)

	
class gameParameter():
	def __init__(self):
		self.gameMode = sio.AI_VS_AI
		self.gameAIPath = []
		self.gameMapPath = None
		self.replayInfo=[] #定义回放列表用于生成回放文件，每个元素储存一个回合的信息
		self.displayInfo = '' #展示组的回放文件
		self.timeoutSwitch = [1,1]
		self.AI_Debug = [False,False]
		
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


if __name__ == "__main__":
	gp = gameParameter()
	#运行线程		
	ui_thread = Sui()
	ai_thread = Sai()
	logic_thread = Slogic()

	ai_thread.daemon = True
	logic_thread.daemon = True

	ui_thread.start()
	ui_thread.join()
