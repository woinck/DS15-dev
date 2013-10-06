 #-*- coding: UTF-8 -*-
import shelve
import basic

default = 'default_map.db'
key = ("map", "base") # 定义shelve类的键值为"map"和"base"


def change_path(path):
	'''如果有必要的话，定义一个改变路径的函数也是极好的'''
	pass

def read_from(filename = default, change_path = 0):
	'''从文件中读取地图信息和单位信息的函数,
	函数接受文件名(扩展名一定为.db)和路径改变
	参数作为形参，返回二元元组(map, base)即地
	图和单位列表。'''
	

	if change_path:
		pass # TODO!!!
	try:
		filename = filename.encode('gbk')
		shelv_in = shelve.open(filename)
		return (shelv_in[key[0]], shelv_in[key[1]])
	except IOError as err:
		print 'File error: ' + str(err)
	except KeyError as kerr:
		print 'Key error: ' + str(kerr)
	finally:
		shelv_in.close();

def write_to(info_tuple, filename = default, change_path = 0):
	'''将地图信息和单位信息写入文件, 接受二元元组(map, base)
	为参数。filename和change_path定义同上。写入成功返回1，
	否则返回0.'''
	if change_path:
		pass # TODO!!!
	try:
		shelv_out = shelve.open(filename)
		shelv_out[key[0]] = info_tuple[0]
		shelv_out[key[1]] = info_tuple[1]
		return 1 
	except IOError as err:
		print 'File error: ', str(err)
		return 0
	except KeyError as kerr:
		print 'Key error: ', str(kerr)
		return 0
	finally:
		shelv_out.close()

def main():
	'''测试用'''
	(field, base) = read_from()  
	for each in field:
		for eeach in each:
			print eeach.type
		print

	for each in base[0]:
		print each.position
	for each in base[1]:
		print each.position
	raw_input("press anything to continue")
if __name__ == '__main__':
	main()

