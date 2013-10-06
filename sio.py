 #-*- coding:UTF-8 -*-

import cPickle, basic, threading, os, time, subprocess, socket, sys
reload(sys)
sys.setdefaultencoding('gb2312')

#AI模式 0：py 1：cpp
USE_CPP_AI = 0
#游戏运行参数
DEBUG_MODE = 0
'''
关于DEGUB_MODE:
为0时,启动游戏只需运行相应UI即可,程序将自动调用sserver及logic文件;
为1时需先手动运行logic,再运行sserver,再运行ui
'''
RELEASE_MODE = 0
SINGLE_PROCESS = 1 #此常量为1时各命令窗口合并，只会产生一个线程，为0时分开（便于调试）
REPLAY_MODE = 0 #此常量为1时会生成回放文件,######废弃######
AI_CMD_TIMEOUT = 1 # AI命令最长等待时间，超过则不再接收
AI_CONNECT_TIMEOUT = 3 # 与AI程序进行对接时的最长等待时间

#游戏模式,界面组请关注!
AI_VS_AI = 0
PLAYER_VS_AI = 1
PLAYER_VS_PLAYER = 2

#一些常量
HOST = '127.0.0.1' # 主机地址
LOGIC_PORT = 8801 # logic 连接端口
UI_PORT = 8802 # UI 连接端口
AI_PORT = 8803 # AI 连接端口
#error
devnull = open(os.devnull, 'w')
if RELEASE_MODE:
	SERV_FILE_NAME = '\\sserver.exe'
	LOGIC_FILE_NAME = '\\sclientlogic.exe'
else:
	SERV_FILE_NAME = '\\sserver.py'	
	LOGIC_FILE_NAME = '\\sclientlogic.py' # logic 程序文件名,若有变化请修改此常量!

UI_FILE_NAME = '\\ai_debugger.py' # UI程序文件名,若有变化请修改此常量!
REPLAY_FILE_PATH = '\\ReplayFiles'

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
def _cpp_sends_begin(conn, team_number, whole_map, mirror_number, mirror, soldier_number, soldier):
        conn.send(str(team_number))
        conn.recv(3)
        for i in range(COORDINATE_X_MAX):
                for j in range(COORDINATE_Y_MAX):
                        conn.send(str(whole_map[i][j]))
                        conn.recv(3)
        conn.send(str(mirror_number))
        conn.recv(3)
        for i in range(mirror_number):
                conn.send(str(mirror[i][0][0])+' '+str(mirror[i][0][1])+' '+str(mirror[i][1][0])+' '+str(mirror[i][1][1]))
                conn.recv(3)
        conn.send(str(soldier_number[0])+' '+str(solder_number[1]))
        conn.recv(3)
        for i in range(soldier_number):
                conn.send( str(soldier[i][0].kind)+' '+str(soldier[i][0].life)+' '
                           +str(soldier[i][0].attack)+' '+str(soldier[i][0].agility)+' '
                           +str(soldier[i][0].defence)+' '+str(soldier[i][0].move_range)+' '
                           +str(soldier[i][0].move_speed)+' '+str(soldier[i][0].attack_range[0])+' '
                           +str(soldier[i][0].attack_range[1])+' '+str(soldier[i][0].up)+' '
                           +str(soldier[i][0].p[0])+' '+str(soldier[i][0].p[1]) )
                conn.recv(3)
        for i in range(soldier_number):
                conn.send( str(soldier[i][1].kind)+' '+str(soldier[i][1].life)+' '
                           +str(soldier[i][1].attack)+' '+str(soldier[i][1].agility)+' '
                           +str(soldier[i][1].defence)+' '+str(soldier[i][1].move_range)+' '
                           +str(soldier[i][1].move_speed)+' '+str(soldier[i][1].attack_range[0])+' '
                           +str(soldier[i][1].attack_range[1])+' '+str(soldier[i][1].up)+' '
                           +str(soldier[i][1].p[0])+' '+str(soldier[i][1].p[1]) )
                conn.recv(3)
#向cpp客户端AI传输每回合信息
def _cpp_sends(conn, move_id, temple_number, temple, turn, score):
        conn.send(str(move_id)+' '+str(temple_number)+' '+str(turn)+' '+str(score[0])+' '+str(score[1]))
        conn.recv(3)
        for i in range(temple_number):
                conn.send(str(temple[i].pos[0])+' '+str(temple[i].pos[1])+' '+str(temple[i].state))
                conn.recv(3)
        for i in range(soldier_number):
                conn.send( str(soldier[i][0].kind)+' '+str(soldier[i][0].life)+' '
                           +str(soldier[i][0].attack)+' '+str(soldier[i][0].agility)+' '
                           +str(soldier[i][0].defence)+' '+str(soldier[i][0].move_range)+' '
                           +str(soldier[i][0].move_speed)+' '+str(soldier[i][0].attack_range[0])+' '
                           +str(soldier[i][0].attack_range[1])+' '+str(soldier[i][0].up)+' '
                           +str(soldier[i][0].p[0])+' '+str(soldier[i][0].p[1]) )
                conn.recv(3)
        for i in range(soldier_number):
                conn.send( str(soldier[i][1].kind)+' '+str(soldier[i][1].life)+' '
                           +str(soldier[i][1].attack)+' '+str(soldier[i][1].agility)+' '
                           +str(soldier[i][1].defence)+' '+str(soldier[i][1].move_range)+' '
                           +str(soldier[i][1].move_speed)+' '+str(soldier[i][1].attack_range[0])+' '
                           +str(soldier[i][1].attack_range[1])+' '+str(soldier[i][1].up)+' '
                           +str(soldier[i][1].p[0])+' '+str(soldier[i][1].p[1]) )
                conn.recv(3)       
#从cpp客户端AI接收每回合指令
def _cpp_recvs(conn, cmd):
        recvbuf = conn.recv(10)
        rbuf = recvbuf.split()
        cmd.order = int(rbuf[0])
        cmd.target_id = int(rbuf[1])
        cmd.move = (int(rbuf[2]), int(rbuf[3]))

		
class ConnException(Exception):
	def __init__(self):
		Exception.__init__(self)
		
		
#将对象以字符串形式通过指定连接发送
def _sends(conn,data):
	try:
		conn.send(cPickle.dumps(data))
		conn.send('|')
	except:
		raise ConnException()

#接收字符串并将其转换为对象返回，空则返回'|'
def _recvs(conn):
	result = ''
	
	try:
		c = conn.recv(1)
	except socket.timeout:
		raise socket.timeout
	except:
		raise ConnException()
		
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
	with open(filePath,'w') as save:
		cPickle.dump(fileInfo,save)
	
def _ReplayFileName(aiInfo):
	result = '\\'
	result += aiInfo[0] + '_vs_' + aiInfo[1] + '_'
	result += time.strftime('%Y%m%d-%H-%M-%S')
	result += '.rep'
	return result

def cmdDisplay(cmd):
	print 'move:',cmd.move
	print 'order:',cmd.order
	print 'target:',cmd.target
'''
class Prog_Run(progPath):	
	def 
	def run(self):
		os.system('cmd /c start %s' %(self.progPath))
		#subprocess.Popen('python ' + progPath,shell = True)
'''
def Prog_Run(progPath):	
	global SINGLE_PROCESS
	if SINGLE_PROCESS:
		progPath=progPath.encode('gbk')
		print progPath
		if RELEASE_MODE:	
			result = subprocess.Popen(progPath, stderr = devnull)
		else: 
			result = subprocess.Popen('python ' + progPath)
	else:
		os.system('cmd /c start %s' %unicode(progPath))
		result = None
	return result
		