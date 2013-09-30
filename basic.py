# -*- coding: UTF-8 -*-
import random
import time
#常量采用全字母大写，变量及函数全字母小写，类名首字母大写，单词用‘—‘隔开
random.seed(time.time())
TURN_MAX = 20
COORDINATE_X_MAX = 20
COORDINATE_Y_MAX = 20
SOLDIERS_NUMBER = 10

TURRET_RANGE = range(2,11)
TEMPLE_UP_TIME = 10
TURRET_SCORE_TIME = 5

PLAIN = 0#平原
MOUNTAIN = 1#山地
FOREST = 2#森林
BARRIER = 3#屏障
TURRET = 4#炮塔
TEMPLE = 5#神庙
MIRROR = 6#传送门
FIELD_EFFECT = {PLAIN:(1,0,0,0,0),
                MOUNTAIN:(2,0,0,0,1),
                FOREST:(2,0,0,1,0),
                BARRIER:(1,0,0,0,0),
                TURRET:(1,2,0,0,0),
                TEMPLE:(1,3,0,0,0),
                MIRROR:(1,0,0,0,0)}
#(move_consumption, score, strength_up, agility_up, defence_up)
HERO_UP_LIMIT = 5
BASE_UP_LIMIT = 3
HERO_SCORE = 3
BASE_SCORE = 1
HERO_1_REPAIR_COST = 5
HERO_2_KILL_RATE = 10
HERO_3_UP_TIME = 5

SABER = 0#剑士
LANCER = 1#枪兵
ARCHER = 2#弓兵
DRAGON_RIDER = 3#飞骑兵
WARRIOR = 4#战士
WIZARD = 5#法师
HERO_1 = 6
HERO_2 = 7
HERO_3 = 8
ABILITY = {SABER:(25,18,95,12,6,[1],5),
           LANCER:(25,17,90,13,7,[1],4),
           ARCHER:(25,17,90,12,6,[2],3),
           DRAGON_RIDER:(21,15,95,10,8,[1],2),
           WARRIOR:(30,20,85,15,5,[1],1),
           WIZARD:(21,10,90,12,6,[],0),
           HERO_1:(55,17,90,15,5,[1],6),
           HERO_2:(40,20,100,13,6,[1],6),
           HERO_3:(45,20,95,14,7,[1,2],6)}
#(LIFE, STRENGTH, AGILITY, DEFENCE, MOVE_RANGE, ATTACK_RANGE, MOVE_SPEED)
#WIZARD:不可攻击，STRENGTH表示回复生命数
ATTACK_EFFECT = {SABER:{SABER:1, LANCER:0.5, ARCHER:1, DRAGON_RIDER:0.5, WARRIOR:1.5, WIZARD:1, HERO_1:1, HERO_2:1, HERO_3:1},
                 LANCER:{SABER:1.5, LANCER:1, ARCHER:1, DRAGON_RIDER:1, WARRIOR:0.5, WIZARD:1, HERO_1:1, HERO_2:1, HERO_3:1},
                 ARCHER:{SABER:1, LANCER:1, ARCHER:1, DRAGON_RIDER:2, WARRIOR:1, WIZARD:1, HERO_1:1, HERO_2:1, HERO_3:1},
                 DRAGON_RIDER:{SABER:1.5, LANCER:1, ARCHER:1, DRAGON_RIDER:1, WARRIOR:0.5, WIZARD:1, HERO_1:1, HERO_2:1, HERO_3:1},
                 WARRIOR:{SABER:0.5, LANCER:1.5, ARCHER:1, DRAGON_RIDER:1.5, WARRIOR:1, WIZARD:1, HERO_1:1, HERO_2:1, HERO_3:1},
                 HERO_1:{SABER:1, LANCER:1, ARCHER:1, DRAGON_RIDER:1, WARRIOR:1, WIZARD:1, HERO_1:1, HERO_2:1, HERO_3:1},
                 HERO_2:{SABER:1, LANCER:1, ARCHER:1, DRAGON_RIDER:1, WARRIOR:1, WIZARD:1, HERO_1:1, HERO_2:1, HERO_3:1},
                 HERO_3:{SABER:1, LANCER:1, ARCHER:1, DRAGON_RIDER:1, WARRIOR:1, WIZARD:1, HERO_1:1, HERO_2:1, HERO_3:1}}
