#include "basic.h"
#include <stdio.h>

game_info info = {};
char teamName[20]="Sample";

int GetHeroType()
{
	return ASSASSIN;   //ѡ��Ӣ��
}

void ChooseSoldier(int num_inc, int id[]) //���֣�kind��ѡ������num_inc��ʾ������Ҫ����ѡ���ʿ��������id[i]��ʾ��i����Ҫѡ�������ʿ�����
{
	//ѡ��������дѡ����ֵĲ��ԣ�����Ϊʾ��
	for (int i=0; i<num_inc; i++)
	{
		if(info.soldier[0][1-info.team_number].kind == BERSERKER) //����Է���Ӣ��Ϊ��սʿ
			info.soldier[id[i]][info.team_number].kind = 1;
		else info.soldier[id[i]][info.team_number].kind = 2;
	}
}


Command AI_main()
{
	Command cmd;
	//ѡ��������д�Լ���AI������
	
	cmd.order = wait;
	cmd.destination = info.soldier[info.move_id][info.team_number].pos;
	cmd.destination.x--; 
	cmd.target_id = 0;
	return cmd;
}