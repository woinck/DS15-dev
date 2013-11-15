import basic, socket, time, sio
import main
DANGER_HP = 10
def attack_id(whole_map, base, unit_id, move_area):
    team = unit_id[0]
    self = base[team][unit_id[1]]
    result = []
    for position in move_area:
        for j in range(0,len(base[1-team])):
            target = base[1-team][j]
            if self.kind != basic.WIZARD:
                damage = (self.strength - target.defence) * basic.ATTACK_EFFECT[self.kind][target.kind]
            else:
                damage = 0
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

def find_person(base, position):
    for i in range(2):
        for j in range(len(base[i])):
            if base[i][j].position == position and base[i][j].life > 0:
                return (i,j)
    return (-1,-1)

def GetHeroType_1(mapInfo,base):
    return basic.HERO_1
def AI_1(whole_map, Info):
    team=Info.id[0]
    unit=Info.id[1]
    self=Info.base[team][unit]
    return basic.Command(0, self.position, (0,0))

def GetHeroType_2(mapInfo,base):
    return basic.HERO_2
def AI_2(whole_map, Info):
    team=Info.id[0]
    unit=Info.id[1]
    self=Info.base[team][unit]
    move=Info.range
    base=Info.base
    order = 0
    for i in range(0, len(base[1 - team])):
        if main.distance(base[1 - team][i].position, self.position) == 1:
            order = 1
            break
    result = basic.Command(order,self.position,(1-team,i))
    return result

def GetHeroType_3(mapInfo,base):
    return basic.HERO_3
def AI_3(whole_map, Info):
    team=Info.id[0]
    unit=Info.id[1]
    self=Info.base[team][unit]
    return basic.Command(0, self.position, (0,0))

def GetHeroType_4(mapInfo,base):
    return basic.HERO_1
def AI_4(whole_map, Info):
    team=Info.id[0]
    unit=Info.id[1]
    self=Info.base[team][unit]
    base=Info.base
    if self.kind == basic.WIZARD or self.kind == basic.HERO_1:
        for i in range(0, len(base[team])):
            if main.distance(base[team][i].position, self.position) == 1 and base[team][i].life < basic.ABILITY[base[team][i].kind][0]:
                return basic.Command(2, self.position,(team, i))
    for i in range(0, len(base[1-team])):
        d = main.distance(base[1-team][i].position,self.position)
        if d <= self.attack_range[1] and d >= self.attack_range[0]:
            return basic.Command(1, self.position, (1-team,i))
    return basic.Command(0, self.position, (0,0))

def GetHeroType_5(mapInfo,base):
    return basic.HERO_3