#相克性
class Map_Basic:
    '''基本地形：平原、山地、森林、屏障、陷阱
    FIELD_EFFECT(move_consumption, score, strength_up, agility_up, defence_up)'''
    def __init__(self, kind):
        self.kind = kind
        self.score = FIELD_EFFECT[kind][1]
        self.move_consumption = FIELD_EFFECT[kind][0]
    def effect(self, base, whole_map, unit_id, score):
        '''地形效果'''
        base[unit_id[0]][unit_id[1]].strength += FIELD_EFFECT[self.kind][2]
        base[unit_id[0]][unit_id[1]].agility += FIELD_EFFECT[self.kind][3]
        base[unit_id[0]][unit_id[1]].defence += FIELD_EFFECT[self.kind][4]
    def leave(self, base, unit_id):
        '''离开地形后能力恢复'''
        base[unit_id[0]][unit_id[1]].strength -= FIELD_EFFECT[self.kind][2]
        base[unit_id[0]][unit_id[1]].agility -= FIELD_EFFECT[self.kind][3]
        base[unit_id[0]][unit_id[1]].defence -= FIELD_EFFECT[self.kind][4]
class Map_Turret(Map_Basic):
    '''特殊地形：炮塔
    FIELD_EFFECT(move_consumption, score, strength_up, agility_up, defence_up)'''
    def __init__(self, kind):
        self.kind = kind
        self.score = FIELD_EFFECT[kind][1]
        self.move_consumption = FIELD_EFFECT[kind][0]
        self.time = 0
    def effect(self, base, whole_map, unit_id, score):
        k = base[unit_id[0]][unit_id[1]].kind
        if k == ARCHER:
            base[unit_id[0]][unit_id[1]].attack_range = TURRET_RANGE
    def leave(self, base, unit_id):
        k = base[unit_id[0]][unit_id[1]]
        if k == ARCHER:
            base[unit_id[0]][unit_id[1]].attack_range = ABILITY[ARCHER][5]
        self.time = 0
class Map_Temple(Map_Basic):
    '''特殊地形：神庙
    FIELD_EFFECT(move_consumption, score, strength_up, agility_up, defence_up)'''
    def __init__(self, kind):
        self.kind = kind
        self.score = FIELD_EFFECT[kind][1]
        self.move_consumption = FIELD_EFFECT[kind][0]
        self.time = 0 #神庙计数器 
        self.up = random.choice([1,2,3]) #下一个神符种类
    def effect(self, base, whole_map, unit_id, score):
        if self.time >= TEMPLE_UP_TIME and ((w.kind < 6 and w.up < BASE_UP_LIMIT) or (w.kind > 5 and w.up < HERO_UP_LIMIT)):
            base[unit_id[0]][unit_id[1]].up += 1
            if self.up == 1:
                base[unit_id[0]][unit_id[1]].strength += 1
            elif self.up == 2:
                base[unit_id[0]][unit_id[1]].agility += 1
            elif self.up == 3:
                base[unit_id[0]][unit_id[1]].defence += 1
            self.time = 0
            self.up = random.choice([1,2,3])
            score[unit_id[0]] += self.score
class Map_Mirror(Map_Basic):
    '''特殊地形：传送门
    FIELD_EFFECT(move_consumption, score, strength_up, agility_up, defence_up)'''
    def __init__(self, kind, out = (0,0)):
        self.kind = kind
        self.score = FIELD_EFFECT[kind][1]
        self.move_consumption = FIELD_EFFECT[kind][0]
        self.out = out #传送出口
    def effect(self, base, whole_map, unit_id, score):
        r = True
        for i in base:
            for j in i:
                if j.position == self.out:
                    r = False
        if r:
            base[unit_id[0]][unit_id[1]].move(self.out)
