#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *
from sqlalchemy import and_

def GetJson_ACPeriodCate(userID, modeDate, startDate, endDate):
    """返回Json：门禁趋势与分布
    :param userID: 查询工号
    :param modeDate: 日期模式，合并到最短时间单位. 0-day, 1-week, 2-month, 3-Quarter. (default 2)
    :param startDate: 限定来源数据起始日期
    :param endDate: 限定来源数据结束日期
    """
    # Query.
    strQuery = db.session.query(acrec.ac_datetime, ac_loc.category).filter(
        and_(acrec.user_id == userID, acrec.node_id == ac_loc.node_id)).order_by(acrec.ac_datetime)

    if len(startDate) != 0:
        strQuery = strQuery.filter(and_(acrec.ac_datetime >= startDate, acrec.ac_datetime <= endDate))

    results = strQuery.all()
    if len(results) == 0:
        return {'errMsg': u'没有找到记录。'}

    res_datetimes = [result.ac_datetime for result in results]
    res_categorys = [result.category for result in results]

    from ProAcPeriodCate import ACPeriodCate
    process = ACPeriodCate(res_datetimes, res_categorys)
    json_dateTrend = process.get_date_trend(modeDate)
    json_timeDistribution = process.get_time_distribution()

    json_response = {'json_dateTrend':json_dateTrend, 'json_timeDistribution':json_timeDistribution}

    return json_response
