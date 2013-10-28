import hashlib, sqlite3, SocketServer

DATABASE_NAME = 'development.sqlite3'



class MyTCPHandler(SocketServer.BaseRequestHandler):

	def handle(self):
		
		self.conn = sqlite3.connect(DATABASE_NAME)
		self.c = self.conn.cursor()

		self.userName = self.request.recv(128)

		#Send salt to client
		self.request.sendall(self.GetSalt())
		#Receive password from client
		
		userPassword = self.request.recv(128)

		#Check if the user's info is correct
		if not self.Check(userPassword):
			self.request.sendall('0')
			return

		self.request.sendall('1')
		self.request.recv(128)
		
		while True:
			# Get test battle score from database
			testScore = self.GetScore()
			testScore = ' '.join(testScore)
			self.request.sendall(testScore)

			newScore = self.request.recv(128).split()
			self.AddScore(newScore)



	def GetSalt(self):

		self.c.execute('select salt from users where name = \'%s\'' % (self.userName))
		result = self.c.fetchall()
		
		if len(result) == 0:
			return 'Dugy'
		return result[0][0]

	def Check(self,userPassword):

		self.c.execute('select hashed_password from users where name = \'%s\'' % (self.userName))
		result = self.c.fetchall()
		
		if len(result) == 0:
			return False
		return userPassword == result[0][0]

	def GetScore(self):
		
		result = []
		for i in range(10):
			self.c.execute('select test%s from users where name = \'%s\'' % (str(i),self.userName))
			result.append(self.c.fetchall()[0][0])
			if result[-1] == None:
				result[-1] = 0
		return map(str,result)

	def AddScore(self,newScore):
		self.c.execute('select test%s from users where name = \'%s\'' % (str(newScore[0]),self.userName))
		curScore = self.c.fetchall()[0][0]
		if curScore == None:
			curScore = 0
		if int(newScore[1]) > int(curScore):
			self.c.execute('update users set test%s = %s where name = \'%s\'' % (str(newScore[0]),str(newScore[1]),self.userName))
			self.conn.commit()



if __name__ == "__main__":
	HOST, PORT = "127.0.0.1", 8086

	# Create the server
	server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
	server.serve_forever()
