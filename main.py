# -*- coding: UTF-8 -*-
import basic

def distance(i,j):
	return abs(i[0]-j[0])+abs(i[1]-j[1])

def available_spots(map_list, unit_list, source_num, move_target = (-1,-1)):
	'''该函数用于计算当前地图下某单位的活动范围。
	   传入参量map_list，为基本地图单元的二维数组
	   储存了地图的全部信息。unit_list同样记录了所有
	   单位的信息。source_num是一个元组，为(side_num, object_num)
	   如果指定move_target用于指定移动目的地后返回移动路线,为经过点的列表形式如[(0,0),(1,0),(1,1),(1,2)]'''
	s_unit = unit_list[source_num[0]][source_num[1]] # 目标单位
	s_position = s_unit.position # 源点坐标
	k = 1 - source_num[0]
	u_block = []; s_block = []
	for j in range(len(unit_list[k])):
		if unit_list[k][j].life > 0:
			if s_unit.kind == basic.DRAGON_RIDER:
				s_block += [unit_list[k][j].position]
			else:
				u_block += [unit_list[k][j].position]
	if s_unit.kind != basic.DRAGON_RIDER:
		for i in range(len(map_list)):
			for j in range(len(map_list[i])):
				if map_list[i][j].kind == basic.BARRIER:
					u_block += [(i, j)]
	#计算单位阻挡的位置
	for j in range(len(unit_list[1 - k])):
		if unit_list[1 - k][j].life > 0 and j != source_num[1]:
			s_block += [unit_list[1 - k][j].position]
	#计算己方单位占据而不能到达的位置
	d_spots = [s_position] # 所有已经确定可到的点
	a_spots = [[[s_position,1]]] # 所有点按到达顺序形成的二阶链表，元素为 点+该点已消耗的移动力
	direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]
	for i in range(1, s_unit.move_range):
		a = []
		for former_point in a_spots[i-1]:
			if former_point[1] >= map_list[former_point[0][0]][former_point[0][1]].move_consumption:
				for j in direction:
					i_1 = former_point[0][0] + j[0]
					i_2 = former_point[0][1] + j[1]
					if 0 <= i_1 < len(map_list) and 0<= i_2 < len(map_list[0]):
						latter_point = [(i_1, i_2), 1]
						if not (latter_point[0] in u_block or latter_point[0] in d_spots):
							if not latter_point[0] in s_block:
								d_spots += [latter_point[0]]
							a += [latter_point]
			else:
				a += [[(former_point[0][0], former_point[0][1]), former_point[1] + 1]]
		a_spots += [a]
	a_spots += [[]]
	if move_target in d_spots:
		d_spots = []
		i = len(a_spots) - 1
		while i > 1:
			i -= 1
			if [move_target, 1] in a_spots[i]:
				d_spots += [move_target]
				for j in direction:
					i_1 = move_target[0] + j[0]
					i_2 = move_target[1] + j[1]
					if (i_1, i_2) in  [k[0] for k in a_spots[i-1]]:
						move_target = (i_1, i_2)
						break
		d_spots.reverse()
	return d_spots	
def perparation(whole_map, base, score, map_temple):
	'''每回合前准备阶段'''
	for i in map_temple:
		m = whole_map[i[0][0]][i[0][1]]
		if m.time >= basic.TEMPLE_UP_TIME:
			i[1] = m.up #有神符存在
		else:
			whole_map[i[0][0]][i[0][1]].time += 1
		#神庙计时器+1
	for i in [0,1]:
		for j in range(0, len(base[i])):
			p = base[i][j].position
			if whole_map[p[0]][p[1]].kind == basic.TURRET:
				whole_map[p[0]][p[1]].time += 1
				if whole_map[p[0]][p[1]].time == basic.TURRET_SCORE_TIME:
					score[i] += whole_map[p[0]][p[1]].score
			#连续占有多回合炮塔积分
			if base[i][j].time > 0:
				base[i][j].time += 1
				if base[i][j].time == basic.HERO_3_UP_TIME:
					base[i][j].time = 0
					base[i][j].defence -= 1
					base[i][j].strength -= 1
			#英雄3技能持续时间判断
def calculation(command, base, whole_map, move_range, map_temple, score, unit_id):
	'''将传入指令计算后传出'''
	move_position = command.move
	order = command.order
	w = command.target
	i = unit_id[1]; j = unit_id[0]
	attack_1 = -1; attack_2 = -1
	route = [base[j][i].position]
	#added by ning
	trans = False
	if move_position in move_range:
		sc = whole_map[base[j][i].position[0]][base[j][i].position[1]].kind == basic.TURRET and base[j][i].position == move_position
		route += available_spots(whole_map, base, unit_id, move_position)
		if not sc:
			print "))))))",base[j][i].attack_range,base[j][i].position
			print whole_map[base[j][i].position[0]][base[j][i].position[1]].__class__.__name__
			whole_map[base[j][i].position[0]][base[j][i].position[1]].leave(base, (j, i))		
			base[j][i].move(move_position)
			print "))))))",base[j][i].attack_range
		if whole_map[move_position[0]][move_position[1]].kind == basic.MIRROR:
                        order = 0
		if not sc:
			#added by ning
			if isinstance(whole_map[move_position[0]][move_position[1]], basic.Map_Mirror):
				trans = whole_map[move_position[0]][move_position[1]].effect(base, whole_map, (j, i), score)
			else:
				whole_map[move_position[0]][move_position[1]].effect(base, whole_map, (j, i), score)
		for tp in map_temple:
			if tp[0] == move_position:
				tp[1] = 0
		if order != 0 and w[1] >= len(base[w[0]]):
			order == 0
		if order == 1 and w[0] == 1 - j:
			if base[j][i].attack_range[0] <= distance(base[j][i].position, base[1 - j][w[1]].position) <= base[j][i].attack_range[1] and base[1 - j][w[1]].life > 0:
				attack_1 = base[j][i].attack(base, (1 - j, w[1]))
			if attack_1!=-1 and base[1 - j][w[1]].life > 0 and base[1 - j][w[1]].attack_range[0] <= distance(base[j][i].position, base[1 - j][w[1]].position) <= base[1 - j][w[1]].attack_range[1]:
				attack_2 = base[1 - j][w[1]].attack(base, (j, i),0.5)
			#攻击及反击
		elif order == 2 and w[0] == j:
			if distance(base[j][i].position, base[j][w[1]].position) == 1:
				base[j][i].skill(base, (j,w[1]))
				#使用技能

	for i in [0,1]:
		over = True
		for j in base[i]:
			if j.life > 0:
				over = False
		if over:
			break   
	return basic.Round_End_Info(base, route, (attack_1, attack_2), trans, score, over)
	
def end_score(score, base, turn):
	'''结束后计算积分返回胜队，（-1表示平局）'''
	if turn >= basic.TURN_MAX:
		for i in [0,1]:
			for j in range(0, len(base[i])):
				if base[i][j].life > 0:
					if base[i][j].kind < 6:
						score[i] += base[i][j].life * basic.BASE_SCORE
					else:
						score[i] += base[i][j].life * basic.HERO_SCORE
		if score[1] != score[0]:
			return int(score[1] > score[0])
		else:
			return -1
	for i in [0,1]:
		over = True
		for j in base[i]:
			if j.life > 0:
				over = False
		if over:
			return 1-i  
