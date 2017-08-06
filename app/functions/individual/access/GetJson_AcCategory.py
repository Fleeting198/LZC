#!/usr/bin/env python
# coding: UTF-8

from app.models import db, ac_loc, acrec
from sqlalchemy import and_, func

"""门禁类型次数比例"""


def GetJson_AcCategory(userID, startDate, endDate):
    dbQuery = db.session.query(ac_loc.category, func.count('*')).filter(
        and_(ac_loc.node_id == acrec.node_id, acrec.user_id == userID)).group_by(ac_loc.category)
    if startDate:
        dbQuery = dbQuery.filter(and_(acrec.ac_datetime >= startDate, acrec.ac_datetime <= endDate))
    results = dbQuery.all()

    if not results:
        return {'errMsg': u'没有找到记录。'}

    # Process data
    from app.functions.Pro_Cate import CategoryProcess
    vals = CategoryProcess(results)

    # 转换到Echarts的格式
    # seriesData = []  # [{value: , name: }, {value: , name: }, ...]
    seriesData = []
    for k, v in vals.items():
        seriesData.append({'value': int(v), 'name': k})
    # 按降序排序供前端输出，但是数据处理的时候已经有序了
    # seriesData = sorted(seriesData, cmp_dictVN,reverse=True)

    json_response = {'seriesData': seriesData}
    return json_response
