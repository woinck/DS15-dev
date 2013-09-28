from basic import *
from field_shelve import *
m = Map_Basic
u = Base_Unit
mirror = Map_Mirror
maps = [[m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [mirror(6,(3, 0)), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)]]
units0 = [[u(5, (0, 0)), u(2, (1, 0)), u(3, (0, 2))],
          [u(3, (3, 3)), u(2, (3, 2)), u(1, (3, 1))]]
        

        
write_to((maps,units0))