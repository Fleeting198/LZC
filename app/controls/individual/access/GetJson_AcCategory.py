#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *
from sqlalchemy import and_, func

"""门禁类型次数比例"""

def GetJson_AcCategory(userID, startDate, endDate):
    # Query
    strQuery = db.session.query(ac_loc.category, func.count('*')).filter(
        and_(ac_loc.node_id==acrec.node_id, acrec.user_id==userID)).group_by(ac_loc.category)

    if startDate:
        strQuery = strQuery.filter(and_(acrec.ac_datetime >= startDate, acrec.ac_datetime <= endDate))

    results = strQuery.all()

    if not results:
        return {'errMsg': u'没有找到记录。'}

    # Process data
    from app.controls.Pro_Cate import CategoryProcess
    vals = CategoryProcess(results)

    # 转换到Echarts的格式
    # seriesData = []  # [{value: , name: }, {value: , name: }, ...]
    titles = vals.keys()
    seriesData = []
    for k, v in vals.iteritems():
        seriesData.append({'value': int(v), 'name': k})
    # 按降序排序供前端输出，但是数据处理的时候已经有序了
    # seriesData = sorted(seriesData, cmp_dictVN,reverse=True)

    json_response = {'titles': titles, 'seriesData': seriesData}
    return json_response


def cmp_dictVN(d1, d2):
    if d1['value'] < d2['value']:
        return -1
    if d1['value'] > d2['value']:
        return 1
    return 0
