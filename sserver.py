# -*- coding: UTF-8 -*-
import sio, socket, time, threading, os,subprocess
from field_shelve import *


def _SocketConnect(host,port,connName,list = 1):
	global gProcess,gProc
	result = []
	serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	try:
		serv.bind((host,port))
	except:
		print 'port occupied, the program will exit...'
		time.sleep(3)
		exit(1)
		
	#设定AI连接最大时间
	if connName == 'AI':
		print 'waiting ai'
		if sio.DEBUG_MODE or sio.AI_DEBUG:
			serv.settimeout(None)
		else:
			serv.settimeout(sio.AI_CONNECT_TIMEOUT)
		print '\n',
	else:
		serv.settimeout(None)
	serv.listen(list)
	print 'waiting for %s connection...\n' %(connName),
	
	for i in range(list):
		#进行连接
		try:
			result.append(serv.accept())
		except socket.timeout:
			print connName,i,'connection failed'
			time.sleep(3)
			exit(1)
		
		#每有一个socket连接成功（两个AI算一个socket）则进程标记+1
		print '\n%s%d connected: %s\n' %(connName,i,result[-1][1]),
		if gProc.acquire():
			gProcess += 1
			gProc.notifyAll()
			gProc.release()
	
	#logic或ui返回
	if len(result) == 1:
		return result[0]
	else:
		return result

