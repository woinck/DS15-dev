#ifndef _BASIC_H
#define _BASIC_H

/////////////////////////////////////////////////////////////
// ��Ϸ��������
/////////////////////////////////////////////////////////////

const int TURN_MAX = 30;         // ���غ���
const int COORDINATE_X_MAX = 20; // ��ͼ���Χ
const int COORDINATE_Y_MAX = 20;
const int SOLDIERS_NUMBER = 10;  // ��λ��������
const int MIRROR_MAX = 20;       // ħ����������
const int TEMPLE_MAX = 10;       // �ż���������

/////////////////////////////////////////////////////////////
// ��Ϸ��ͼ����
/////////////////////////////////////////////////////////////

// ��ͼ���ͱ��
const int PLAIN = 0;    // ƽԭ
const int MOUNTAIN = 1; // ɽ��
const int FOREST = 2;   // ɭ��
const int BARRIER = 3;  // ����
const int TURRET = 4;   // ����
const int TEMPLE = 5;   // �ż�
const int MIRROR = 6;   // ħ��

// ����Ч������: �ƶ�������, ���ֽ���, �����ӳ�, �����ӳɡ�
// ����ĵ�i��j��Ԫ�ض�Ӧ�ŵ�i��Ԫ�صĵ�j��Ч��
const int FIELD_EFFECT[][5] = {{1, 0, 0, 0},
                               {2, 0, 0, 1},
                               {2, 0, 0, 0},
                               {1, 0, 0, 0},
                               {1, 2, 0, 0},
                               {1, 3, 0, 0},
                               {1, 1, 0, 0}};

const int TEMPLE_UP_TIME = 10;     // �ż���������Ļغϼ��
const int TURRET_SCORE_TIME = 5;   // ����ռ�������������ֽ����Ļغ���
const int TURRET_RANGE = 10;       // ����������                          

const int HERO_UP_LIMIT = 5;      // Ӣ��ͨ���ż��������ļӳɴ�������
const int BASE_UP_LIMIT = 3;      // ��ͨ��λͨ���ż��������ļӳɴ�������
const int HERO_SCORE = 5;         // Ӣ��ʣ��Ѫ���ķ����ӳ�
const int BASE_SCORE = 3;         // ��ͨ��λʣ��Ѫ���ķ����ӳ�


/////////////////////////////////////////////////////////////
// ��Ϸ��λ����
/////////////////////////////////////////////////////////////

const int SABER = 0;              // ��ʿ
const int SOLDIER = 1;            // ͻ����
const int ARCHER = 2;             // �ѻ���
const int AIRPLANE = 3;           // ս��
const int TANK = 4;               // ̹��
const int WIZARD = 5;             // ����ʦ
const int BERSERKER = 6;          // ��սʿ
const int ASSASSIN = 7;           // ��ɱ��
const int ARCHMAGE = 8;           // ��ʦ

const int LIFE_COST = 5;          // Ӣ��1���ͷż���ʱ���ĵ�����ֵ
const int CRITICAL_HIT_RATE = 10; // Ӣ��2�ı����� 
const int UP_DURANCE = 5;         // Ӣ��3�ļ��ܼӳɵ�ʱ������   

// ��λ���Բ���������ֵ�����������������ƶ���
const int ABILITY[][6] = {{25, 18, 12, 6},
                          {25, 17, 13, 7},
                          {25, 17, 12, 6},
                          {21, 15, 12, 8},
                          {30, 17, 14, 5},
                          {21, 10, 12, 6},
                          {55, 20, 14, 5},
                          {40, 20, 13, 6},
                          {45, 18, 14, 7}};

// �����������Ч��
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
// �ṹ�嶨��
/////////////////////////////////////////////////////////////

typedef struct position { // λ�ýṹ�壬����xy����
    int x, y;
}Position;

typedef struct soldier_basic { // ������λ�ṹ�壬�������л���������
    int kind, life, strength, defence, move_range;
    int attack_range[2]; // attack_range[1][0]��ʾ������Χ������
    int duration; // ��λ��Ӣ��3�ļ���ǿ����ʱ��
    Position pos;
}Soldier_Basic;

typedef struct temple { // ����ṹ��
    Position pos;
    int state; // ��ʾ�������״̬��0������Ƭ��1������+1��2���ƶ�+1��3������+1��
}Temple;

typedef struct mirror { // ħ���ṹ��
  Position inPos, outPos; // ����ʹ�����λ�� 
} Mirror; 

typedef struct game_info { // ��Ϸ��Ϣ�ṹ�壬ÿ�غ�ѡ�ִ��л�ȡ��Ҫ����Ϣ
    int team_number;                              // �����(0��1)
    int map[COORDINATE_X_MAX][COORDINATE_Y_MAX];  // ��ͼ��������
	int map_size[2];                              // ��ͼ��[0]����[1]
    int mirror_number;                            // ħ������
    Mirror mir[MIRROR_MAX];                       // �����ľ���λ�ü�����
    int soldier_number[2];                        // ������λ����
    int move_id;                                  // �ƶ���λ����ʾ�������е�move_id����
    int score[2];                                 // ���ӵ�ǰ����(���������ʿ����ռ��
    int turn;                                     // ��ǰ�ܻغ���
    int temple_number;                            // ��������
    Temple temple[TEMPLE_MAX];                    // �������λ�ü�״̬
    Soldier_Basic soldier[SOLDIERS_NUMBER][2];    // ˫����λ����Ϣ
}Game_Info;

typedef enum cmd_order { //command order��ö������
	wait, attack, skill
}Cmd_Order;

typedef struct command {  // ѡ�ֲ���,ÿ�غϴ����߼�
    Position destination; // Ҫ�ƶ���Ŀ�ĵ�
    Cmd_Order order;            // wait:������attack:������skill:����
    int target_id;        // Ŀ�굥λ
} Command;
#endif