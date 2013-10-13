#include "basic.h"
#include <stdlib.h>

extern game_info info;

Position* move_range(int team_number, int move_id) { //搜索单位可移动范围,以（-1，-1）结束
  typedef struct spot {
    Position pos;
    int move_consume;
  }Spot;
  Soldier_Basic self = info.soldier[move_id][team_number];
  int o = 0, s = 0, d = 0, i, j, b;
  Position end = {-1,-1};
  Position* result = (Position*)(malloc(self.move_range * self.move_range * sizeof(Position)));
  Spot* up_layer = (Spot*)(malloc(sizeof(Spot))), * down_layer;
  Position* other_block = (Position*)(malloc((SOLDIERS_NUMBER + COORDINATE_X_MAX) * sizeof(Position)));
  Position* self_block = (Position*)(malloc(SOLDIERS_NUMBER * sizeof(Position)));
  const Position direction[4] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
  int l = 1, a, i_x, i_y, t;
  short r;
 Position pos;
 if(self.kind != AIRPLANE)
  {for(j = 0; j < SOLDIERS_NUMBER; j++)
     {if(info.soldier[j][1 - team_number].life > 0) {other_block[o] = info.soldier[j][1 - team_number].pos; o++;}
      if(info.soldier[j][team_number].life > 0 && j != move_id) {self_block[s] = info.soldier[j][team_number].pos; s++;}
      }
   for(i = 0; i < COORDINATE_X_MAX; i++)
    for(j = 0; j < COORDINATE_Y_MAX; j++)
      if(info.map[i][j] == BARRIER) {other_block[o].x = i; other_block[o].y = j; o++;}
   }
 result[d] = self.pos; d++;
 up_layer[0].pos = self.pos; up_layer[0].move_consume = 1;
 for(i = 0; i < self.move_range; i++)
  {down_layer = (Spot*)(malloc((l * 4 + 1) * sizeof(Spot)));
   a = 0;
   for(j = 0; j < l; j++)
       if(up_layer[j].move_consume >= FIELD_EFFECT[info.map[up_layer[j].pos.x][up_layer[j].pos.y]][0])
           for(t = 0; t < 4; t++)
            {i_x = up_layer[j].pos.x + direction[t].x;
             i_y = up_layer[j].pos.y + direction[t].y;
             if(0 <= i_x && i_x <= COORDINATE_X_MAX && 0 <= i_y && i_y<=COORDINATE_Y_MAX)
               {r = 1;
                pos.x = i_x; pos.y = i_y;
                for(b = 0; b < o; b++)
                    if(other_block[b].x == pos.x && other_block[b].y == pos.y) {r = 0;break;}
                for(b = 0; b < d; b++)
                    if(pos.x == result[b].x && pos.y == result[b].y) {r = 0;break;}
                if(r)
                   {down_layer[a].pos = pos;
                    down_layer[a].move_consume = 1;
                    a++;
                    r = 1;
                    for(b = 0; b < s; s++)
                       if(self_block[b].x == pos.x && self_block[b].y == pos.y) r = 0;
                    if(r)
                      {result[d] = pos;
                       d++;}
                    }
                }
            }
       else
         {down_layer[a].pos = up_layer[j].pos;
          down_layer[a].move_consume = up_layer[j].move_consume + 1;
          a++;}
   l = a;
   free(up_layer);
   up_layer = down_layer;}
 free(up_layer); free(other_block); free(self_block);
 result[d] = end;
 return result;}
