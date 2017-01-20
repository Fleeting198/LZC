#!/usr/bin/env python
# coding: utf-8

from app.models import *

"""学校全部消费类型比例，消费额比例 和 刷卡机比例"""


def GetJson_SchConCategory():
    sql = "select category,amount,count from sch_con_category"
    results = db.session.execute(sql).fetchall()

    dataDict = {}
    for result in results:
        category = str(result[0])
        amount = float(result[1])
        count = int(result[2])
        dataDict[category] = {'amount': amount, 'count': count}

    json_response = {'titles': dataDict.keys(), 'data': dataDict}
    return json_response


def cmp_dictVN(d1, d2):
    if d1['value'] < d2['value']:
        return -1
    if d1['value'] > d2['value']:
        return 1
    return 0
