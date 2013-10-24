import socket, hashlib
import sys, time

HOST, PORT = '127.0.0.1', 10086


try:
	# Create a socket (SOCK_STREAM means a TCP socket)		
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Connect to server and send data
	sock.connect((HOST, PORT))

	userName = raw_input('Username: ')
	password = raw_input('Password: ')
	
	#Get salt
	sock.sendall(userName)
	salt = sock.recv(128)
	
	# Get hashed password
	sha2 = hashlib.sha256()
	sha2.update(userName + password + salt)
	sock.sendall(sha2.hexdigest())
	
	received = sock.recv(128)

	if received == '0':
		print 'fail!'

		# DO SOMETHING HERE!
		exit()

	else:
		print 'succeed!'
		sock.sendall('ok')

		while True:
			testScore = sock.recv(1024).split()
			for i in range(10):
				print 'stage %d: ' % (i), testScore[i]
			
			# receive stage & score from logic
			stage = raw_input('stage(enter 0 to quit): ')
			if stage == '0':
				exit()
			score = raw_input('score: ')
			
			newScore = [str(stage),str(score)]
			newScore = ' '.join(newScore)
			sock.sendall(newScore)

finally:
	sock.shutdown(socket.SHUT_RDWR)
