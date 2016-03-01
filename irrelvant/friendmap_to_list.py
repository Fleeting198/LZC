#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from MysqlClient import MysqlClient
import json, types, os, sys

# 选出acr_friendmap, con_friendmap 中数据处理
# dict 合并
# 重新写入数据库，key做一列，value dict做一列

class Friendmaps_to_list:

    def __init__(self):
        self.mc = MysqlClient()


    def query_map_to_dict(self, table_name):
        sys.stdout.write(u'开始查询表%s。\n' % table_name)
        sqlimit = 50    # 每次查询条数
        sqlstart = 0    # 每次查询开始条数，每次加sqlimit
        dict_all = {}

        table_rows = self.query_table_rows(table_name)

        while table_rows >= sqlstart:
            sql_select = "select v from %s limit %d,%d;" % (table_name, sqlstart, sqlimit)
            rs = self.mc.query(sql_select)

            for r in rs:
                print len(r[0])
                dict_loc = eval(r[0])
                for k, v in dict_loc.iteritems():
                    if k in dict_all:
                        # 合并个人关系字典
                        for k1, v1 in v.iteritems():
                            if k1 in dict_all[k]:
                                dict_all[k][k1] += v1
                            else:
                                dict_all[k][k1] = 1
                    else:
                        dict_all[k] = v
            sqlstart += sqlimit

        sys.stdout.write(u'返回结果字典。\n')
        sys.stdout.write(str(len(dict_all)))

        return dict_all


    def query_table_rows(self, table_name):
        sql_rows = "select count(*) from %s;" % (table_name)
        rs = self.mc.query(sql_rows)
        table_rows = rs[0][0]
        sys.stdout.write("Table %s has %d rows." % (table_name, table_rows))
        return table_rows


    def insert_to_list(self, dict_all, table_name):
        # 全部查询到后每个人的关系字典才具备完整性，才可以开始插入。
        # 问题是内存不足，dict_all 太大。
        # 对每一行原始记录，遍历每个个人字典，每个人工号去目标表中查询，若查询到已有的此人行，合并字典（MySQL并做不到?）
        # TODO: 消费表内存错误

        sys.stdout.write(u'开始插入到表%s。\n' % table_name)
        for k, v in dict_all.iteritems():
            v = str(v).replace("'", "\\'")
            sql_insert = "insert into %s(user_id, dict_relation) values('%s', '%s'); " % (table_name, k, v)
            self.mc.query(sql_insert)

        sys.stdout.write(u'表%s插入完成。\n' % table_name)


if __name__ == '__main__':

    list_maps = ['acr_friendmap', 'con_friendmap']
    list_lists = ['acr_friendlist', 'con_friendlist']

    instance = Friendmaps_to_list()

    # for i in (0, 1):
    #     dict_all = instance.query_map_to_dict(list_maps[i])
    #     instance.insert_to_list(dict_all, list_lists[i])

    dict_all = instance.query_map_to_dict(list_maps[1])
    instance.insert_to_list(dict_all, list_lists[1])
