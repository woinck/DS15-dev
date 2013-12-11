import basic,sio

replayInfo = sio._ReadFile("C:\Users\woinck\Desktop\Sample_vs_Sample_20131211-22-56-04.rep")

for i in range(30):
	flag = False
	try:
		print 'i:',i
		print 'move:',replayInfo[i][1].move
		print 'order:',replayInfo[i][1].order
		print 'target:',replayInfo[i][1].target
		print '========================='
	except:
		pass
	
raw_input()