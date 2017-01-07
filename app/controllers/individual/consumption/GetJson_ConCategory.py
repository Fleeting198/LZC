#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *
from sqlalchemy import and_, func

"""消费类型金额比例"""


def GetJson_ConCategory(userID, startDate, endDate):
    # Query
    strQuery = db.session.query(dev_loc.category, func.sum(consumption.amount)).filter(
        and_(consumption.user_id == userID, dev_loc.node_id == device.node_id,
             device.dev_id == consumption.dev_id)).group_by(dev_loc.category)

    if startDate:
        strQuery = strQuery.filter(and_(consumption.con_datetime >= startDate, consumption.con_datetime <= endDate))

    results = strQuery.all()
    if not results:
        return {'errMsg': u'没有找到记录。'}

    # Process data
    from app.controllers.Pro_Cate import CategoryProcess
    vals = CategoryProcess(results)
    titles = vals.keys()

    # seriesData = []  # [{value: , name: }, {value: , name: }, ...]
    seriesData = []
    for k, v in vals.iteritems():
        seriesData.append({'value': v, 'name': k})

    seriesData = sorted(seriesData, cmp_dictVN, reverse=True)

    json_response = {'titles': titles, 'seriesData': seriesData}
    return json_response


def cmp_dictVN(d1, d2):
    if d1['value'] < d2['value']:
        return -1
    if d1['value'] > d2['value']:
        return 1
    return 0
