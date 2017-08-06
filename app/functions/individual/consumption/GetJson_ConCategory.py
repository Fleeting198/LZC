#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *
from sqlalchemy import and_, func

"""消费类型金额比例"""


def GetJson_ConCategory(userID, startDate, endDate):
    dbQuery = db.session.query(dev_loc.category, func.sum(consumption.amount), func.count('*')).filter(
        and_(consumption.user_id == userID, dev_loc.node_id == device.node_id,
             device.dev_id == consumption.dev_id)).group_by(dev_loc.category)
    if startDate:
        dbQuery = dbQuery.filter(and_(consumption.con_datetime >= startDate, consumption.con_datetime <= endDate))
    results = dbQuery.all()
    if not results:
        return {'errMsg': u'没有找到记录。'}

    # Process data
    dataDict = {}
    for result in results:
        category = str(result[0])
        amount = float(result[1])
        count = int(result[2])
        dataDict[category] = {'amount': amount, 'count': count}

    json_response = {'dataDict': dataDict}
    return json_response