class Sui(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = 'Thread-UI'
		
	def run_AI(self,conn,AIPath):
		if AIPath == None:
			try:
				conn.send('|')
			except:
				conn.shutdown(socket.SHUT_RDWR)
				exit(1)
		else:
			if sio.DEBUG_MODE or sio.AI_DEBUG:
				return None
			else:
				print 'ai running'
				return sio.Prog_Run(AIPath,True)
	def run(self):
		global gProcess,rProcess
		global mapInfo,base,heroType,aiInfo,gameMode,timeoutSwitch,aiConnErr,gameAIPath
		global rbInfo,reInfo,rCommand
		global ai_thread,logic_thread
		
		#定义回放列表用于生成回放文件，每个元素储存一个回合的信息
		replayInfo=[]
		
		#与UI连接
		connUI,address = _SocketConnect(sio.HOST,sio.UI_PORT,'UI')
		connUI.settimeout(1)
		
		#接收游戏模式、地图和AI信息
		gameMode,gameMapPath,gameAIPath=sio._recvs(connUI)
		
		#设置AI超时开关
		for i in range(2):
			if gameAIPath[i]==None or sio.AI_DEBUG:
				timeoutSwitch[i]=0
			else:
				timeoutSwitch[i]=1
		
		if gameMode <= sio.PLAYER_VS_PLAYER:
			if not sio.DEBUG_MODE:
				sio.Prog_Run(os.getcwd() + sio.LOGIC_FILE_NAME)
				time.sleep(0.1)
			logic_thread.start()
		
		#读取地图文件
		#print 'gameAIPath: ',gameAIPath#for test
		#print 'gameMapPath: ',gameMapPath#for test
		#(mapInfo,base)=read_from(gameMapPath)		
		(mapInfo,base)=sio._ReadFile(gameMapPath)
		#运行AI线程及文件
		AIProg = []
		while gProc.acquire():
			if gProcess != sio.LOGIC_CONNECTED:
				gProc.wait()
			else:
				#运行AI连接线程
				ai_thread.start()
				#运行AI1
				AIProg.append(self.run_AI(connUI,gameAIPath[0]))
				gProc.release()
				break
			gProc.release()

		while gProc.acquire():
			if gProcess != sio.ONE_AI_CONNECTED:
				gProc.wait()
			else:
				#运行AI2
				AIProg.append(self.run_AI(connUI,gameAIPath[1]))
				gProc.release()
				break
			gProc.release()

		#所有连接建立后，将游戏进度前调
		while gProc.acquire():
			if gProcess != sio.CONNECTED:
				gProc.wait()
			else:
				gProcess = sio.MAP_SET
				gProc.notifyAll()
				gProc.release()
				break
			gProc.release()

		#AI返回heroType后将其传回界面
		while gProc.acquire():
			if gProcess != sio.HERO_TYPE_SET:
				gProc.wait()
			else:
				try:
					sio._sends(connUI,(mapInfo,base,aiInfo))
				except:
					connUI.shutdown(socket.SHUT_RDWR)
					exit(1)
				replayInfo.append((mapInfo,base,aiInfo))
				gProcess = sio.ROUND
				gProc.notifyAll()
				gProc.release()
				break
			gProc.release()
		
		#初始化完毕，进入回合==============================================================
		print 'ui in game'#for test
		flag = False
		#等待回合初始信息产生完毕
		while gProcess < sio.OVER:
			while rProc.acquire():
				print rProcess
				if rProcess != sio.RBINFO_SET:
					rProc.wait()
				else:
					#发送回合信息
					try:
						sio._sends(connUI,rbInfo)
					except:
						connUI.shutdown(socket.SHUT_RDWR)
						exit(1)
					print 'rbInfo sent to ui'
					rProcess = sio.RBINFO_SENT_TO_UI
					rProc.notifyAll()
					rProc.release()
					break
				rProc.release()
			
			#等待回合所有信息产生完毕
			while rProc.acquire():
				if rProcess != sio.REINFO_SET:
					rProc.wait()
				else:
					#发送回合信息
					try:	
						sio._sends(connUI,(rCommand,reInfo))
					except:
						connUI.shutdown(socket.SHUT_RDWR)
						exit(1)
					print 'reInfo sent to ui'#for test
					#回合信息存至回放列表中
					replayInfo.append([rbInfo,rCommand,reInfo])
					rProcess = sio.START
					rProc.notifyAll()
					#若游戏结束则跳出循环
					if reInfo.over:
						flag = True
					rProc.release()
					break
				rProc.release()
			if flag:
				break
		
		#向UI发送胜利方
		while gProc.acquire():
			if gProcess != sio.WINNER_SET:
				gProc.wait()
			else:
				try:
					sio._sends(connUI,winner)
				except:
					print 'winner sent failed!!!!!!'
					connUI.shutdown(socket.SHUT_RDWR)
					exit(1)
				connUI.settimeout(None)
				replay_mode = sio._recvs(connUI)
				gProc.notifyAll()
				gProc.release()
				break
			gProc.release()
		
		#存回放文件
		if replay_mode == True:	
			#检验回放文件目录
			try:
				os.mkdir(os.getcwd() + sio.REPLAY_FILE_PATH)
			except:
				pass
			#写入回放
			sio._WriteFile(replayInfo,os.getcwd() + sio.REPLAY_FILE_PATH + sio._ReplayFileName(aiInfo))
			
		connUI.shutdown(socket.SHUT_RDWR)
		
class Slogic(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = 'Thread-Logic'
	
	def run(self):
		global gProcess,rProcess,mapInfo,heroType,aiInfo,rbInfo,reInfo,rCommand,winner,base,aiConnErr,gameMode
		
		connLogic = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			connLogic.connect((sio.HOST,sio.LOGIC_PORT))
			print 'Logic connected'
		except:
			print 'logic connection failed, the program will exit...'
			time.sleep(2)
			exit(1)
			
		if gProc.acquire():
			gProcess += 1
			gProc.notifyAll()
			gProc.release()
			
		#发送游戏初始信息
		while gProc.acquire():
			if gProcess < sio.HERO_TYPE_SET:
				gProc.wait()
			else:
				for i in range(2):
					base[i][0].kind = heroType[i]
				sio._sends(connLogic,basic.Begin_Info(mapInfo,base,heroType))
				gProc.release()
				break
			gProc.release()	
		
		#等待其他线程初始化完毕
		while gProc.acquire():
			if gProcess != sio.ROUND:
				gProc.wait()
			else:
				gProc.release()
				break
			gProc.release()
		
		#初始化完毕，进入回合==============================================================	
		#print 'logic in game'#for test
		
		while gProcess != sio.OVER:
			#接收回合开始信息
			if gameMode != sio.AI_VS_AI:
				time.sleep(1)#time delay
			while rProc.acquire():
				if rProcess != sio.START:
					rProc.wait()
				else:
					rbInfo = sio._recvs(connLogic)
					print 'rbInfo received from logic'#for test
					rProcess = sio.RBINFO_SET
					rProc.notifyAll()
					rProc.release()
					break
				rProc.release()
				
			#将命令发送至AI
			while rProc.acquire():
				#print 'logic acquired',rProcess
				if rProcess != sio.RCOMMAND_SET:
					rProc.wait()
				else:	
					sio._sends(connLogic,rCommand)
					reInfo = sio._recvs(connLogic)
					if aiConnErr[rbInfo.id[0]]:
						reInfo.over = sio.AI_BREAKDOWN
					print 'reInfo received from logic'
					rProc.release()
					break
				rProc.release()

			#判断游戏是否结束，并调整游戏进度标记
			if reInfo.over != sio.CONTINUE:
				gProc.acquire()
				gProcess = sio.OVER
				gProc.notifyAll()
				gProc.release()

			#调整回合进度标记
			while rProc.acquire():
				rProcess = sio.REINFO_SET
				rProc.notifyAll()
				rProc.release()
				break	
		
		if reInfo.over == sio.NORMAL_OVER:
			winner = sio._recvs(connLogic)
		if reInfo.over == sio.AI_BREAKDOWN:
			for i in range(2):
				if aiConnErr[i] == True:
					winner = i
		print 'winner: ',winner
		
		#接收胜利方信息
		gProc.acquire()
		gProcess = sio.WINNER_SET
		gProc.notifyAll()
		gProc.release()
		
		connLogic.shutdown(socket.SHUT_RDWR)

class Sai(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = 'Thread-AI'
		self.connErr = False
	
	def run(self):
		global gProcess,rProcess,mapInfo,heroType,aiInfo,base, aiConnErr, gameAIPath
		global rbInfo,reInfo,rCommand
		global gameMode,timeoutSwitch
		
		#与AI进行socket连接
		[(connAI1,address1),(connAI2,address2)] = _SocketConnect(sio.HOST,sio.AI_PORT,'AI',2)
		connAI=[connAI1,connAI2]
		
		#设置命令限时
		print 'timeoutSwitch: ', timeoutSwitch
		for i in range(2):
			if timeoutSwitch[i]==1:
				connAI[i].settimeout(sio.AI_CMD_TIMEOUT)
			else:
				connAI[i].settimeout(None)

		#向AI传输游戏初始信息并接收AI的反馈
		while gProc.acquire():
			if gProcess != sio.MAP_SET:
				gProc.wait()
			else:
				for i in range(2):
					try:
						if sio.USE_CPP_AI and (gameAIPath[i] != None):
							sio._cpp_sends_begin(connAI[i],i,mapInfo,(len(base[0]),len(base[1])),base)
						else:
							sio._sends(connAI[i],(mapInfo,base))
					except sio.ConnException:
						aiConnErr[i] = True
					try:
						if sio.USE_CPP_AI and (gameAIPath[i] != None):
							aiInfoTemp,heroTypeTemp = sio._cpp_recvs_begin(connAI[i])
						else:
							aiInfoTemp,heroTypeTemp = sio._recvs(connAI[i])
						aiInfo.append(aiInfoTemp)
						heroType.append(heroTypeTemp)
					except socket.timeout:
						print 'fail to receive AI',i,'\'s information, default settings will be used...'
						aiInfo.append('Player'+str(i))
						heroType.append(6)
						
				for i in range(2):
					base[i][0].kind=heroType[i]
				#调节游戏进度标记
				gProcess = sio.HERO_TYPE_SET
				#print 'heroType set'#for test
				
				gProc.notifyAll()
				gProc.release()
				break
			gProc.release()

		#初始化完毕，进入回合==============================================================
		print 'ai in game'#for test 
		
		#游戏回合阶段
		roundNum = 0
		while gProcess < sio.OVER:
			roundNum =  roundNum + 1
			#将回合开始信息发送至AI，并接收AI的命令
			while rProc.acquire():
				if rProcess != sio.RBINFO_SENT_TO_UI:
					rProc.wait()
				else:
					#清空接收区缓存（其中可能有因超时而没收到的上一回合的命令）
					connAI[rbInfo.id[0]].settimeout(0)
				
					try:
						connAI[rbInfo.id[0]].recv(1024)
					except:
						pass
						
					if timeoutSwitch[rbInfo.id[0]]==1:
						connAI[rbInfo.id[0]].settimeout(sio.AI_CMD_TIMEOUT)
					else:
						connAI[rbInfo.id[0]].settimeout(None)
						
					#计分，用于传输
					if roundNum <= 2:
						tempScore = [0,0]
					else:
						tempScore = reInfo.score
					
					#发送回合信息
					try:
						if sio.USE_CPP_AI and gameAIPath[rbInfo.id[0]] != None:
							sio._cpp_sends(connAI[rbInfo.id[0]],rbInfo.id[1],len(rbInfo.temple),rbInfo.temple,(len(base[0]),len(base[1])),base,roundNum,tempScore)
						else:
							sio._sends(connAI[rbInfo.id[0]],rbInfo)
					except sio.ConnException:
						#AI连接错误，标记至connErr中
						aiConnErr[rbInfo.id[0]] = True
						
					print 'rbInfo sent to AI'
					if aiConnErr[rbInfo.id[0]] == True:
						rCommand = basic.Command()
					else:
						try:
							print 'prepare to receive cmd'
							if sio.USE_CPP_AI and gameAIPath[rbInfo.id[0]] != None:
								rCommand = sio._cpp_recvs(connAI[rbInfo.id[0]])
							else:
								rCommand = sio._recvs(connAI[rbInfo.id[0]])
							print 'AI',rbInfo.id[0],'\'s command:'
							sio.cmdDisplay(rCommand)
						except socket.timeout:
							print 'fail to receive cmd, default will be used..'
							rCommand = basic.Command()
						except sio.ConnException:
							print 'in aiConnErr!!!!!!!!!!!!'
							aiConnErr[rbInfo.id[0]] = True
							rCommand = basic.Command()

					rProcess = sio.RCOMMAND_SET
					rProc.notifyAll()
					rProc.release()
					break
				rProc.release()
			
			#调整回合进度标记
			while rProc.acquire():
				if rProcess == sio.RCOMMAND_SET:
					rProc.wait()
				else:
					rProc.release()
					break
				rProc.release()
			
		#向AI发送结束标志
		if reInfo.over == sio.NORMAL_OVER:
			for i in range(2):
				connAI[i].send('|')
				connAI[i].shutdown(socket.SHUT_RDWR)


global mapInfo,heroType,aiInfo,aiConnErr,gameAIPath
global rbInfo,reInfo,rCommand
global winner,gameMode,timeoutSwitch
global whole_map,base


aiInfo=[]
heroType=[]
reInfo=None
timeoutSwitch=[1,1]
aiConnErr = [False,False]

mapInfo = []
base = [[], []]

#设置进度标记
gProcess = sio.START
rProcess = sio.START
gProc=threading.Condition()
rProc=threading.Condition()

#运行线程		
ui_thread = Sui()
ai_thread = Sai()
logic_thread = Slogic()

ai_thread.daemon = True
logic_thread.daemon = True

ui_thread.start()
ui_thread.join()
#ai_thread.connAI[0].close()
#ai_thread.connAI[0].close()
#logic_thread.connLogic.close()

#time.sleep(10)
#raw_input('')
