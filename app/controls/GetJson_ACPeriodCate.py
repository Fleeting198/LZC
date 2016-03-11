#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *
from sqlalchemy import and_


def GetJson_ACPeriodCate(userID, modeDate, startDate, endDate):
    # Query.
    strQuery = db.session.query(acrec.ac_datetime, ac_loc.category).filter(
        and_(acrec.user_id == userID, acrec.node_id == ac_loc.node_id)).order_by(acrec.ac_datetime)
    if len(startDate) != 0:
        strQuery = strQuery.filter(and_(acrec.ac_datetime >= startDate, acrec.ac_datetime <= endDate))
    results = strQuery.all()

    res_datetimes = [result.ac_datetime for result in results]
    res_categorys = [result.category for result in results]

    from ACPeriodCate import ACPeriodCate
    json_dateTrend, json_timeDistribution = ACPeriodCate(res_datetimes, res_categorys, modeDate)

    # json_response = jsonify(json_dateTrend=json_dateTrend, json_timeDistribution=json_timeDistribution)
    json_response = {'json_dateTrend':json_dateTrend, 'json_timeDistribution':json_timeDistribution}

    return json_response
