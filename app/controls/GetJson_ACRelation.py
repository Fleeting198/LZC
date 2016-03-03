#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *

def GetJson_ACRelation(userID):

    list_relation = query_list_relation(userID)

    # 获得最大关系值
    max_val = list_relation[0][1]

    source = str(userID)

    # symbolSize max and min
    max_size = 30
    min_size = 10

    # 初始化节点和边队列
    nodes = [{'name': source, 'value': int(max_val * 1.2),
              'symbolSize': (min_size * max_val - max_size + (max_size - min_size) * (max_val + 10)) / (max_val - 1)}]
    links = []

    # 在nodes 中返回key:name 为name 的元素序号，若无则返回-1
    def index_of_name(name):
        index = 0
        for node in nodes:
            if node['name'] == name:
                # print "返回了%s的序号%d" % (name,index)
                return index
            index += 1
        return -1

    max_concern = 50
    for i in range(len(list_relation)):
        if i < max_concern:
            item = list_relation[i]
            k = item[0]; v = item[1]
            node = {'name': k, 'value': v,
                    'symbolSize': (min_size * max_val - max_size + (max_size - min_size) * v) / (max_val - 1)}
            nodes.append(node)
            link = {'source': index_of_name(source), 'target': index_of_name(k)}
            links.append(link)

    print 'Round1: count_nodes=%d, count_links=%d' % (len(nodes), len(links))
    # print nodes
    # print links
    print "======================="

    # 第一轮完成，nodes确定，遍历所有nodes
    for j in range(1, len(nodes)):
        source = nodes[j]['name']
        list_relation = query_list_relation(source)
        max_concern = 10
        for i in range(len(list_relation)):
            if i < max_concern:
                item = list_relation[i]
                k = item[0]; # v = item[1]
                idx_k = index_of_name(k)
                if idx_k != -1:
                    link = {'source': i, 'target': idx_k}
                    links.append(link)

    print 'Round1: count_nodes=%d, count_links=%d' % (len(nodes), len(links))
    # print nodes
    # print links

    json_response = {'nodes': nodes, 'links': links}
    return json_response


def cmp_list_item(item1,item2):
    if item1[1] > item2[1]:
        return 1
    elif item1[1] < item2[1]:
        return -1
    else:
        return 0


# 查询表中人际关系，转为dict，转为list并排序。
def query_list_relation(userID):
    # Query
    strQuery = acr_friendlist.query.filter(acr_friendlist.user_id == userID)
    dict_relation = strQuery.first().str_relation_to_dict()

    # Stage 0 completed: dict_relation queried.
    # =======================


    # 删掉关系所有者在关系中的记录
    if userID in dict_relation:
        del dict_relation[userID]

    # Stage 1 completed: dict_relation without self inside.
    # =======================


    # 排序
    list_relation = []
    for k, v in dict_relation.iteritems():
        list_relation.append([k, int(v)])

    del dict_relation

    list_relation = sorted(list_relation, cmp_list_item)[::-1]

    # Stage 2 completed: sorted list_relation.
    # =======================

    return list_relation
