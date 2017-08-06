# !/usr/bin/env python
# coding: UTF-8

from app.models import *
from numpy import array
from sqlalchemy import and_
from time import time

"""消费能力和学习努力之间的关系"""


def GetJson_StudyAndConAbility(userID):
    max_limit = 2000  # 处理样本点数量上限
    dbQuery = db.session.query(con_statistics, ac_study).filter(
        con_statistics.user_id == ac_study.user_id)
    resultUsers = dbQuery.all()

    valList = []
    timeList = []
    studyList = []

    # 读取数据到列表
    limitCount = 0
    for result in resultUsers:
        studyCount = result.ac_study.count_study()
        # studyCount = int(result.count_acad + result.count_sci + result.count_lib)
        studyList.append(studyCount)

        # 筛选过后计数
        limitCount += 1
        if limitCount > max_limit:  break

        val = float(result.con_statistics.total_vals)
        times = int(result.con_statistics.total_times)

        valList.append(val)
        timeList.append(times)

    # 将平均月消费额作为消费能力指标
    indexList = [val / 12.0 for val in valList]

    # 获取异常值上下范围
    from app.helpers import IQRHighLowLimit
    lLimCon, hLimCon = IQRHighLowLimit(indexList)
    lLimStu, hLimStu = IQRHighLowLimit(studyList)

    # 对正常范围内数据进行处理
    usersList = []
    for i in range(len(indexList)):
        if indexList[i] < lLimCon or indexList[i] > hLimCon: continue
        if studyList[i] < lLimStu or studyList[i] > hLimStu: continue
        usersList.append((indexList[i], studyList[i]))

    # users聚类 耗时最大
    k = 4
    users = array(usersList)
    from tools.Kmeans import kmeansProcess
    centroids, labels = kmeansProcess(users[:, :2], k)  # users是三维的，只取前两维聚类

    # 包装聚类结果
    clusterList = []
    for i in range(len(centroids)):
        if centroids[i][0] == -1: continue  # 跳过空簇
        usersi = list(users[labels == i])
        points = [list(user) for user in usersi]
        clusterList.append({'centroid': list(centroids[i]), 'points': points})

    # ============================
    dbQuery = db.session.query(con_statistics, ac_study).filter(and_(
        con_statistics.user_id == userID, con_statistics.user_id == ac_study.user_id))
    targetUser = dbQuery.first()

    if not targetUser:
        return {'errMsg': u'没有找到记录。'}
    # 处理查询对象数据
    val = float(targetUser.con_statistics.total_vals)

    studyCount = targetUser.ac_study.count_study()
    # studyCount = targetUser.count_acad + targetUser.count_sci + targetUser.count_lib
    conIndex = val / 12.0
    targetUser = {'name': userID, 'value': [conIndex, studyCount]}

    # =================
    json_response = {'users': clusterList, 'targetUser': targetUser}
    return json_response
