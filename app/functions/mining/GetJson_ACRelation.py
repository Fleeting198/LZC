#!/usr/bin/env python
# coding: UTF-8

from app.models import *
import pickle


def GetJson_ACRelation(userID):
    # 查询目标用户的关联
    dictRelation = query_relation(userID, isTarget=True)
    if 'errMsg' in dictRelation:
        return dictRelation

    # 前端ECharts用的点大小和连线值
    maxSymbolSize, minSymbolSize = 40, 10
    maxLinkValLimit, minLinkValLimit = 20, 3

    # 最大和最小的差
    diffSymbolSize = float(maxSymbolSize - minSymbolSize)
    diffLinkValLimit = float(maxLinkValLimit - minLinkValLimit)

    maxFirLevelNodes = 30  # 一级点添加数量上限
    countFirLevelNodes = 0  # 已添加点计数

    nodes, links = [], []  # 初始化点列表和线列表
    nodeTarget = {'name': userID, 'value': 1, 'symbolSize': maxSymbolSize + 10}  # 目标用户数据单独拿出来

    # 第一轮添加点
    newNodeList_name, newNodeList_suppCount, newNodeList_confRate = [], [], []
    for k, v in dictRelation.items():
        newNodeList_name.append(k)
        newNodeList_suppCount.append(v[0])
        newNodeList_confRate.append(v[1])

        countFirLevelNodes += 1
        if countFirLevelNodes == maxFirLevelNodes: break

    maxNodeVal, minNodeVal = max(newNodeList_confRate), min(newNodeList_confRate)
    diffNodeVal = float(maxNodeVal - minNodeVal)

    for i in range(len(newNodeList_name)):
        name = newNodeList_name[i]
        conf = newNodeList_confRate[i]
        suppCount = newNodeList_suppCount[i]
        # 加点
        symbolSize = diffSymbolSize * (conf - maxNodeVal) / diffNodeVal + maxSymbolSize
        node = {'name': name, 'value': 0, 'conf': conf, 'suppCount': suppCount, 'symbolSize': symbolSize}
        nodes.append(node)
        # 加边
        linkVal = diffLinkValLimit * (conf - maxNodeVal) / diffNodeVal + maxLinkValLimit
        link = {'source': str(userID), 'target': name, 'value': linkVal}
        links.append(link)

    # 第二轮加边
    def nameInNodes(name, nodes):
        for n in nodes:
            if name == n['name']: return True
        return False

    maxSecLevelNodes = 30  # 二级点添加数量上限
    countSecLevelNodes = 0

    newNodeList_name, newNodeList_suppCount = [], []
    for i in range(len(nodes)):
        userID = nodes[i]['name']
        dictRelation = query_relation(userID, isTarget=False)
        if len(dictRelation) == 0: continue

        breakFlag = False
        for k, v in dictRelation.items():
            if nameInNodes(k, nodes):
                newNodeList_name.append(k)
                newNodeList_suppCount.append(v[1])

                countSecLevelNodes += 1
                if countSecLevelNodes == maxSecLevelNodes:
                    breakFlag = True
                    break
        if breakFlag: break

    maxNodeVal = max(maxNodeVal, max(newNodeList_suppCount))
    minNodeVal = min(minNodeVal, min(newNodeList_suppCount))
    diffNodeVal = float(maxNodeVal - minNodeVal)

    for i in range(len(newNodeList_name)):
        k = newNodeList_name[i]
        v = newNodeList_suppCount[i]

        linkVal = diffLinkValLimit * (v - maxNodeVal) / diffNodeVal + maxLinkValLimit
        link = {'source': str(userID), 'target': k, 'value': linkVal}
        links.append(link)

    with open('ProjectPrefs.pkl', 'rb') as f:
        prefs = pickle.load(f)
        cntTransactions = prefs['cntTransactionsRelation']

    json_response = {'nodes': nodes, 'links': links, 'nodeTarget': nodeTarget, 'cntTransactions': cntTransactions}
    return json_response


def query_relation(userID, isTarget):
    dbQuery = ac_relation_confdata.query.filter(ac_relation_confdata.left_user_id == userID)
    results = dbQuery.all()

    if results is None or not results:
        if isTarget:
            return {'errMsg': u'没有找到记录。'}
        else:
            return {}

    dictRelation = {}
    for result in results:
        dictRelation[result.right_user_id] = (result.suppCount, result.confRate)

    return dictRelation
