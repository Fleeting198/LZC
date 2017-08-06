#!/usr/bin/env python
# coding: utf-8

from app.models import *

"""学校全部消费类型比例，消费额比例 和 刷卡机比例"""


def GetJson_SchConCategory():
    sql = "select category,amount,count from sch_con_category"
    results = db.session.execute(sql).fetchall()

    dataList = []  # 为了方便用python排序，用列表
    for result in results:
        category = str(result[0])
        amount = float(result[1])
        count = int(result[2])
        dataList.append({'name': category, 'amount': amount, 'count': count})

    # 按amount属性排序
    def _cmp(a, b):
        if a['amount'] < b['amount']:
            return -1
        elif a['amount'] > b['amount']:
            return 1
        else:
            return 0

    from functools import cmp_to_key
    dataList = sorted(dataList, key=cmp_to_key(_cmp), reverse=True)

    json_response = {'data': dataList}
    return json_response
