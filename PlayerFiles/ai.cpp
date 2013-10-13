#include "basic.h"
#include "Basic2.h"
#include <stdio.h>

game_info info;
wchar_t teamName[20]=L"player";

int GetHeroType()
{
	return ASSASSIN;
}

Command AI_main()
{
	Command cmd;
	//选手在这里写自己的AI主函数
	
	if (info.move_id == 1) 
	{
		cmd.order = wait;
		cmd.destination.x = 1;
		cmd.destination.y = 2;
		cmd.target_id = 0;
	}

	if (info.move_id == 2) 
	{
		cmd.order = wait;
		cmd.destination.x = 2;
		cmd.destination.y = 2;
		cmd.target_id = 0;
	}

	if (info.move_id == 0) 
	{
		cmd.order = attack;
		cmd.destination.x = 1;
		cmd.destination.y = 0;
		cmd.target_id = 0;
	}

	/*
	empty AI
	cmd.order = wait;
	cmd.destination = info.soldier[info.move_id][info.team_number].pos;
	cmd.target_id = 0;
	*/
	return cmd;
}