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
	if (FREE_CHOOSE == 0)   
	{
		memset(recvbuf, 0, sizeof(char)*128);
		recv(client, recvbuf, 127, 0);
		sscanf(recvbuf, "%d %d", &info.soldier_number[0], &info.soldier_number[1]);
		send(client, "ok", 3, 0);
		get_soldier_info();
		//��ȡ��ʼ��Ϣ
	}

	else while (1)
	{
		memset(recvbuf, 0, sizeof(char)*128);		
		recv(client, recvbuf, 127, 0);
		if (recvbuf[0] == '|') 
		{
			send(client, "ok", 2, 0);	
			break; //��|��Ϊѡ�������־
		}

		int enemy_inc, self_inc; //�Է�����ѡ����ֵ�ʿ����Ŀ������������Ҫ����ѡ���ʿ����
		int choice[2]; //�Է�����ѡ��ı��ֺ�
		int id[2]; //��ǰҪѡ���ֵ�ʿ����
		sscanf(recvbuf, "%d %d %d %d %d %d", &enemy_inc, &choice[0], &choice[1], &self_inc, &id[0], &id[1]);

		for (int i=info.soldier_number[1-info.team_number]; i<info.soldier_number[1-info.team_number]+enemy_inc; i++) //��ȡ���ֵ���ѡ��Ϣ
		{
			info.soldier[i][1-info.team_number].kind = choice[i-info.team_number];
		}
		info.soldier_number[1-info.team_number] += enemy_inc;

		ChooseSoldier(self_inc, id); //����ѡ�ֱ�д��ѡ����		
	
		memset(sendbuf, 0, sizeof(char)*128);        //��ƽ̨����ѡ����Ϣ
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
		get_soldier_info();
  		cmd = AI_main();
		memset(sendbuf, 0, sizeof(char)*128);
		sprintf(sendbuf, "%d %d %d %d", (int)cmd.order, cmd.target_id, cmd.destination.x, cmd.destination.y);
		send(client, sendbuf, strlen(sendbuf), 0); 
	} //��Ϸ���غϽ��У�ֱ���ֳ�ʤ��

	closesocket(client);
	WSACleanup();
	return 0;
}

