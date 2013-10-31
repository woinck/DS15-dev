#include<winsock2.h>
#include<stdio.h>
#include"basic.h"
#include <Windows.h>
#pragma comment(lib,"WS2_32.lib")

extern game_info info;
extern char teamName[20];
extern int GetHeroType();

Command cmd;  //选手操作,每回合传给逻辑
char recvbuf[128] = {}; //从平台接收信息
char sendbuf[128] = {}; //向平台发送信息

SOCKET client; //声明client，用于下面的get_soldier_info()的调用

void ChooseSoldier(int num_inc, int id[]);
command AI_main();

void get_soldier_info()
{
	for(int i = 0; i < info.soldier_number[0]; i++)
	{
		memset(recvbuf, 0, sizeof(char)*128);
		recv(client, recvbuf, 127, 0);
		sscanf(recvbuf, "%d %d %d %d %d %d %d %d %d %d", &info.soldier[i][0].kind, &info.soldier[i][0].life, &info.soldier[i][0].strength,    &info.soldier[i][0].defence,  &info.soldier[i][0].move_range,    &info.soldier[i][0].attack_range[0], &info.soldier[i][0].attack_range[1], &info.soldier[i][0].duration,  &info.soldier[i][0].pos.x,  &info.soldier[i][0].pos.y);
		send(client, "ok", 3, 0);
	}
	for(int i = 0; i < info.soldier_number[1]; i++)
	{
		memset(recvbuf, 0, sizeof(char)*128);
		recv(client, recvbuf, 127, 0);
		sscanf(recvbuf, "%d %d %d %d %d %d %d %d %d %d", &info.soldier[i][1].kind, &info.soldier[i][1].life, &info.soldier[i][1].strength,    &info.soldier[i][1].defence,  &info.soldier[i][1].move_range,    &info.soldier[i][1].attack_range[0], &info.soldier[i][1].attack_range[1],&info.soldier[i][1].duration,  &info.soldier[i][1].pos.x,  &info.soldier[i][1].pos.y);
		send(client, "ok", 3, 0);
	}
} //用于每回合更新双方单位信息

int main()
{
	WORD wVersionRequired;
	WSADATA wsaData;
	wVersionRequired = MAKEWORD(1, 1);
	if ( WSAStartup(wVersionRequired, &wsaData) != 0 )
	{
		printf("The version required is not found!/n");
		return 1;
	}
	client = socket(AF_INET, SOCK_STREAM, 0);
	SOCKADDR_IN cliaddr;
	cliaddr.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");
	cliaddr.sin_family = AF_INET;
	cliaddr.sin_port = htons(8803);
	if(connect(client, (sockaddr*)&cliaddr, sizeof(sockaddr)) == -1)
	{
		printf("\n==============欢迎参加队式十五==============\n\n");
		printf("没有检测到平台端口，请确认平台程序已经运行再运行本程序\n");
		system("pause>nul");
		exit(0);
	}
	//建立socket连接
	
	
	recv(client, recvbuf, 127, 0);
	sscanf(recvbuf, "%d", &info.team_number);
	send(client, "ok", 3, 0);

	for (int i = 0; i < 2; i++)
	{
	memset(recvbuf, 0, sizeof(char)*128);
	recv(client, recvbuf, 127, 0);
	sscanf(recvbuf, "%d", &info.map_size[i]);
	send(client, "ok", 3, 0);
	}

	for(int i = 0; i < info.map_size[0]; i++)
		for(int j = 0; j < info.map_size[1]; j++)
		{
			memset(recvbuf, 0, sizeof(char)*128);
			recv(client, recvbuf, 127, 0);
			sscanf(recvbuf, "%d", &info.map[i][j]);
			send(client, "ok", 3, 0);
		}


	memset(recvbuf, 0, sizeof(char)*128);
	recv(client, recvbuf, 127, 0);
	sscanf(recvbuf, "%d", &info.mirror_number);
	send(client, "ok", 3, 0);
	for(int i = 0; i < info.mirror_number; i++)
	{
		memset(recvbuf, 0, sizeof(char)*128);
		recv(client, recvbuf, 127, 0);
		sscanf(recvbuf, "%d %d %d %d", &info.mir[i].inPos.x, &info.mir[i].inPos.y, &info.mir[i].outPos.x, &info.mir[i].outPos.y);
		send(client, "ok", 3, 0);
	}

	///////////////////////////////////以下为自由选择兵种模式关闭和开启的处理
	if (FREE_CHOOSE == 0)   
	{
		memset(recvbuf, 0, sizeof(char)*128);
		recv(client, recvbuf, 127, 0);
		sscanf(recvbuf, "%d %d", &info.soldier_number[0], &info.soldier_number[1]);
		send(client, "ok", 3, 0);
		get_soldier_info();
		//读取初始信息
	}

	else while (1)
	{
		memset(recvbuf, 0, sizeof(char)*128);		
		recv(client, recvbuf, 127, 0);
		if (recvbuf[0] == '|') 
		{
			send(client, "ok", 2, 0);	
			break; //以|作为选择结束标志
		}

		int enemy_inc, self_inc; //对方最新选择兵种的士兵数目，己方本轮需要进行选择的士兵数
		int choice[2]; //对方最新选择的兵种号
		int id[2]; //当前要选兵种的士兵号
		sscanf(recvbuf, "%d %d %d %d %d %d", &enemy_inc, &choice[0], &choice[1], &self_inc, &id[0], &id[1]);

		for (int i=info.soldier_number[1-info.team_number]; i<info.soldier_number[1-info.team_number]+enemy_inc; i++) //读取对手的已选信息
		{
			info.soldier[i][1-info.team_number].kind = choice[i-info.team_number];
		}
		info.soldier_number[1-info.team_number] += enemy_inc;

		ChooseSoldier(self_inc, id); //调用选手编写的选择函数		
	
		memset(sendbuf, 0, sizeof(char)*128);        //向平台发送选择信息
		if (self_inc == 1) 
		{
			sprintf(sendbuf, "%d", info.soldier[id[0]]);
			send(client, sendbuf, 1, 0);
		}
		else 
		{
			sprintf(sendbuf, "%d %d", info.soldier[id[0]], info.soldier[id[1]]);
			send(client, sendbuf, 3, 0);
		}

		info.soldier_number[info.team_number] += self_inc;
	}

	

	while(1)
	{
		memset(recvbuf, 0, sizeof(char)*128);		
		recv(client, recvbuf, 127, 0);

		if(recvbuf[0] == '|') break; //以|作为游戏结束标志
		sscanf(recvbuf, "%d %d %d %d %d", &info.move_id, &info.temple_number, &info.turn, &info.score[0], &info.score[1]);
		send(client, "ok", 3, 0);

		for(int i = 0; i < info.temple_number; i++)
		{
			memset(recvbuf, 0, sizeof(char)*128);
			recv(client, recvbuf, 127, 0);
			sscanf(recvbuf, "%d %d %d", &info.temple[i].pos.x, &info.temple[i].pos.y, &info.temple[i].state);
			send(client, "ok", 3, 0);
		}
		get_soldier_info();
  		cmd = AI_main();
		memset(sendbuf, 0, sizeof(char)*128);
		sprintf(sendbuf, "%d %d %d %d", (int)cmd.order, cmd.target_id, cmd.destination.x, cmd.destination.y);
		send(client, sendbuf, strlen(sendbuf), 0); 
	} //游戏按回合进行，直到分出胜负

	closesocket(client);
	WSACleanup();
	return 0;
}

