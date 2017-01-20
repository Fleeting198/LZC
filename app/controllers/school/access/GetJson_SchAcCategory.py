#!/usr/bin/env python
# coding: utf-8

from app.models import *
from sqlalchemy import func

"""学校全部门禁类型次数比例"""


def GetJson_SchAcCategory():
    strQuery = db.session.query(ac_loc.category, func.count('*')).group_by(ac_loc.category)
    results = strQuery.all()

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
