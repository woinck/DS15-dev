 #-*- coding:UTF-8 -*-
import cPickle, basic, threading, os, time, subprocess, socket, sys


RELEASE_MODE = 1



reload(sys)
sys.setdefaultencoding('gbk')
#os.system("chcp 936")

#重定向
if RELEASE_MODE == 1:
	logF = open('log.log','w')
	sys.stdout = logF

#AI模式 0：py 1：cpp
USE_CPP_AI = 1

#兵种选择模式 0：固定兵种 1：自由选择兵种
FREE_CHOOSE = 0

#游戏运行参数
DEBUG_MODE = 0
SINGLE_PROCESS = 1 #此常量为1时各命令窗口合并，只会产生一个线程，为0时分开（便于调试）

AI_CMD_TIMEOUT = 1 # AI命令最长等待时间，超过则不再接收
AI_CONNECT_TIMEOUT = 3 # 与AI程序进行对接时的最长等待时间

#游戏模式
AI_VS_AI = 0
PLAYER_VS_AI = 1
PLAYER_VS_PLAYER = 2
TEST_BATTLE = 3
NET_GAME_SERVER = 4
NET_GAME_CLIENT = 5

#一些常量
HOST = '127.0.0.1' # 主机地址
LOGIC_PORT = 8801 # logic 连接端口
UI_PORT = 8802 # UI 连接端口
AI_PORT = 8803 # AI 连接端口

#error
#devnull = open(os.devnull, 'w')
if RELEASE_MODE:
	SERV_FILE_NAME = '\\sserver.exe'
	LOGIC_FILE_NAME = '\\sclientlogic.exe'
else:
	SERV_FILE_NAME = '\\sserver.py' 
	LOGIC_FILE_NAME = '\\sclientlogic.py' # logic 程序文件名,若有变化请修改此常量!

UI_FILE_NAME = '\\ai_debugger.py' # UI程序文件名,若有变化请修改此常量!
REPLAY_FILE_PATH = '\\ReplayFiles'
DISPLAY_FILE_PATH = '\\DisplayFiles'

#游戏/回合进程标记,对战流程用
START = 0
UI_CONNECTED = 1
LOGIC_CONNECTED = 2
ONE_AI_CONNECTED = 3
CONNECTED = 4
MAP_SET = 5
HERO_TYPE_SET = 6
ROUND = 7
OVER = 8
WINNER_SET = 9

RBINFO_SET = 1
RBINFO_SENT_TO_UI = 2
RCOMMAND_SET = 3
REINFO_SET = 4

#OVER的值
CONTINUE = 0
NORMAL_OVER = 1
AI_BREAKDOWN = 2



class MapInfo:
	def __init__(self,whole_map):
		self.mapInfo = whole_map

#向cpp客户端AI传输游戏初始信息
def _cpp_sends_begin(conn, team_number, whole_map, soldier_number, soldier):
		conn.send(str(team_number))
		conn.recv(3)
		mirror_number = 0
		mirror = []
		conn.send(str(len(whole_map)))
		conn.recv(3)
		conn.send(str(len(whole_map[0])))
		conn.recv(3)
		
		for i in range(len(whole_map)):
				for j in range(len(whole_map[0])):
						if whole_map[i][j].kind == basic.MIRROR:
							mirror_number = mirror_number + 1
							mirror.append(whole_map[i][j])
						conn.send(str(whole_map[i][j].kind))
						conn.recv(3)
		conn.send(str(mirror_number))
		conn.recv(3)

		for i in range(len(whole_map)):
				for j in range(len(whole_map[0])):
					if whole_map[i][j].kind == basic.MIRROR:
						conn.send(str(i)+' '+str(j)+' '+str(whole_map[i][j].out[0]) + ' '+str(whole_map[i][j].out[1]))
						conn.recv(3)
		if FREE_CHOOSE == 0:
			conn.send(str(soldier_number[0])+' '+str(soldier_number[1]))
			conn.recv(3)
			for i in range(soldier_number[0]):
					conn.send( str(soldier[0][i].kind)+' '+str(soldier[0][i].life)+' '
							   +str(soldier[0][i].strength)+' '
							   +str(soldier[0][i].defence)+' '
							   +str(soldier[0][i].move_range)+' '
							   +str(soldier[0][i].attack_range[0])+' '
							   +str(soldier[0][i].attack_range[1])+' '
							   +str(soldier[0][i].up)+' '
							   +str(soldier[0][i].position[0])+' '
							   +str(soldier[0][i].position[1]))
					conn.recv(3)
			for i in range(soldier_number[1]):
					conn.send( str(soldier[1][i].kind)+' '+str(soldier[1][i].life)+' '
							   +str(soldier[1][i].strength)+' '
							   +str(soldier[1][i].defence)+' '+str(soldier[1][i].move_range)+' '
							   +str(soldier[1][i].attack_range[0])+' '
							   +str(soldier[1][i].attack_range[1])+' '+str(soldier[1][i].up)+' '
							   +str(soldier[1][i].position[0])+' '+str(soldier[1][i].position[1]) )
					conn.recv(3)

