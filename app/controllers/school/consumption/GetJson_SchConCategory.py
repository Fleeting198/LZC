#!/usr/bin/env python
# coding: utf-8

from app.models import *
from sqlalchemy import func

"""学校全部消费类型比例，消费额比例不是刷卡机比例"""


def GetJson_SchAcCategory():
    strQuery = db.session.query(dev_loc.category, func.count('*')).group_by(dev_loc.category)

    results = strQuery.all()

    if not results:
        return {'errMsg': u'没有找到记录。'}

    # Process data
    from app.controllers.Pro_Cate import CategoryProcess
    vals = CategoryProcess(results, fold=False)

    # 转换到Echarts的格式
    # seriesData = []  # [{value: , name: }, {value: , name: }, ...]
    titles = vals.keys()
    seriesData = []
    for k, v in vals.iteritems():
        seriesData.append({'value': int(v), 'name': k})
    # 按降序排序供前端输出，但是数据处理的时候已经有序了
    seriesData = sorted(seriesData, cmp_dictVN, reverse=True)

    json_response = {'titles': titles, 'seriesData': seriesData}
    return json_response


def cmp_dictVN(d1, d2):
    if d1['value'] < d2['value']:
        return -1
    if d1['value'] > d2['value']:
        return 1
    return 0
