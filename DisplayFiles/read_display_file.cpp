#include <iostream>
#include <fstream>
#include <direct.h>
#include <string.h>
#include <string>
#include <vector>
#include "display_basic.h"
using namespace std;

Game_Info info = {};
Round_Begin_Info rbinfo = {};
Command cmd = {};
round_End_Info reinfo = {};

int main()
{
	char* path = getcwd(NULL, 0);
	strcat(path, "\\\DisplayFiles\\\display.rep");
	ifstream fin(path);
	
	fin >> info.map_size[0] >> info.map_size[1];
	for (int i=0; i<info.map_size[0]; i++)
		for (int j=0; j<info.map_size[1]; j++)
			fin >> info.map[i][j];
	fin >> info.team_name[0] >> info.team_name[1];
	for (int i=0; i<2; i++)
	{
		fin >> info.soldier_number[i];
		for (int j=0; j<info.soldier_number[i]; j++)
			fin >> info.soldier[j][i].kind >> info.soldier[j][i].life 
				  >> info.soldier[j][i].strength >> info.soldier[j][i].defence
				  >> info.soldier[j][i].move_range >> info.soldier[j][i].attack_range[0]
				  >> info.soldier[j][i].attack_range[1] >> info.soldier[j][i].duration
				  >> info.soldier[j][i].pos.x >> info.soldier[j][i].pos.y;
	}
	//////////////以上为读入初始信息

	rbinfo.temple.resize(info.temple_number);

	while (!reinfo.over)
	{
		fin >> rbinfo.move_team >> rbinfo.move_id;
		fin >> rbinfo.range_num;
		rbinfo.range.resize(rbinfo.range_num);
		for (int i=0; i<rbinfo.range_num; i++)
		{
			fin >> rbinfo.range[i].x >> rbinfo.range[i].y;
		}
		for (int i=0; i<2; i++)
		{
			fin >> rbinfo.soldier_number[i];
			for (int j=0; j<rbinfo.soldier_number[i]; j++)
				fin >> rbinfo.soldier[j][i].kind >> rbinfo.soldier[j][i].life 
					  >> rbinfo.soldier[j][i].strength >> rbinfo.soldier[j][i].defence
					  >> rbinfo.soldier[j][i].move_range >> rbinfo.soldier[j][i].attack_range[0]
					  >> rbinfo.soldier[j][i].attack_range[1] >> rbinfo.soldier[j][i].duration
					  >> rbinfo.soldier[j][i].pos.x >> rbinfo.soldier[j][i].pos.y;
		}
		for (int i=0; i<info.temple_number; i++)
		{
			fin >> rbinfo.temple[i].pos.x >> rbinfo.temple[i].pos.y >> rbinfo.temple[i].state;
		}

		////////////////展示组操作

		fin >> cmd.destination.x >> cmd.destination.y >> cmd.order
			  >> cmd.target_team >> cmd.target_id;

		////////////////展示组操作

		for (int i=0; i<2; i++)
		{
			fin >> reinfo.soldier_number[i];
			for (int j=0; j<reinfo.soldier_number[i]; j++)
				fin >> reinfo.soldier[j][i].kind >> reinfo.soldier[j][i].life 
					  >> reinfo.soldier[j][i].strength >> reinfo.soldier[j][i].defence
					  >> reinfo.soldier[j][i].move_range >> reinfo.soldier[j][i].attack_range[0]
					  >> reinfo.soldier[j][i].attack_range[1] >> reinfo.soldier[j][i].duration
					  >> reinfo.soldier[j][i].pos.x >> reinfo.soldier[j][i].pos.y;
		}
		fin >> reinfo.route_len;
		reinfo.route.resize(reinfo.route_len);
		for (int i=0; i<reinfo.route_len; i++)
		{
			fin >> reinfo.route[i].x >> reinfo.route[i].y;
		}
		fin >> reinfo.score[0] >> reinfo.score[1];
		fin >> reinfo.attack_effect[0] >> reinfo.attack_effect[1];
		fin >> reinfo.trans >> reinfo.over;

		///////////////展示操作
	}
}


	