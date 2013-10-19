#include "basic.h"
#include <stdio.h>

game_info info = {};
char teamName[20]="Sample";

int GetHeroType()
{
	return ASSASSIN;   //选择英雄
}

void ChooseSoldier(int num_inc, int id[]) //兵种（kind）选择函数，num_inc表示本轮需要进行选择的士兵数量，id[i]表示第i个需要选择种类的士兵编号
{
	//选手在这里写选择兵种的策略，以下为示例
	for (int i=0; i<num_inc; i++)
	{
		if(info.soldier[0][1-info.team_number].kind == BERSERKER) //如果对方的英雄为狂战士
			info.soldier[id[i]][info.team_number].kind = 1;
		else info.soldier[id[i]][info.team_number].kind = 2;
	}
}


Command AI_main()
{
	Command cmd;
	//选手在这里写自己的AI主函数
	
	cmd.order = wait;
	cmd.destination = info.soldier[info.move_id][info.team_number].pos;
	cmd.destination.x--; 
	cmd.target_id = 0;
	return cmd;
}