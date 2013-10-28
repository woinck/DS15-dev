#include "basic.h"
#include <stdio.h>

game_info info = {};

char teamName[20]="Player";        //在这里设定队伍名字，尽量用英文


int GetHeroType()
{
	return ASSASSIN;   //閫夋嫨鑻遍泟
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
	//閫夋墜鍦ㄨ繖閲屽啓鑷繁鐨凙I涓诲嚱鏁?
	
	cmd.destination = info.soldier[info.move_id][info.team_number].pos;
	cmd.order = wait;
	cmd.target_id = 0;

	return cmd;
}

