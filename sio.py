# -*- coding: UTF-8 -*-

import cPickle,basic,time

#游戏运行参数
DEBUG_MODE = 1 # 为0时,启动游戏只需运行sserver.py即可,程序将自动调用ui及logic文件;为1时先手动运行logic,再运行sserver,再运行ui
REPLAY_MODE = 0 #此常量为1时会生成回放文件
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
UI_FILE_NAME = '\\ai_debugger.py' # UI程序文件名,若有变化请修改此常量!
LOGIC_FILE_NAME = '\\sclientlogic.py' # logic 程序文件名,若有变化请修改此常量!

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
RCOMMAND_SET = 2
REINFO_SET = 3


class MapInfo:
	def __init__(self,whole_map):
		self.mapInfo = whole_map

#将对象以字符串形式通过指定连接发送
def _sends(conn,data):
	conn.send(cPickle.dumps(data))
	conn.send('|')

#接收字符串并将其转换为对象返回，空则返回'#'
def _recvs(conn):
	result = ''
	c = conn.recv(1)
	while c != '|':
		result = result + c
		c = conn.recv(1)
	if result == '':
		return '|'
	else:
		return cPickle.loads(result)

#从文件读取地图信息
def _ReadFile(filePath):
	with open(filePath,'r') as read:
		result = cPickle.load(read)
	return result

#将地图信息写入文件
def _WriteFile(fileInfo,filePath):
	with open(filePath,'w') as save:
		cPickle.dump(fileInfo,save)
	
def _ReplayFileName(aiInfo):
	result = ''
	result += aiInfo[0] + '_vs_' + aiInfo[1] + '_'
	result += time.strftime('%Y%m%d-%H-%M-%S')
	result += '.rep'
	return result
	
def _DefaultCommand(rbInfo):
	return basic.Command((1,2),'attack',3)
	
#此函数为调试用
def construct_base(map,hero_type):
	return [[1,2,3,4],[8,7,6,5]]
