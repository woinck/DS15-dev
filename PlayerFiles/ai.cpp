#include "basic.h"
#include <stdio.h>

game_info info = {};
char teamName[20]="Player";        //在这里设定队伍名字，尽量用英文

int GetHeroType()
{
	return ASSASSIN;   //选择英雄
}

int move_range(Game_Info &gameInfo, int team, int id, Position *tmp);

void ChooseSoldier(int num_inc, int id[])
{

	for (int i=0; i<num_inc; i++)
	{
		if (id[i] == 0) info.soldier[id[i]][info.team_number].kind = ARCHMAGE;

		if (info.soldier[0][1-info.team_number].kind == ARCHMAGE) info.soldier[id[i]][info.team_number].kind = 4;
		else info.soldier[id[i]][info.team_number].kind = 3;	
	}

}

Command AI_main()
{
	Command cmd;
	//选手在这里写自己的AI主函数
	
	

	return cmd;
}

