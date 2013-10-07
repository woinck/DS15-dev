#include"basic.h"
command AI_main()
{
	command cmd;
	//选手在这里写自己的AI主函数
	cmd.order = 1;
	cmd.target_id = 0;
	cmd.destination.x = initial.soldier[0][1 - initial.team_number].p.x + 1 ; cmd.destination.y = initial.soldier[0][1 - initial.team_number].p.y + 1;
	return cmd;
}