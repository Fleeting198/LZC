#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import codecs
import csv

import MySQL

"""
依赖 兔大侠和他的朋友们 的 对MySQLdb常用函数进行封装的类 MySQL.py

示例：

自定义数据库配置和文件路径

import CSV2MySQL

csv = CSV2MySQL.Cvs2MySQL()

csv.acl2mysqlfile1()
csv.acl2mysqlfile2()
csv.consumption2mysql()
csv.device2MySQL()

"""


class Cvs2MySQL:
    _mysql = None
    path_device = "csv/device.csv"
    path_acl1 = "csv/acl1.csv"
    path_acl2 = "csv/acl2.csv"
    path_consumption = "csv/consumption.csv"
    num_oncecommit = 10000

    def __init__(self):
        """
        初始化 MySql 连接
        """
        self._mysql = MySQL.MySQL()

    def device2MySQL(self):
        """
        录入消费地点对应表 device
        """
        print "开始录入消费地点对应表"
        with codecs.open(self.path_device) as csvfile:
            reader = csv.reader(csvfile)
            reader.next()
            for ID, LOCATION, DEVID in reader:
                # Insert
                strsql = "insert into device(location, dev_id) values('" + LOCATION + "','" + DEVID + "')"
                self._mysql.insert(strsql)
        print "消费地点对应表录入完成"

    def acl2mysqlfile1(self):
        """
        录入门禁表1，以及个体表
        """
        print "开始录入门禁表1"
        sql_acrec = """insert ignore into acrec(user_id,ac_datetime,node_des,legal) values(%s,%s,%s,%s);"""
        sql_individual = """insert ignore into individual(user_id,role,grade) values(%s,%s,%s);"""

        with codecs.open(self.path_acl1) as csvfile:
            reader = csv.reader(csvfile)
            reader.next()  # Jump first line.

            list_acrec = []
            list_individual = []
            count = 0

            for USERACCESSNUMBER, ACCESSTIME, NODEDSC, LEGAL, ROLE, GRADE in reader:
                LEGAL = 1 if LEGAL == '合法卡' else 0  # legal 合法卡1 非法卡0
                # Insert
                data_acrec = (USERACCESSNUMBER, ACCESSTIME, NODEDSC, LEGAL)
                list_acrec.append(data_acrec)

                date_individual = (USERACCESSNUMBER, ROLE, GRADE)
                list_individual.append(date_individual)
                count += 1

                # 满num_oncecommit 提交一次
                if count / self.num_oncecommit == 1:
                    self._mysql._cur.executemany(sql_acrec, list_acrec)
                    self._mysql._cur.executemany(sql_individual, list_individual)

                    self._mysql.commit()
                    count = 0
                    list_acrec = []
            # 最后提交
            self._mysql._cur.executemany(sql_acrec, list_acrec)
            self._mysql._cur.executemany(sql_individual, list_individual)

            self._mysql.commit()

        print "门禁表一及其中个体录入完成。"

    ''''''
    def acl2mysqlfile2(self):
        """
        录入门禁数据2
        和入门禁数据1相比就是把文件名换一下而已
        """
        print "开始录入门禁表2"

        sql_acrec = """insert ignore into acrec(user_id,ac_datetime,node_des,legal) values(%s,%s,%s,%s);"""
        sql_individual = """insert ignore into individual(user_id,role,grade) values(%s,%s,%s);"""

        with codecs.open(self.path_acl2) as csvfile:
            reader = csv.reader(csvfile)
            reader.next()  # Jump first line.

            list_acrec = []
            list_individual = []
            count = 0

            for USERACCESSNUMBER, ACCESSTIME, NODEDSC, LEGAL, ROLE, GRADE in reader:
                LEGAL = 1 if LEGAL == '合法卡' else 0  # legal 合法卡1 非法卡0
                # Insert
                data_acrec = (USERACCESSNUMBER, ACCESSTIME, NODEDSC, LEGAL)
                list_acrec.append(data_acrec)

                date_individual = (USERACCESSNUMBER, ROLE, GRADE)
                list_individual.append(date_individual)
                count += 1

                # 满num_oncecommit 提交一次
                if count / self.num_oncecommit == 1:
                    self._mysql._cur.executemany(sql_acrec, list_acrec)
                    self._mysql._cur.executemany(sql_individual, list_individual)

                    self._mysql.commit()
                    count = 0
                    list_acrec = []
            # 最后提交
            self._mysql._cur.executemany(sql_acrec, list_acrec)
            self._mysql._cur.executemany(sql_individual, list_individual)

            self._mysql.commit()

        print "门禁表二录入完成。"

    def consumption2mysql(self):
        """
        录入消费数据
        """
        print "开始录入消费表"
        with codecs.open(self.path_consumption) as csvfile:
            reader = csv.reader(csvfile)
            reader.next()  # Jump first line.
            strsql = """insert ignore into consumption(user_id,dev_id,con_datetime,amount) values(%s,%s,%s,%s);"""
            list_data = []
            count = 0

            for STUEMPNO, TRANSDATE, TRANSTIME, DEVPHYID, AMOUNT, ROLE, GRADE in reader:

                # 合并TRANSDATE,TRANSTIME "YYYY-mm-dd hh:mm:ss"
                TRANSDATE = TRANSDATE[:6] + '-' + TRANSDATE[6:]
                TRANSDATE = TRANSDATE[:4] + '-' + TRANSDATE[4:]
                TRANSTIME = TRANSTIME[:4] + ':' + TRANSTIME[4:]
                TRANSTIME = TRANSTIME[:2] + ':' + TRANSTIME[2:]
                DATETIME = TRANSDATE + ' ' + TRANSTIME

                data = (STUEMPNO, DEVPHYID, DATETIME, AMOUNT)
                list_data.append(data)
                count += 1

                # 满num_oncecommit 提交一次
                if count / self.num_oncecommit == 1:
                    self._mysql._cur.executemany(strsql, list_data)
                    self._mysql.commit()
                    count = 0
                    list_data = []
            # 最后提交
            self._mysql._cur.executemany(strsql, list_data)
            self._mysql.commit()

        print "消费表录入完成"
