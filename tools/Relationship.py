#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import MySQL

'''
计算人际关系，效率太低，完全不可行。
'''

def relationshipA(target="PPNWPQQW"):
	dbconfig = {'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'passwd': 'root', 'db': 'witcampus',
                'charset': 'utf8'}  # 数据库连接配置信息
	t1 = 30
	t2 = 30
	b = 10

	mysql1 = MySQL.MySQL(dbconfig)
	mysql2 = MySQL.MySQL(dbconfig)
	friends = {}
	sql = "select node_des,datetime from acrec where user_id='%s' " % target
	num_res1 = mysql1.query(sql)

	for row in mysql1.fetchAllRows():
		sql = "select user_id from acrec where timestampdiff(second,datetime,'%s')<30 and timestampdiff(second,datetime,'%s')>-30 and node_des = '%s'" % (row[1],row[1],row[0])
		num_res2 = mysql2.query(sql)
		for row2 in mysql2.fetchAllRows():
			if row2[0] in friends.keys():
				friends[row2[0]] += 1
			else:
				friends[row2[0]] = 1

	for key, value in friends:
		if value > b:
			print key

if __name__ == '__main__':
	relationshipA()
