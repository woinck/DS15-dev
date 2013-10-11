#ifndef _BASIC_H
#define _BASIC_H

/////////////////////////////////////////////////////////////
// 游戏基本参数
/////////////////////////////////////////////////////////////

const int TURN_MAX = 30;         // 最大回合数
const int COORDINATE_X_MAX = 20; // 地图最大范围
const int COORDINATE_Y_MAX = 20;
const int SOLDIERS_NUMBER = 10;  // 单位数量上限
const int MIRROR_MAX = 10;       // 魔镜数量上限
const int TEMPLE_MAX = 10;       // 遗迹数量上限

/////////////////////////////////////////////////////////////
// 游戏地图参数
/////////////////////////////////////////////////////////////

// 地图类型编号
const int PLAIN = 0;    // 平原
const int MOUNTAIN = 1; // 山地
const int FOREST = 2;   // 森林
const int BARRIER = 3;  // 屏障
const int TURRET = 4;   // 炮塔
const int TEMPLE = 5;   // 遗迹
const int MIRROR = 6;   // 魔镜

// 地形效果矩阵: 移动力消耗, 积分奖励, 攻击加成, 防御加成。
// 数组的第i，j个元素对应着第i种元素的第j种效果
const int FIELD_EFFECT[][5] = {{1, 0, 0, 0},
                               {2, 0, 0, 1},
                               {2, 0, 0, 0},
                               {1, 0, 0, 0},
                               {1, 2, 0, 0},
                               {1, 3, 0, 0},
                               {1, 1, 0, 0}};

const int TEMPLE_UP_TIME = 10;     // 遗迹出现神符的回合间隔
const int TURRET_SCORE_TIME = 5;   // 连续占有炮塔触发积分奖励的回合数
const int TURRET_RANGE = 10;       // 炮塔最大射程                          

const int HERO_UP_LIMIT = 5;      // 英雄通过遗迹获得神符的加成次数上限
const int BASE_UP_LIMIT = 3;      // 普通单位通过遗迹获得神符的加成次数上限
const int HERO_SCORE = 3;         // 英雄剩余血量的分数加成
const int BASE_SCORE = 1;         // 普通单位剩余血量的分数加成


/////////////////////////////////////////////////////////////
// 游戏单位参数
/////////////////////////////////////////////////////////////

const int SABER = 0;              // 剑士
const int SOLDIER = 1;            // 突击兵
const int ARCHER = 2;             // 狙击手
const int AIRPLANE = 3;           // 战机
const int TANK = 4;               // 坦克
const int WIZARD = 5;             // 治疗师
const int BERSERKER = 6;          // 狂战士
const int ASSASSIN = 7;           // 暗杀者
const int ARCHMAGE = 8;           // 大法师

const int LIFE_COST = 5;          // 英雄1在释放技能时消耗的生命值
const int CRITICAL_HIT_RATE = 10; // 英雄2的暴击率 
const int UP_DURANCE = 5;         // 英雄3的技能加成的时间限制   

// 单位属性参数：生命值、攻击力、防御、移动力和移动顺序
const int ABILITY[][6] = {{25, 18, 12, 6, 1},
                          {25, 17, 13, 7, 2},
                          {25, 17, 12, 6, 3},
                          {21, 15, 12, 8, 4},
                          {30, 17, 14, 5, 5},
                          {21, 10, 12, 6, 6},
                          {55, 20, 14, 5, 0},
                          {40, 20, 13, 6, 0},
                          {45, 18, 14, 7, 0}};

// 攻击的相克性效果
const float ATTACK_EFFECT[][9] = {{1,   0.5, 1, 0.5, 1.5, 1, 1, 1, 1},
                                  {1.5, 1,   1, 1,   0.5, 1, 1, 1, 1},
                                  {1,   1,   1, 2,   2,   1, 1, 1, 1},
                                  {1.5, 1,   1, 1,   0.5, 1, 1, 1, 1},
                                  {0.5, 1.5, 1, 1.5, 1,   1, 1, 1, 1},
                                  {1,   1,   1, 1,   1,   1, 1, 1, 1},
                                  {1,   1,   1, 1,   1,   1, 1, 1, 1},
                                  {1,   1,   1, 1,   1,   1, 1, 1, 1},
                                  {1,   1,   1, 1,   1,   1, 1, 1, 1}};

/////////////////////////////////////////////////////////////
// 结构体定义
/////////////////////////////////////////////////////////////

typedef struct position { // 位置结构体，包含xy坐标
    int x, y;
    bool operator==(Position pos) { return (x == pos.x) && (y == pos.y); }
    bool operator!=(const Position pos) { return !(*this == pos); }
}Position;

typedef struct soldier_basic { // 基本单位结构体，包含所有基本的属性
    int kind, life, attack, defence, move_range, move_order;
    int attack_range[2]; // attack_range[1][0]表示攻击范围上下限
    int duration; // 单位被英雄3的技能强化的时间
    Position pos;
}Soldier_Basic;

typedef struct temple { // 神庙结构体
    Position pos;
    int state; // 表示神庙神符状态，0：无碎片；1：攻击+1；2：移动+1；3：防御+1；
}Temple;

typedef struct mirror { // 魔镜结构体
  Position inPos, outPos; // 进入和传出的位置 
} Mirror; 

typedef struct game_info { // 游戏信息结构体，每回合选手从中获取必要的信息
    int team_number;                              // 队伍号(0或1)
    int map[COORDINATE_X_MAX][COORDINATE_Y_MAX];  // 地图各点类型
	int map_size[2];                              // 地图行[0]、列[1]
    int mirror_number;                            // 魔镜数量
    Mirror mir[MIRROR_MAX];                       // 各处的镜子位置及出口
    int soldier_number[2];                        // 各方单位数量
    int move_id;                                  // 移动单位，表示本队伍中第move_id个人
    int score[2];                                 // 两队当前积分(不包括存活士兵所占）
    int turn;                                     // 当前总回合数
    int temple_number;
    Temple temple[TEMPLE_MAX];                    // 各神庙的位置及状态
    Soldier_Basic soldier[SOLDIERS_NUMBER][2];    // 双方单位的信息
}Game_Info;

typedef struct command {  // 选手操作,每回合传给逻辑
    Position destination; // 要移动的目的地
    int order;            // 0:待机，1:攻击，2:技能
    int target_id;        // 目标单位
} Command;
#endif