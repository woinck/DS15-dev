#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#我自己用个人算法给队式写的搜路函数
import copy

def GetRoute(map_list, units_list, idNum, end_pos):
    """参量map_list为传入的二维地图数组，行列分别代表着地图上的行列;
    参量units_list为传入的二维单位数组，两行多列，行代表队伍;
    参量idNum为代表行动单位的二元组;参量end_pos为命令中指定的目标坐标;
    函数返回一个数组，数组中元素是依次需要走过的格点坐标,如果无法到达该格点，
    返回空数组"""    
    def __getRoute(avail_list, beg_pos, end_pos, step):
        """传入可以走的列表，开始以及结束位置，可以用的步数,返回route数组
        以及标识flag代表是否成功找到路"""
        if step <= 0:
            return [],False
        if beg_pos == end_pos:
            return [],True
        neighbor = ((beg_pos[0]+1, beg_pos[1]), (beg_pos[0]-1, beg_pos[1]),
                    (beg_pos[0], beg_pos[1]+1), (beg_pos[0], beg_pos[1]-1))
        tmp_list = [avail_list[i][:2] for i in range(len(avail_list))]
        possible_route = []
        for pos in neighbor:
            if pos in tmp_list:
                new_step = step - avail_list[tmp_list.index(pos)][2]
                new_avail = copy.copy(avail_list)
                if beg_pos in tmp_list:
                    new_avail.pop(tmp_list.index(beg_pos))
                route, flag = __getRoute(new_avail, pos, end_pos, new_step)
                if flag:
                    route.insert(0, pos)
                    possible_route.append(route)
        if possible_route:
            len_ = [len(i) for i in possible_route]
            return possible_route[len_.index(min(len_))],True

        else:
            return [],False
    
    border = [units_list[i][j].position \
                  for i in range(2) for j in range(len(units_list[0]))]
    avail_list = [(i, j ,map_list[i][j].move_consumption) for i in range(len(map_list)) \
                      for j in range(len(map_list[0])) \
                      if (i, j) not in border]
    beg_pos = units_list[idNum[0]][idNum[1]].position
    step = units_list[idNum[0]][idNum[1]].move_range
    route, flag = __getRoute(avail_list, beg_pos, end_pos, step)
    return route

#for test
if __name__ == "__main__":
    import Ui_2DReplay.testdata
    print GetRoute(Ui_2DReplay.testdata.maps, Ui_2DReplay.testdata.units2_, (0,1),(2,1))
