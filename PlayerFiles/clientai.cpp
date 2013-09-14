#include<winsock2.h>
#include<stdio.h>
#include"ai.cpp"
#pragma comment(lib,"WS2_32.lib")

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
	
	SOCKET client = socket(AF_INET, SOCK_STREAM, 0);
	SOCKADDR_IN cliaddr;
	cliaddr.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");
	cliaddr.sin_family = AF_INET;
	cliaddr.sin_port = htons(8818);
	connect(client, (sockaddr*)&cliaddr, sizeof(sockaddr));
	send(client, "AI has connected.", 17, 0);

	char recvbuf[128] = {};
	char sendbuf[128] = {};
	round_begin_info info;
	command cmd;

	while(1)
	{
		recv(client, recvbuf, 127, 0);
		if(recvbuf[0] == '#') break;
		int nrange; //move_range的数组长度
		sscanf(recvbuf, "%d %d %d", &info.move_id, &info.temple_state, &nrange);
		memset(info.move_range, 0, sizeof(position)*nrange);
		for(int i=0; i<nrange; i++) sscanf(recvbuf, "%d %d", &info.move_range[i].x, &info.move_range[i].y);
		cmd = AI_main(info);
		strcpy(sendbuf, "");
		sprintf(sendbuf, "%d %d %d %d", cmd.destination.x, cmd.destination.y, cmd.order, cmd.target_id);
		send(client, sendbuf, strlen(sendbuf), 0); 
	}

	closesocket(client);
	WSACleanup();
}