#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *

def GetJson_ACRelation(userID):

    list_relation = query_list_relation(userID)
    num_total = len(list_relation)

    # 获得最大关系值
    max_val = list_relation[0][1]

    source = str(userID)

    # symbolSize max and min
    max_size = 20       # For echarts 2.2.7
    min_size = 1

    # max_size = 30     # For echarts 3.1
    # min_size = 10

    # node 属性计算
    value_source = int(max_val * 1.2)
    symbolSize_source = (min_size * max_val - max_size + (max_size - min_size) * (max_val + 10)) / (max_val - 1)
    # 初始化节点和边队列
    nodes = [{'name': source, 'value': value_source, 'symbolSize':symbolSize_source/2 }]
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

    # 第一轮处理，与目标有直接关系的对象
    min_val = 2     # 最小关系值阈值
    max_concern = 25    # 这一轮最大进行处理的二级点数量
    for i in range(len(list_relation)):
        if i < max_concern:     # 数量限制

            # 取项的属性
            item = list_relation[i]
            k = item[0]; v = item[1]
            symbolSize_source = (min_size * max_val - max_size + (max_size - min_size) * v) / (max_val - 1)
            # Deprecated
            # # 对关系值大的一定数量个node 加默认显示的标签
            # if i < int(max_concern*0.5) and v > min_val:    # 默认显示标签的前 x% 个node并且关系值筛选。
            #     node = {'name': k, 'value': v,
            #             'label':{'normal':{'show':'false', 'position': 'right',
            #                                'formatter': '{b}', 'textStyle': {'color': '#000'}}},
            #             'symbolSize': (min_size * max_val - max_size + (max_size - min_size) * v) / (max_val - 1)}
            # else:
            #     node = {'name': k, 'value': v,
            #             'symbolSize': (min_size * max_val - max_size + (max_size - min_size) * v) / (max_val - 1)}

            node = {'name': k, 'value': v, 'symbolSize': symbolSize_source/2}
            nodes.append(node)

            link = {'source': index_of_name(source), 'target': index_of_name(k), 'weight': v}

            # link = {'source': index_of_name(source), 'target': index_of_name(k)}
            links.append(link)

    print 'Round1: count_nodes=%d, count_links=%d' % (len(nodes), len(links))
    # print nodes
    # print links
    print "======================="

    # 第二轮加边
    for j in range(1, len(nodes)):  # 遍历源目标外的点
        source = nodes[j]['name']   # 取名字
        list_relation = query_list_relation(source) # 查询
        max_concern = 7  # 最大进行处理的二级点数量

        for i in range(len(list_relation)):     # 遍历查询结果
            if i < max_concern:     # 处理数量限制
                # 取项的属性
                item = list_relation[i]
                k = item[0];  v = item[1]

                if v > min_val:     # 关系值筛选
                    idx_k = index_of_name(k)    # 取name 在nodes 中序号
                    if idx_k != -1:
                        link = {'source': i, 'target': idx_k, 'weight': (nodes[i]['value']+nodes[idx_k]['value'])/2.0 }

                        # link = {'source': i, 'target': idx_k}
                        links.append(link)

    print 'Round1: count_nodes=%d, count_links=%d' % (len(nodes), len(links))
    # print nodes
    # print links

    json_response = {'num_total': num_total, 'nodes': nodes, 'links': links}
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
