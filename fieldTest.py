# -*- coding: cp936 -*-
import basic

def construct_map(kind):
    '''�������͹����ͼ����(�������ŵ�������)'''
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
def readline(string, i = 1):
    '''��ȡstring�ı��ĵ�i��'''
    for j in range(0,i):
        c = ""
        while(string[0]!='\n'):
            c += string[0]
            string = string[1:]
        c += string[0]
        string = string[1:]
    return c
def get_map(txt, whole_map, base):
    '''�ļ�����,�����ͼ
       whole_map��ʾ��������    
       base[0],base[1]�б��ʾʿ��
       txtΪ��ͼ�ı�'''
    k = 0; t = 1
    while 1:
        string = readline(txt, t)
        t += 1
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
        string = readline(txt, t)
        t += 1
        mirror_position = get_position(string[:5])
        mirror_control = get_position(string[6:])
        whole_map[mirror_position[0]][mirror_position[1]] = basic.Map_Mirror(basic.MIRROR, mirror_control)
    #����������ֵ�ͼת��Ϊ���͵�ͼ
    for i in [0,1]:
        string = readline(txt, t)
        t += 1
        while string != '\n':
            c = string[0]
            position = get_position(string[2:7])
            base[i] += [basic.Base_Unit(ord(c) - 48, position)]
            string = string[8:]
    #����ʿ��
'''Ӧ��ʾ����(string��Ϊ��ͼ�ı�)
whole_map = []; base = [[], []]
get_map(string, whole_map, base)'''
