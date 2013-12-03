#include "basic.h"
#define NULL 0
#define INFINITE 10086
const int MaxV = 20; // 地图边长最大值
const int AdjacentVec[4][2] = { // 四个毗邻点的方向向量
    {0, -1}, {0, 1}, {-1, 0}, {1, 0}};
void relax(Game_Info &gameInfo, int *pathv, int v, int col, int row);
int minEdge(int num, int *pathv);

// 计算所得的移动范围坐标将连续储存在选手传入的地址tmp表示后，
// 请确保tmp后申请了足够多的空间用以储存移动范围。
// 返回值move_range直接返回能够到达的点的数量。 
// team和id分别代表寻求单位的队伍和单位号。
int move_range(Game_Info &gameInfo, int team, int id, Position *tmp) { 
    Soldier_Basic &mvObj = gameInfo.soldier[id][team];  // 当前移动单位结构体
    int pathv[MaxV * MaxV];                             // 维护从源点到各点的最短距离
    // 求地图列数和行数
    int col = gameInfo.map_size[0], row = gameInfo.map_size[1];                             
    int chash = col; if (col < row) chash = row;

    int source = mvObj.pos.x * chash + mvObj.pos.y;       // 源点在pathv中的index

    for (int i = 0; i < chash * chash; ++i)             // 初始化最短距离为正无穷
        pathv[i] = INFINITE;
    pathv[source] = 0;                                  // 源点距离为0
    tmp[0].x = mvObj.pos.x; tmp[0].y = mvObj.pos.y;    
    relax(gameInfo, pathv, source, id, team);           // 于源点处松弛
    int num = 1;                                        // 记录已证实可达的点数
    while (true) {
        int pathNum = minEdge(chash * chash - 1, pathv);    // 贪心

        // 在移动力耗尽以及没有点可松弛时跳出
        if (pathv[pathNum] > mvObj.move_range || pathNum == -1) {
            break;
        } else {
            int x = pathNum / chash, y = pathNum % chash;   // 松弛点在地图中的坐标
            // 除去己敌方单位
            int flag = 0;
            for (int teamx = 0; teamx < 2; ++teamx)
                for (int i = 0; i < gameInfo.soldier_number[teamx]; ++i) {
                    if ((x == gameInfo.soldier[i][teamx].pos.x) && 
                        (y == gameInfo.soldier[i][teamx].pos.y) && 
                        (gameInfo.soldier[i][teamx].life)) {
                            flag = 1; break;}
                }
            // 将该点并入结果中
            if (!flag) { tmp[num].x = x; tmp[num++].y = y;}
            relax(gameInfo, pathv, pathNum, id, team);  // 松弛
        }
        pathv[pathNum] = 0;                             // 置0表示该点已经松弛过
    }
    return num;
}

// 使用pathv中的第v个终点来松弛
void relax(Game_Info &gameInfo, int *pathv, int v, int id, int team) { 
    int col = gameInfo.map_size[0], row = gameInfo.map_size[1];
    int chash = col; if (col < row) chash = row;
    int vx = v / chash, vy = v % chash; // 第v个点在地图中的坐标
    for (int i =0; i < 4; ++i) {    // 4个方向松弛
        int endx = vx + AdjacentVec[i][0], endy = vy + AdjacentVec[i][1];
        if (endx >=0 && endy >= 0 && endx < col && endy < row) {
            int pathEnd = endx * chash + endy;
            int edgeLen = FIELD_EFFECT[gameInfo.map[vx][vy]][0];
            
            if (gameInfo.soldier[id][team].kind
                == AIRPLANE) { edgeLen = 1; } // 飞行单位无视地形
            else {  // 判断是否遇到障碍
                int eneNum = gameInfo.soldier_number[1 - team];
                for (int i = 0; i < eneNum; ++i) {
                    Soldier_Basic 
                        &eneSol = gameInfo.soldier[i][1 - team];
                    if (eneSol.pos.x == endx && 
                        eneSol.pos.y == endy && eneSol.life>0) {
                            edgeLen = INFINITE;
                            break;
                    }
                }
                if (gameInfo.map[endx][endy] == BARRIER) {
                    edgeLen = INFINITE;
                }
            }
            // 松弛
            if (pathv[pathEnd] && edgeLen + pathv[v] < pathv[endx * chash + endy]) {
                pathv[endx * chash + endy] = edgeLen + pathv[v];
            }

        }
    }
}

int minEdge(int num, int *pathv) { // 贪心最短路，在没有可行路径时返回-1
    int minCost = INFINITE, tmp = 0;
    for (int i = 0; i < num; ++i) {
        if (pathv[i] < minCost && pathv[i]) {
            minCost = pathv[i];
            tmp = i;
        }
    }
    if (minCost == INFINITE) return -1;
    return tmp;
}
