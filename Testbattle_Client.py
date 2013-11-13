# -*- coding: utf8 -*-
import socket, hashlib, sio, os, time

HOST, PORT = '59.66.141.37', 8086



# Create a socket (SOCK_STREAM means a TCP socket)		
sock = None
testScore = None
gameAiPath = ""

class ConnectionError(Exception):
	def __init__(self):
		super(ConnectionError, self).__init__()

def OpenSocket():
	# Connect to server and send data
	global sock
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((HOST, PORT))
		return True
	except:
		# Do sth here
		print 'connection error!'
		return False


def ConnectWithWebsite(userName, password):
	global sock
	global testScore
	global gameAiPath
	try:
		#Get salt
		sock.sendall(userName)
		salt = sock.recv(128)
		
		# Get hashed password
		sha2 = hashlib.sha256()
		sha2.update(password + 'TeamStyle15' + salt)
		sock.sendall(sha2.hexdigest())
	
		received = sock.recv(128)

		if received == '0':
			print 'Wrong password or connection fail!'#for test
			# DO SOMETHING HERE! ###########################界面组修改#########################
			return (False, None)

		else:
			print 'succeed!'#for test
			sock.sendall('ok')
			testScoreTemp = sock.recv(1024).split() # get score
			testScore = []
			for i in range(10):
				testScore.append(testScoreTemp[(i + 1) % 10])
			return (True, testScore)
	except:
	# do sth here
		print 'err'#for test
		return (False, None)


def ConnectWithLogic(lv, aiPath):
	global sock
	global testScore
	global gameAiPath
	for i in range(10):
		print 'stage %d: ' % (i), testScore[i]
			


	# select stage
	# stage = raw_input('stage(enter 0 to quit): ')###########################界面组修改#########################
	# if stage == '0':
	#	exit()

	# choose ai file path here ###########################界面组修改#########################
	gameAIPath = aiPath

	# run game here
	serverProg = sio.Prog_Run(os.getcwd() + sio.SERV_FILE_NAME)
	conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		time.sleep(0.2)
		conn.connect((sio.HOST,sio.UI_PORT))
	except:
		conn.close()
		print 'fail to connect with platform'
		raise ConnectionError()

	sio._sends(conn, (sio.TEST_BATTLE, lv,(None,unicode(gameAIPath)),[0,0]))
	sio._sends(conn, lv)

	# receive score
	#score = raw_input('score: ')
			
	score = sio._recvs(conn)
	winner = sio._recvs(conn)
	
	if winner == 0:
		score = 0
		print 'You lose'

	newScore = [str(lv%10),str(score)]
	newScore = ' '.join(newScore)

	sock.sendall(newScore)
	return winner, score


def CloseSocket():
	global sock
	sock.shutdown(socket.SHUT_RDWR)

if __name__=="__main__":
	OpenSocket()
	username = raw_input("name: ")
	password = raw_input("password: ")
	ConnectWithWebsite(username, password)
	CloseSocket()

