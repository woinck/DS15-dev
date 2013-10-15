import basic,sio

map,base = sio._ReadFile("C:\Users\woinck\Documents\GitHub\DS15-dev\Maps\\4.map")

for i in base:
	for j in i:
		print j.__dict__
