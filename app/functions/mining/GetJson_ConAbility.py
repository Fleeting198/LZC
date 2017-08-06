#!/usr/bin/env python
# coding: UTF-8

from app.models import con_statistics, db
from numpy import array
from time import time

"""消费能力判定"""


def GetJson_ConAbility(userID):
    max_limit = 2000  # 处理样本点数量上限
    dbQuery = db.session.query(con_statistics.total_vals, con_statistics.total_times, con_statistics.per).limit(
        max_limit)
    results = dbQuery.all()

    # 所有数据处理
    # 读取数据到列表
    valsList = []
    timesList = []
    persList = []
    for result in results:
        valsList.append(float(result[0]))
        timesList.append(int(result[1]))
        persList.append(float(result[2]))

    # 获取异常值上下范围
    from app.helpers import IQRHighLowLimit
    # lLimVal, hLimVal = IQRHighLowLimit(valsList)
    # lLimTime, hLimTime = IQRHighLowLimit(timesList)
    lLimPer, hLimPer = IQRHighLowLimit(persList)

    # 对正常范围内数据进行处理
    users = []
    numberDict = {}
    lenSection = 10
    for i in range(len(valsList)):
        # if valsList[i] < lLimVal or valsList[i] > hLimVal: continue
        # if timesList[i] < lLimTime or timesList[i] > hLimTime: continue
        if persList[i] < lLimPer or persList[i] > hLimPer: continue
        # 消费能力散点图处理
        users.append([valsList[i], persList[i], timesList[i]])

        # 消费能力柱状图的数据处理，写进字典里
        key = int(valsList[i] / 12) / lenSection
        if key in numberDict:
            numberDict[key] += 1
        else:
            numberDict[key] = 1

    # users聚类
    k = 3
    users = array(users)
    from tools.Kmeans import kmeansProcess
    # 聚类过程耗时太长
    centroids, labels = kmeansProcess(users[:, :2], k)  # users是三维的，只取前两维聚类

    # 包装聚类结果
    clusterList = []
    for i in range(len(centroids)):
        if centroids[i][0] == -1: continue  # 跳过空簇
        usersi = list(users[labels == i])
        points = [list(user) for user in usersi]
        clusterList.append({'centroid': list(centroids[i]), 'points': points})

    # ========================
    dbQuery = db.session.query(con_statistics.total_vals, con_statistics.total_times, con_statistics.per).filter(
        con_statistics.user_id == userID)
    targetUser = dbQuery.first()

    if not targetUser:
        return {'errMsg': u'没有找到记录。'}

    # 被查询的目标个体
    val = float(targetUser[0])
    time = int(targetUser[1])
    per = float(targetUser[2])
    targetUser = {"name": userID, "value": (val, per, time)}

    scatterConAbility = {'users': clusterList, 'targetUser': targetUser}

    # =======================
    # 把柱状图的字典转为echarts的格式
    maxSectionLeft = max(list(numberDict.keys()))
    axisLabels = []
    vals = []

    intNumberDict = {}
    # 把字典的键转为整数，整合相同键的值，相加
    for k, v in numberDict.items():
        kInt = int(k)
        if kInt in intNumberDict:
            intNumberDict[kInt] += v
        else:
            intNumberDict[kInt] = v

    sum_amount = sum(intNumberDict.values())
    for i in range(int(maxSectionLeft) + 1):
        sectionLeft = i * lenSection
        axisLabels.append("%d~%d" % (sectionLeft, sectionLeft + lenSection))

        if i in intNumberDict.keys():
            vals.append(intNumberDict[i] / sum_amount * 100)
        else:
            vals.append(0)

    users = {"axisLabels": axisLabels, 'vals': vals}

    targetPerMonth = targetUser['value'][0] / 12
    targetPerMonthKey = int(targetPerMonth) / lenSection
    targetPeopleCount = numberDict[targetPerMonthKey]

    targetUser = {"targetPerMonthKey": targetPerMonthKey, 'numSection': targetPeopleCount}
    barConAbility = {"users": users, 'targetUser': targetUser}

    json_response = {'scatterConAbility': scatterConAbility, 'barConAbility': barConAbility}

    return json_response
