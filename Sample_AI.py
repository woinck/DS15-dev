import basic, socket, time, sio
import main
ATTACK_RATE = 75
DANGER_HP = 7
def GetHeroType(mapInfo,base):
		s = 0; t = 0
		for i in mapInfo:
				for j in i:
						if j.kind == 2 or j.kind == 1:
								s += 1
						if j.kind == 3:
								t += 1
		if t >= 1.0 / 3 * len(mapInfo) * len(mapInfo[0]):
				return basic.HERO_3
		elif s >= 1.0 / 3 * len(mapInfo) * len(mapInfo[0]):
				return basic.HERO_2
		else:
				return basic.HERO_1
def attack_id(whole_map, base, unit_id, move_area):
	team = unit_id[0]
	self = base[team][unit_id[1]]
	result = []
	for position in move_area:
		for j in range(0,len(base[1-team])):
			target = base[1-team][j]
			if (not j in result) and target.life > 0 and (self.attack_range[0]<=main.distance(target.position,position)<=self.attack_range[1]):
				result += [j]
	if self.kind == basic.ARCHER:
		for i in move_area:
			if whole_map[i[0]][i[1]].kind == basic.TURRET:
				for j in range(0,len(base[1-team])):
					if basic.TURRET_RANGE[0]<=main.distance(base[1-team][j].position, i)<=basic.TURRET_RANGE[1]:
						result += [j]
	return result
def skill_id(whole_map, base, unit_id, move_area):
	team = unit_id[0]
	self = base[team][unit_id[1]]
	result = []
	for position in move_area:
		for j in range(0,len(base[1-team])):
			target = base[1-team][j]
			if target.life > 0 and main.distance(target.position,position) == 1:
				result += [j]
	return result
def find_position(whole_map, base, unit_id, target_id, distance, move):
	target_position = base[target_id[0]][target_id[1]].position
	for i in move:
		if whole_map[i[0]][i[1]].kind == basic.TURRET and base[unit_id[0]][unit_id[1]].kind == basic.ARCHER:
			if basic.TURRET_RANGE[0]<=main.distance(i,target_position)<=basic.TURRET_RANGE[1]:
				return i
		if main.distance(i, target_position) in distance:
			return i
	return (-1,-1)
def AI(whole_map, Info):
	team=Info.id[0]
	unit=Info.id[1]
	self=Info.base[team][unit]
	move=Info.range
	target_id=-1; kill = []; distance = self.attack_range
	most_damage = 0; order = 1
	attack_list = attack_id(whole_map, Info.base, Info.id, move)
	if self.kind == basic.WIZARD or (self.kind == basic.HERO_1 and self.life > DANGER_HP):
		for i in skill_id(whole_map, Info.base, Info.id, move):
			target = Info.base[1-team][i]
			if target.life < DANGER_HP:
				distance = [1]; attack_list = []
				target_id = i; order = 2
				break
	for i in attack_list:
		target = Info.base[1-team][i]
		damage = int((self.strength - target.defence) * basic.ATTACK_EFFECT[self.kind][target.kind])
		if target.life - damage <= 0:
			kill += [i]
		if most_damage < damage and (int((target.strength - self.defence) * basic.ATTACK_EFFECT[target.kind][self.kind])<self.life or target.attack_range != self.attack_range):
			most_damage = damage
			target_id = i
	kill_life = 0
	for i in kill:
		target = Info.base[1-team][i]
		if target.life > kill_life:
			target_id = i
			kill_life = target.life 
	if target_id==-1:
		if self.kind == basic.HERO_3:
			for i in skill_id(whole_map, Info.base, Info.id, move):
				return basic.Command(2,find_position(whole_map, Info.base,Info.id,(team,i),[1],move),(team, i))
		positon = self.position
		if self.life < DANGER_HP:
			for j in move:
				under_attack = False
				for i in range(0,len(Info.base[1-team])):
					target = Info.base[1-team][i]
					if target.life > 0 and target.kind != basic.WIZARD:
						target.move_range += target.attack_range[-1]
						if j in main.available_spots(whole_map, Info.base, (1-team,i)):
							under_attack = True
							target.move_range -= target.attack_range[-1]
							break
						target.move_range -= target.attack_range[-1]
					if not under_attack:
						position = j; break
		else:
			distance = basic.COORDINATE_X_MAX * 2
			for i in move:
				for j in range(0,len(Info.base[1-team])):
					target = Info.base[1-team][j]
					if main.distance(i,target.position) < distance:
						distance = main.distance(i,target.position)
						position = i
			result = basic.Command(0,position,(0,0))
	else:
		if order == 1:
			team = 1 - team
		result = basic.Command(order,find_position(whole_map, Info.base,Info.id,(team,target_id), distance, move),(team, target_id))
	return result
aiInfo = 'Sample_AI'
conn=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
	conn.connect((sio.HOST,sio.AI_PORT))
	print 'connected!'
except:
	print 'failed to connect, the program will exit...'
	time.sleep(2)
	exit(1)
mapInfo,base=sio._recvs(conn)
sio._sends(conn,(aiInfo,GetHeroType(mapInfo,base)))
print 'info sent'
while True:
	rBeginInfo=sio._recvs(conn)
	print 'rbInfo got'
	if rBeginInfo != '|':
		sio._sends(conn,AI(mapInfo,rBeginInfo))
		print 'cmd sent\n\n'
	else:
		break

conn.close()
print ('ai end')