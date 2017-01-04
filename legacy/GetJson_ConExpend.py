#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *
from sqlalchemy import and_

def GetJson_expenditure(userID, modeDate, modeTime, startDate, endDate):
    strQuery = db.session.query(consumption.con_datetime,consumption.amount).filter(
        consumption.user_id == userID).order_by(consumption.con_datetime)

    if startDate:
        strQuery = strQuery.filter(
            and_(consumption.con_datetime >= startDate, consumption.con_datetime <= endDate))

    results = strQuery.all()

    if not results:
        return {'errMsg': u'没有找到记录。'}

    # Get columns
    res_datetimes = [result.con_datetime for result in results]
    res_amounts = [result.amount for result in results]

    from app.controls.ProDateTimeValue import DateTimeValueProcess
    process = DateTimeValueProcess(res_datetimes, res_amounts)


    axisLabels, vals = process.get_time_distribution(modeTime)
    json_response = {'axisLabels': axisLabels, 'vals':vals}
    return json_response
