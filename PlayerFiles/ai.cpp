#include "basic.h"
#include <stdio.h>

game_info info = {};
char teamName[20]="Player";        //�������趨�������֣�������Ӣ��

int GetHeroType()
{
	return ASSASSIN;   //ѡ��Ӣ��
}

void ChooseSoldier(int num_inc, int id[])
{

	for (int i=0; i<num_inc; i++)
	{
		if (info.soldier[0][1-info.team_number].kind == ARCHMAGE) info.soldier[id[i]][info.team_number].kind = 4;
		else info.soldier[id[i]][info.team_number].kind = 3;	
	}

}

int move_range(Game_Info &gameInfo, int team, int id, Position *tmp);

Command AI_main()
{
	Command cmd = {};
	//ѡ��������д�Լ���AI������
	int num = 0;
	Position range[300] = {};
	num = move_range(info, info.team_number, info.move_id, range);
	
	cmd.destination = range[0];
	cmd.order = wait;
	return cmd;
}

