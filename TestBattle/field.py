# -*- coding: cp936 -*-
import basic

def construct_map(kind):
    '''利用类型构造地图对象(除传送门单独构造)'''
    if kind == basic.TURRET:
        return basic.Map_Turret(kind)
    elif kind == basic.TEMPLE:
        return basic.Map_Temple(kind)
    else:
        return basic.Map_Basic(kind)
def get_position(string):
    x = (ord(string[0]) - 48) * 10 + (ord(string[1]) - 48)
    y = (ord(string[3]) - 48) * 10 + (ord(string[4]) - 48)
    return (x, y)
def print_position(point):
    string = ''
    num_0 = chr(point[0] / 10 + 48) + chr(point[0] % 10 + 48)
    num_1 = chr(point[1] / 10 + 48) + chr(point[1] % 10 + 48)
    string += num_0 + ',' + num_1
    return string

def get_map(route, whole_map, base):
    '''文件操作,读入地图
       whole_map表示地形类型    
       base[0],base[1]列表表示士兵
       route为地图存储路径'''
    map_file = open(route, "r")
    k = 0
    while 1:
        string = map_file.readline()
        if string == "\n":
            break
        m = []
        for c in string[:-1]:
            kind = ord(c) - 48
            m += [construct_map(kind)]
            if kind == basic.MIRROR:
                k += 1
        whole_map += [m]
    for i in range(1, k+1):
        string = map_file.readline()
        mirror_position = get_position(string[:5])
        mirror_control = get_position(string[6:])
        whole_map[mirror_position[0]][mirror_position[1]] = basic.Map_Mirror(basic.MIRROR, mirror_control)
    #将读入的数字地图转化为类型地图
    for i in [0,1]:
        string = map_file.readline()
        while string != '\n':
            c = string[0]
            position = get_position(string[2:7])
            base[i] += [basic.Base_Unit(ord(c) - 48, position)]
            string = string[8:]
    map_file.close()
    #读入士兵
def print_map(route, whole_map, base):
    '''文件操作，将地图写入文件
       whole_map表示地形类型    
       base[0],base[1]列表表示士兵
       route为地图存储路径'''    
    map_file = open(route, 'w')
    map_mirror = []
    for i in range(len(whole_map)):
        for j in range(len(whole_map[i])):
            map_file.write(chr(whole_map[i][j].kind + 48))
            if whole_map[i][j].kind == basic.MIRROR:
                map_mirror += [(i, j)]
        map_file.write('\n')
    map_file.write('\n')
    for i in map_mirror:
        m = whole_map[i[0]][i[1]].out
        map_file.write(print_position((i[0],i[1])) + ':' + print_position((m[0],m[1])) + ';\n')
    for i in range(2):
        for j in base[i]:
            map_file.write(chr(j.kind + 48) + ':' + print_position(j.position) + ';')
        map_file.write('\n')
    map_file.close()
'''应用示例：
whole_map = []; base = [[], []]
get_map('E:\活动\队式\逻辑\Map.txt', whole_map, base)
print_map('E:\活动\队式\逻辑\Map.txt', whole_map, base)'''