def AI_5(whole_map,Info):
    team=Info.id[0]
    unit=Info.id[1]
    self=Info.base[team][unit]
    move=Info.range
    if (9,2) in move:
        return basic.Command(0, (9, 2), (0, 0))
    if self.kind == basic.ARCHER:
        t = find_person(Info.base, (8,14))
        if t != (-1,-1):
            d = attack_id(whole_map, Info.base, (team,unit), move)
            t = 0
            for i in d:
                if Info.base[1-team][i].life > 0 and m < (self.strength - Info.base[1-team][i].defence) * basic.ATTACK_EFFECT[self.kind][Info.base[1-team][i].kind]:
                    m = (self.strength - Info.base[1-team][i].defence) * basic.ATTACK_EFFECT[self.kind][Info.base[1-team][i].kind]
                    t = i
            return basic.Command(1,find_position(whole_map, Info.base, (team, unit),(1-team,t),2,move), (1-team,t))
        m = 2 * basic.COORDINATE_X_MAX
        for i in move:
            d = main.distance(i, (8,14))
            if m > d:
                d = m
                j = i
        d = []; t = 0
        if m == 0:
            for i in range(Info.base[1-team]):
                if main.distance(Info.base[1-team][i].position, self.position) in range(2,11):
                    if Info.base[1-team][i].life > 0 and Info.base[1-team][i].position == (9, 2):
                        return basic.Command(1, j, (1-team,i))
                    d += [i]
                    if Info.base[1-team][i].life > 0 and m < (self.strength - Info.base[1-team][i].defence) * basic.ATTACK_EFFECT[self.kind][Info.base[1-team][i].kind]:
                        m = (self.strength - Info.base[1-team][i].defence) * basic.ATTACK_EFFECT[self.kind][Info.base[1-team][i].kind]
                        t = i
            for i in d:
                if Info.base[1-team][i].kind == basic.WIZARD:
                    return basic.Command(1, j, (1-team,i))
            return basic.Command(1, j, (1-team,t))
        else:
            return basic.Command(0, j, (0, 0))
    elif self.kind == basic.DRAGON_RIDER:
        d = 2 * basic.COORDINATE_X_MAX; t = 0
        for i in move:
            if i[1]==9 and 5 <= i[0] <= 9:
                return basic.Command(0, i, (0, 0))
            if main.distance(i, (9,8)) < d:
                d = main.distance(i, (9,8))
                t = i
        i = 0
        for d in attack_id(whole_map, Info.base, (team,unit),move):
            if main.distance(t,Info.base[1-team][d]) == 1:
                if Info.base[1-team][d].kind==basic.SABER or Info.base[1-team][d].kind == basic.ARCHER:
                    i = d; break;
        return basic.Command(1, t, (1-team,i))
    else:
        if not(self.position[1]<=2 or self.position[1]>=5) and find_person(Info.base,(3,0))!=(-1,-1):
            if (0,2) in move:
                return basic.Command(1, (0,2), (1-team,0))
            d = 2 * basic.COORDINATE_X_MAX; t = 0
            for i in move:
                if main.distance(i, (0,2)) < d:
                    d = main.distance(i, (0,2))
                    t = i
            return basic.Command(1,t,(1-team,0))
        m = 0; c = 0
        for i in attack_id(whole_map, Info.base, (team,unit),move):
            t = (self.strength - Info.base[1-team][i].defence) * basic.ATTACK_EFFECT[self.kind][Info.base[1-team][i].kind]
            if m < t:
                m = t; c = i;
        return basic.Command(1,find_position(whole_map, Info.base, (team, unit),(1-team,c),self.attack_range,move), (1-team,c))
    

def GetHeroType_6(mapInfo,base):
    return basic.HERO_2
def AI_6(whole_map,Info):
    team=Info.id[0]
    unit=Info.id[1]
    self=Info.base[team][unit]
    move = Info.range
    target_range = attack_id(whole_map, Info.base, (team, unit), move)
    damage = 0; most_damage = 0; target_id = -1
    for i in target_range:
            target = Info.base[1-team][i]
            damage = (self.strength - target.defence) * basic.ATTACK_EFFECT[self.kind][target.kind]
            if self.kind != basic.WIZARD and target.kind != basic.WIZARD:
                sacrifice = (target.strength - self.defence) * basic.ATTACK_EFFECT[target.kind][self.kind]
            else:
                sacrifice = 0
            if most_damage < damage and (sacrifice < self.life or target.attack_range != self.attack_range):
                    most_damage = damage
                    target_id = i
    if target_id != -1:
            return basic.Command(1 ,find_position(whole_map, Info.base,Info.id,(1 - team,target_id), self.attack_range, move),(1 - team, target_id))
    else:
            min_d = basic.COORDINATE_X_MAX * 2
            t = self.position
            for i in move:
                    for k in Info.base[1 - team]:
                            d = main.distance(i, k.position)
                            if min_d > d:
                                    min_d = d; t = i
            return basic.Command(0, t, (0, 0))
def GetHeroType_7(mapInfo,base):
    return basic.HERO_1
def AI_7(whole_map,Info):
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
            if target.kind != basic.WIZARD:
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
	

'''
aiInfo = 'TestBattle_AI'
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
'''