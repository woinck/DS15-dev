#include "basic.h"
#include <stdio.h>

game_info info = {};
char teamName[20]="Player";        //在这里设定队伍名字，尽量用英文

int GetHeroType()
{
	return ASSASSIN;   //选择英雄
}

int move_range(Game_Info &gameInfo, int team, int id, Position *tmp);

Command AI_main()
{
	Command cmd = {};
	//选手在这里写自己的AI主函数
	int num = 0;
	Position range[300] = {};
	num = move_range(info, info.team_number, info.move_id, range);
	
	cmd.destination = range[0];
	cmd.order = wait;
	return cmd;
}

