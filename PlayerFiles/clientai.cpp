#include<winsock2.h>
#include<stdio.h>
#include"basic.h"
#include <Windows.h>
#pragma comment(lib,"WS2_32.lib")

extern game_info info;
extern char teamName[20];
extern int GetHeroType();

Command cmd;  //ѡ�ֲ���,ÿ�غϴ����߼�
char recvbuf[128] = {}; //��ƽ̨������Ϣ
char sendbuf[128] = {}; //��ƽ̨������Ϣ

SOCKET client; //����client�����������get_soldier_info()�ĵ���

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
} //����ÿ�غϸ���˫����λ��Ϣ

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
		printf("\n==============��ӭ�μӶ�ʽʮ��==============\n\n");
		printf("û�м�⵽ƽ̨�˿ڣ���ȷ��ƽ̨�����Ѿ����������б�����\n");
		system("pause>nul");
		exit(0);
	}
	//����socket����
	
	
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

	///////////////////////////////////����Ϊ����ѡ�����ģʽ�رպͿ����Ĵ���

		memset(recvbuf, 0, sizeof(char)*128);
		recv(client, recvbuf, 127, 0);
		sscanf(recvbuf, "%d %d", &info.soldier_number[0], &info.soldier_number[1]);
		send(client, "ok", 3, 0);
		get_soldier_info();
		//��ȡ��ʼ��Ϣ


	send(client, (char *) teamName, sizeof teamName, 0);
	recv(client, recvbuf, 3, 0);
	int heroType = GetHeroType();
	memset(sendbuf,0,sizeof(char)*128);
	sprintf(sendbuf,"%d",heroType);
	send(client,sendbuf,strlen(sendbuf),0);

	while(1)
	{
		memset(recvbuf, 0, sizeof(char)*128);		
		recv(client, recvbuf, 127, 0);

		if(recvbuf[0] == '|') break; //��|��Ϊ��Ϸ������־
		sscanf(recvbuf, "%d %d %d %d %d", &info.move_id, &info.temple_number, &info.turn, &info.score[0], &info.score[1]);
		send(client, "ok", 3, 0);

		for(int i = 0; i < info.temple_number; i++)
		{
			memset(recvbuf, 0, sizeof(char)*128);
			recv(client, recvbuf, 127, 0);
			sscanf(recvbuf, "%d %d %d", &info.temple[i].pos.x, &info.temple[i].pos.y, &info.temple[i].state);
			send(client, "ok", 3, 0);
		}
		printf("senttttttttt");
		get_soldier_info();
  		cmd = AI_main();
		memset(sendbuf, 0, sizeof(char)*128);
		sprintf(sendbuf, "%d %d %d %d", (int)cmd.order, cmd.target_id, cmd.destination.x, cmd.destination.y);
		send(client, sendbuf, strlen(sendbuf), 0); 
		printf("sentTTTTTTTTTTTTTTTTTTTTTTTT");
	} //��Ϸ���غϽ��У�ֱ���ֳ�ʤ��

	closesocket(client);
	WSACleanup();
	return 0;
}

