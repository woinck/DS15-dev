#include<stdio.h>
#include<stdlib.h>
#include"basic.h"

double attack_match(Soldier_Basic a, Soldier_Basic b)
{double hit_possiblity = (a.speed * 3 - b.speed * 2)/100.0;
 int damage = (a.attack - b.defence) * ATTACK_EFFECT[a.kind][b.kind];
 return hit_possiblity * damage;}

command AI_main(round_begin_info info)
{int target_id = -1, i, j, k;
 Soldier_Basic target = initial.soldier[0][1 - info.team_number], cur;
 Soldier_Basic self = initial.soldier[info.move_id][info.team_number];
 command cmd = {self.p, 0, -1};
 int* target_range;
 double a, b;
 int distance = COORDINATE_X_MAX + COORDINATE_Y_MAX, cur_distance;
 target_range = attack_range(info.team_number, info.move_id, info.move_range);
 for(i = 0; target_range[i] != -1; i++)
  {j = target_range[i];
   cur = initial.soldier[j][1 - info.team_number];
   if(cur.life - ((self.attack - target.defence) * ATTACK_EFFECT[self.kind][target.kind]) < 0 && (self.speed * 3 - target.speed * 2) >= 75)
	{target_id = j;
	 break;}
   a = attack_match(self, target);b = attack_match(self, cur);
   if(a < b && b > 0)
	 {target = cur;
	  target_id = i;}
   }
 free(target_range);
 if(target_id != -1)
   {Position end = {-1,-1}, pos;
    for(i = 0; info.move_range[i] != end; i++)
	 {pos = info.move_range[i];
	  distance = abs(target.p.x - pos.x) + abs(target.p.y - pos.y);
	  if(distance >= self.attack_range[0] && distance <= self.attack_range[1])
	    break;}
	cmd.destination = pos;
	cmd.order = 1;
	cmd.target_id = target_id;}
 else
   {Position destination, pos;
    for(i = 0; info.move_range[i] != end; i++)
	  for(k = 0; k < SOLDIERS_NUMBER; k++)
	   {pos = info.move_range[i];
	    target = initial.soldier[k][1 - info.team_number];
	    cur_distance = abs(target.p.x - pos.x) + abs(target.p.y - pos.y);
	    if(cur_distance < distance)
		 {destination = pos;
		  distance = cur_distance;}
	    }
	cmd.destination = destination;}
//选手在这里写自己的AI主函数

	return cmd;
}