#向cpp客户端传输兵种选择信息
def _cpp_sends_choose(conn, enemy_inc, choice, self_inc, id):
	conn.send(str(enemy_inc)+' '+str(choice[0])+' '+str(choice[1])
		+' '+str(self_inc)+' '+str(id[0])+' '+str(id[1]))


#向cpp客户端AI传输每回合信息
def _cpp_sends(conn, move_id, temple_number, temple, soldier_number, soldier, turn, score,):
		conn.send(str(move_id)+' '+str(temple_number)+' '+str(turn)+' '+str(score[0])+' '+str(score[1]))
		conn.recv(3)
		for i in range(temple_number):
				conn.send(str(temple[i][0][0])+' '+str(temple[i][0][1])+' '+str(temple[i][1]))
				conn.recv(3)
		for i in range(soldier_number[0]):
				conn.send( str(soldier[0][i].kind)+' '+str(soldier[0][i].life)+' '
						   +str(soldier[0][i].strength)+' '
						   +str(soldier[0][i].defence)+' '+str(soldier[0][i].move_range)+' '
						   +' '+str(soldier[0][i].attack_range[0])+' '
						   +str(soldier[0][i].attack_range[1])+' '+str(soldier[0][i].up)+' '
						   +str(soldier[0][i].position[0])+' '+str(soldier[0][i].position[1]) )
				conn.recv(3)
		for i in range(soldier_number[1]):
				conn.send( str(soldier[1][i].kind)+' '+str(soldier[1][i].life)+' '
						   +str(soldier[1][i].strength)+' '
						   +str(soldier[1][i].defence)+' '+str(soldier[1][i].move_range)+' '
						   +str(soldier[1][i].attack_range[0])+' '
						   +str(soldier[1][i].attack_range[1])+' '+str(soldier[1][i].up)+' '
						   +str(soldier[1][i].position[0])+' '+str(soldier[1][i].position[1]) )
				conn.recv(3)
		conn.send('ok')

#向展示文件写入初始信息
def _display_begin(whole_map, soldier, ai):
	result = str(len(whole_map)) + ' ' + str(len(whole_map[0])) +' '
	for i in whole_map:
		for j in i:
			result += str(j.kind) + ' '
	result += ai[0] + ' ' + ai[1] + ' '
	for j in range(2):
		result += str(len(soldier[j])) + ' '
		for i in range(len(soldier[j])):
			result += (str(soldier[j][i].kind)+' '
			  +str(soldier[j][i].life)+' '
			  +str(soldier[j][i].strength)+' '
			  +str(soldier[j][i].defence)+' '
			  +str(soldier[j][i].move_range)+' '
			  +str(soldier[j][i].attack_range[0])+' '
			  +str(soldier[j][i].attack_range[1])+' '
			  +str(soldier[j][i].up)+' '
			  +str(soldier[j][i].position[0])+' '
			  +str(soldier[j][i].position[1])+' '
									)
	return result				 

