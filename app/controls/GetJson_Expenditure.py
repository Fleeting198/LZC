#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *
from sqlalchemy import and_

def GetJson_expenditure(userID, modeDate, modeTime, startDate, endDate):
    # Query.
    strQuery = db.session.query(consumption.con_datetime,consumption.amount).filter(
        consumption.user_id == userID).order_by(consumption.con_datetime)
    if len(startDate) != 0:
        strQuery = strQuery.filter(
            and_(consumption.con_datetime >= startDate, consumption.con_datetime <= endDate))
    results = strQuery.all()
    if len(results) == 0:
        return {'errMsg': u'没有找到记录。'}

    # Get columns.
    res_datetimes = [result.con_datetime for result in results]
    res_amounts = [result.amount for result in results]

    from app.controls.ProDateTimeValue import DateTimeValueProcess
    process = DateTimeValueProcess(res_datetimes, res_amounts)

    axisLabels, accumulatedVals, pointVals = process.get_date_trend(modeDate)
    json_dateTrend = {'axisLabels': axisLabels, 'accumulatedVals': accumulatedVals, 'pointVals': pointVals}

    axisLabels, vals = process.get_time_distribution(modeTime)
    json_timeDistribution = {'axisLabels': axisLabels, 'vals':vals}

    json_response = {'json_dateTrend':json_dateTrend, 'json_timeDistribution':json_timeDistribution}

    return json_response