class Base_Unit:
    '''一般士兵
    (LIFE, STRENGTH, AGILITY, DEFENCE, MOVE_RANGE, ATTACK_RANGE, MOVE_SPEED)'''
    def __init__(self, kind, position = (0,0)):
        self.kind = kind
        self.up = 0 #士兵能力上升数
        self.position = position
        self.life = ABILITY[kind][0]
        self.strength = ABILITY[kind][1]
        self.agility = ABILITY[kind][2]
        self.defence = ABILITY[kind][3]
        self.move_range = ABILITY[kind][4]
        self.attack_range = ABILITY[kind][5]
        self.move_speed = ABILITY[kind][6]
        self.time = 0
    def move(self, p):
        '''移动至p = (x, y)'''
        self.position = p
    def attack(self, base, enemy_id):
        '''攻击 enemy'''
        enemy = base[enemy_id[0]][enemy_id[1]]
        r = random.uniform(0,100)
        s = (r <= (self.agility*3 - enemy.agility*2))
        if self.strength > enemy.defence:
            base[enemy_id[0]][enemy_id[1]].life -= int((self.strength - enemy.defence) * s * ATTACK_EFFECT[self.kind][enemy.kind])
        return s
    def skill(self, base, other_id):
        '''法师对other使用回复技能'''
        other = base[other_id[0]][other_id[1]]
        if self.kind == WIZARD:
            base[other_id[0]][other_id[1]].life += self.strength
            if base[other_id[0]][other_id[1]].life > ABILITY[other.kind][0]:
                base[other_id[0]][other_id[1]].life = ABILITY[other.kind][0]   
    def __lt__(self, orther):
        '''比较攻击顺序'''
        return self.move_speed > orther.move_speed
class Hero(Base_Unit):
    def skill(self, base, other_id):
        '''英雄技能'''
        other = base[other_id[0]][other_id[1]]
        if self.kind == HERO_1:
            self.life -= HERO_1_REPAIR_COST
            base[other_id[0]][other_id[1]].life += self.strength
            if base[other_id[0]][other_id[1]].life > ABILITY[other.kind][0]:
                base[other_id[0]][other_id[1]].life = ABILITY[other.kind][0]   
        if self.kind == HERO_3 and other.time == 0:
            base[other_id[0]][other_id[1]].time = 1
            base[other_id[0]][other_id[1]].defence += 1
            base[other_id[0]][other_id[1]].agility += 1
            base[other_id[0]][other_id[1]].strength += 1
    def attack(self, base, enemy_id):
        enemy = base[enemy_id[0]][enemy_id[1]]
        if self.kind == HERO_2:
            d = enemy.defence * (random.uniform(0,100) > HERO_2_KILL_RATE)
        else:
            d = enemy.defence
        r = random.uniform(0,100)
        s = (r <= (self.agility*3 - enemy.agility*2))
        base[enemy_id[0]][enemy_id[1]].life -= (self.strength - d) * s * ATTACK_EFFECT[self.kind][enemy.kind]
        return s        
class Begin_Info:
    def __init__(self, whole_map, base, hero_type = [6,6]):
        self.map = whole_map #二维地图列表
        self.base = base #二维士兵列表，第一维表示队伍0/1
        self.hero_type = hero_type #二元数组表示两队英雄类型
class Round_Begin_Info:
    def __init__(self, move_unit, move_range, base, temple):
        self.id = move_unit #如(0,2)表示0队第三个士兵
        self.range = move_range #坐标列表，如[(0,0),(1,0)]
        self.base = base 
        self.temple = temple
#temple列表表示各神庙是否出现神符，如[[(1,1),0],[(2,3),2]]表示(1,1)处神庙无神符,(2,3)处神庙有2类神符        
class Command:
    def __init__(self,order = 0, move_position = 0, target_id = 0):
        self.move = move_position #坐标(x,y)
        self.order = order #0:待机，1:攻击，2:技能
        self.target = target_id #同Round_Begin_Info.move_unit
class Round_End_Info:
    def __init__(self, base, route, attack_effect, score, over = False):
        self.base = base
        self.route = route#行动路线，点列表
        self.score = score #二元数组，表示当前两队积分
        self.over = over #布尔型，True为结束
        self.effect = attack_effect #二元组表示攻击与反击方是否命中,1表示命中，0表示未命中，-1表示未攻击(超出攻击范围或已死亡),如(1,-1)表示攻击命中，目标未反击
