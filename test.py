import basic,sio

map,base = sio._ReadFile('C:\Users\woinck\Documents\GitHub\DS15-dev\\testmap2.map')

for i in map:
	for j in i:
		print j.kind,j.move_consumption