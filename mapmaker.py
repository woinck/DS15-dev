from basic import *
from field_shelve import *
import sio
m = Map_Basic
u = Base_Unit
mirror = Map_Mirror

maps = [[m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0), mirror(6, (7,0)), m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
        [mirror(6,(0, 3)), m(0), m(1), m(1), m(1), m(1), m(1), m(0),mirror(6, (7,1)), m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0),mirror(6, (7,2)), m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
        [m(0), m(0), Map_Turret(4), m(1), m(1), m(1), m(1), m(0),mirror(6, (7,3)), m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
        [basic.Map_Temple(5), Map_Turret(4), m(1), m(1), m(1), m(1), m(1), m(0),mirror(6, (7,4)), m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0),mirror(6, (7,5)), m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0),mirror(6, (7,6)), m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0),mirror(6, (7,7)), m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
		[m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0),mirror(6, (8,0)), m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
		[m(0), Map_Turret(4), m(1), m(1), m(1), m(1), m(1), m(0),mirror(6, (8,1)), m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
		[m(0), Map_Turret(4), m(1), m(1), m(1), m(1), m(1), m(0),mirror(6, (8,2)), m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
		[m(0), Map_Turret(4), m(1), m(1), m(1), m(1), m(1), m(0),mirror(6, (7,8)), m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
		[m(0), Map_Turret(4), m(1), m(1), m(1), m(1), m(1), m(0),mirror(6, (8,7)), m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
		[m(0), Map_Turret(4), m(1), m(1), m(1), m(1), m(1), m(0),mirror(6, (5,2)), m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
		[m(0), Map_Turret(4), m(1), m(1), m(1), m(1), m(1), m(0),mirror(6, (10,0)), m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
		[m(0), Map_Turret(4), m(1), m(1), m(1), m(1), m(1), m(0),mirror(6, (10,1)), m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
		[m(0), Map_Turret(4), m(1), m(1), m(1), m(1), m(1), m(0),m(1),m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
		[m(0), Map_Turret(4), m(1), m(1), m(1), m(1), m(1), m(0),m(1),m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
		[m(0), Map_Turret(4), m(1), m(1), m(1), m(1), m(1), m(0),m(1),m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)],
		[m(0), Map_Turret(4), m(1), m(1), m(1), m(1), m(1), m(0),m(1),m(3),m(1),m(0),m(1),m(2),m(2),m(1),m(2),m(1),m(0),m(1)]]

units0 = [[u(6, (0, 0)), u(2, (1, 0)), u(3, (0, 2))],
          [u(6, (3, 3)), u(2, (3, 2)), u(1, (3, 1))]]
        
'''
maps = [[m(0), m(0)],
        [m(0), m(0)]]
units0 = [[u(5, (0, 0))],
          [u(3, (1, 1))]]
''' 
#write_to((maps,units0))
<<<<<<< HEAD
sio._WriteFile((maps,units0),'C:\Users\woinck\Documents\GitHub\DS15-dev\\Sample_Map.map')
=======
sio._WriteFile((maps,units0),'C:\Users\Fox\Documents\GitHub\DS15-dev\\mapwithturret.map')
>>>>>>> server_debugging
