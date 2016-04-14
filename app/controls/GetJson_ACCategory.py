#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *
from sqlalchemy import and_, func

def GetJson_ACCategory(userID, startDate, endDate):
    # Query.
    strQuery = db.session.query(ac_loc.category, func.count('*')).filter(
        and_(ac_loc.node_id==acrec.node_id, acrec.user_id==userID)).group_by(ac_loc.category)
    if len(startDate) != 0:
        strQuery = strQuery.filter(and_(acrec.ac_datetime >= startDate, acrec.ac_datetime <= endDate))
    results = strQuery.all()
    if len(results) == 0:
        return {'errMsg': u'没有找到记录。'}

    # Process data.
    from CategoryProcess import CategoryProcess
    titles, vals = CategoryProcess(results)

    # seriesData = []  # [{value: , name: }, {value: , name: }, ...]
    # From tmp_data to seriesData.
    seriesData = []
    for k, v in vals.iteritems():
        seriesData.append({'value': int(v), 'name': k})

    seriesData = sorted(seriesData, cmp_dictVN)[::-1]

    json_response = {'titles': titles, 'seriesData': seriesData}
    return json_response


def cmp_dictVN(d1, d2):
    if d1['value'] < d2['value']:
        return -1
    if d1['value'] > d2['value']:
        return 1
    return 0
