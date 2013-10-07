#include<winsock2.h>
#include<stdio.h>
#include"basic.h"
#pragma comment(lib,"WS2_32.lib")

command AI_main(); //选手编写的AI主函数

SOCKET client; //声明client，用于下面的get_soldier_info()的调用
void get_soldier_info()
{
	for(int i = 0; i < initial.soldier_number[0]; i++)
	{
		memset(recvbuf, 0, sizeof(char)*128);
		recv(client, recvbuf, 127, 0);
		sscanf(recvbuf, "%d %d %d %d %d %d %d %d %d %d %d %d", &initial.soldier[i][0].kind, &initial.soldier[i][0].life, &initial.soldier[i][0].attack,  &initial.soldier[i][0].agility,  &initial.soldier[i][0].defence,  &initial.soldier[i][0].move_range,  &initial.soldier[i][0].move_speed,  &initial.soldier[i][0].attack_range[0], &initial.soldier[i][0].attack_range[1], &initial.soldier[i][0].up,  &initial.soldier[i][0].p.x,  &initial.soldier[i][0].p.y);
		send(client, "ok", 2, 0);
	}
	for(int i = 0; i < initial.soldier_number[1]; i++)
	{
		memset(recvbuf, 0, sizeof(char)*128);
		recv(client, recvbuf, 127, 0);
		sscanf(recvbuf, "%d %d %d %d %d %d %d %d %d %d %d %D", &initial.soldier[i][1].kind, &initial.soldier[i][1].life, &initial.soldier[i][1].attack,  &initial.soldier[i][1].agility,  &initial.soldier[i][1].defence,  &initial.soldier[i][1].move_range,  &initial.soldier[i][1].move_speed,  &initial.soldier[i][1].attack_range[0], &initial.soldier[i][1].attack_range[1],&initial.soldier[i][1].up,  &initial.soldier[i][1].p.x,  &initial.soldier[i][1].p.y);
		send(client, "ok", 2, 0);
	}
} //用于每回合更新双方单位信息

void main()
{
	WORD wVersionRequired;
	WSADATA wsaData;
	wVersionRequired = MAKEWORD(1, 1);
	if ( WSAStartup(wVersionRequired, &wsaData) != 0 )
	{
		printf("The version required is not found!/n");
		return;
	}
	client = socket(AF_INET, SOCK_STREAM, 0);
	SOCKADDR_IN cliaddr;
	cliaddr.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");
	cliaddr.sin_family = AF_INET;
	cliaddr.sin_port = htons(8818);
	connect(client, (sockaddr*)&cliaddr, sizeof(sockaddr));
	send(client, "AI has connected.", 17, 0);
	//建立socket连接
	
	recv(client, recvbuf, 127, 0);
	sscanf(recvbuf, "%d", &initial.team_number);
	send(client, "ok", 2, 0);
	for(int i = 0; i < COORDINATE_X_MAX; i++)
		for(int j = 0; j < COORDINATE_Y_MAX; j++)
		{
			memset(recvbuf, 0, sizeof(char)*128);
			recv(client, recvbuf, 127, 0);
			sscanf(recvbuf, "%d", &initial.map[i][j]);
			send(client, "ok", 2, 0);
		}
	memset(recvbuf, 0, sizeof(char)*128);
	recv(client, recvbuf, 127, 0);
	sscanf(recvbuf, "%d", &initial.mirror_number);
	send(client, "ok", 2, 0);
	for(int i = 0; i < initial.mirror_number; i++)
	{
		memset(recvbuf, 0, sizeof(char)*128);
		recv(client, recvbuf, 127, 0);
		sscanf(recvbuf, "%d %d %d %d", &initial.mir[i].self.x, &initial.mir[i].self.y, &initial.mir[i].out.x, &initial.mir[i].out.y);
		send(client, "ok", 2, 0);
	}
	memset(recvbuf, 0, sizeof(char)*128);
	recv(client, recvbuf, 127, 0);
	sscanf(recvbuf, "%d %d", &initial.soldier_number[0], &initial.soldier_number[1]);
	send(client, "ok", 2, 0);
	get_soldier_info();
	//读取初始信息
	

	while(1)
	{
		memset(recvbuf, 0, sizeof(char)*128);
		recv(client, recvbuf, 127, 0);
		if(recvbuf[0] == '#') break; //以#作为游戏结束标志
		sscanf(recvbuf, "%d %d %d %d %d", &info.move_id, &info.temple_number, &info.turn, &info.score[0], &info.score[1]);
		send(client, "ok", 2, 0);
		for(int i = 0; i < info.temple_number; i++)
		{
			memset(recvbuf, 0, sizeof(char)*128);
			recv(client, recvbuf, 127, 0);
			sscanf(recvbuf, "%d %d %d", &info.temple[i].pos.x, &info.temple[i].pos.y, &info.temple[i].state);
			send(client, "ok", 2, 0);
		}
		get_soldier_info();
  		cmd = AI_main();
		memset(sendbuf, 0, sizeof(char)*128);
		sprintf(sendbuf, "%d %d %d %d", cmd.order, cmd.target_id, cmd.destination.x, cmd.destination.y);
		send(client, sendbuf, strlen(sendbuf), 0); 
	} //游戏按回合进行，直到分出胜负

	closesocket(client);
	WSACleanup();
}