#向展示文件写入回合信息
def _display_round(rbinfo, comd, reinfo):
	result = str(rbinfo.id[0]) + ' ' + str(rbinfo.id[1]) + ' '
	result += str(len(rbinfo.range)) + ' '
	for i in range(len(rbinfo.range)):
		result += str(rbinfo.range[i][0]) + ' ' + str(rbinfo.range[i][1]) + ' '
	for j in range(2):
		for soldier in rbinfo.base[j]:
			result += (str(soldier.kind)+' '
					  +str(soldier.life)+' '
					  +str(soldier.strength)+' '
					  +str(soldier.defence)+' '
					  +str(soldier.move_range)+' '
					  +str(soldier.attack_range[0])+' '
					  +str(soldier.attack_range[1])+' '
					  +str(soldier.up)+' '
					  +str(soldier.position[0])+' '
					  +str(soldier.position[1])+' ')
	result += str(len(rbinfo.temple)) + ' '
	for tmp in rbinfo.temple:
		result += str(tmp[0][0]) + ' ' + str(tmp[0][1]) + ' ' + str(tmp[1]) + ' '
	result += str(comd.move[0]) + ' ' + str(comd.move[1]) + ' '
	result += str(comd.order) + ' '
	print comd.target
	result += str(comd.target[0]) + ' ' + str(comd.target[1]) + ' '
	for j in range(2):
		for soldier in reinfo.base[j]:
			result += (str(soldier.kind)+' '
					  +str(soldier.life)+' '
					  +str(soldier.strength)+' '
					  +str(soldier.defence)+' '
					  +str(soldier.move_range)+' '
					  +str(soldier.attack_range[0])+' '
					  +str(soldier.attack_range[1])+' '
					  +str(soldier.up)+' '
					  +str(soldier.position[0])+' '
					  +str(soldier.position[1])+' ')
	result += str(len(reinfo.route)) + ' '
	for p in reinfo.route:
		result += str(p[0]) + ' ' + str(p[1]) + ' '
	result += str(reinfo.score[0]) + ' ' + str(reinfo.score[1]) + ' '
	result += str(reinfo.effect[0]) + ' ' + str(reinfo.effect[1]) + ' '
	result += str(int(reinfo.trans)) + ' ' + str(int(reinfo.over)) + ' '
	return result

#从cpp客户端AI接收初始信息
def _cpp_recvs_begin(conn):
	result = []
	recvbuf = conn.recv(40)
	recvbuf = recvbuf.split(chr(0))[0]
	conn.send('ok')
	result.append(recvbuf)
	recvbuf = conn.recv(10)
	result.append(int(recvbuf))
	return result
	
#从cpp客户端AI接收兵种选择信息
def _cpp_recvs_choose(conn, self_inc, soldier, team_number, id):
	for i in range(self_inc):
		temp = basic.Base_Unit(int(conn.recv(1)), soldier[team_number][id[i]].position)
		soldier[team_number][id[i]] = temp


#从cpp客户端AI接收每回合指令
def _cpp_recvs(conn):
	recvbuf = conn.recv(10)
	for i in recvbuf:
		if not (i in range(10)):
			recvbuf = recvbuf.replace(i, '')
	rbuf = recvbuf.split()
	try:
		order = int(rbuf[0])
		target_id = int(rbuf[1])
		move = (int(rbuf[2]), int(rbuf[3]))
	except IndexError:
		order = None
		target_id = None
		move = None
	return basic.Command(order,move,target_id)


#连接异常
class ConnException(Exception):
	def __init__(self):
		Exception.__init__(self)
		
		
#将对象以字符串形式通过指定连接发送
def _sends(conn,data):
	if conn == None:
		return
	#try:
	conn.send(cPickle.dumps(data))
	conn.send('|')
#   except:	 raise ConnException()

#接收字符串并将其转换为对象返回，空则返回'|'
def _recvs(conn):
	if conn == None:
		return
	result = ''
	
	try:
		c = conn.recv(1)
	except socket.timeout:
		raise socket.timeout
	#except:
	#	raise ConnException()
		
	while c != '|':
		result = result + c
		try:
			c = conn.recv(1)
		except socket.timeout:
			raise socket.timeout
		except:
			raise ConnException()
	if result == '':
		return '|'
	else:
		return cPickle.loads(result)


#从文件读取回放信息
def _ReadFile(filePath):
	with open(filePath,'r') as read:
		result = cPickle.load(read)
	return result

#将地图信息写入文件
def _WriteFile(fileInfo,filePath):
	print filePath
	with open(filePath,'w') as save:
		cPickle.dump(fileInfo,save)

def _WriteCppFile(fileInfo, filePath):
	print filePath
	display_file = open(filePath, 'w') 
	display_file.write(fileInfo)


def _ReplayFileName(aiInfo,isThreeD = 0):
	result = '\\'
	result += aiInfo[0] + '_vs_' + aiInfo[1] + '_'
	result += time.strftime(u'%Y%m%d-%H-%M-%S')
	result += '.rep'
	if isThreeD != 0:
		result += '3d'
	return result

def cmdDisplay(cmd):
	print 'move:',cmd.move
	print 'order:',cmd.order
	print 'target:',cmd.target

def Prog_Run(progPath,isAI=False):  
	global SINGLE_PROCESS
	if SINGLE_PROCESS:
		progPath=progPath.encode('gbk')
		if RELEASE_MODE or (isAI and USE_CPP_AI):   
			#result = subprocess.Popen(progPath, stderr = devnull)
			result = subprocess.Popen(progPath)
		else: 
			result = subprocess.Popen('python ' + progPath)
	else:
		os.system('cmd /c start %s' %unicode(progPath))
		result = None
	return result
		
