#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *
from sqlalchemy import and_


def GetJson_Penalty(userID):
    # query
    dbQuery = db.session.query(consumption.amount).filter(
        and_(consumption.dev_id == device.dev_id, device.node_id == dev_loc.node_id, dev_loc.category == "discipline",
             consumption.user_id == userID))
    dbQueryLine = db.session.query(penalty_line.amount, penalty_line.num).order_by(penalty_line.amount)
    result = dbQuery.first()
    resultsLine = dbQueryLine.all()

    if result is not None:
        # unpacking results
        userAmount = float(result[0])
    else:
        return {'errMsg': u'没有找到记录。'}

    # process conability for all
    amount = [float(result.amount) for result in resultsLine]
    num = [int(result.num) for result in resultsLine]

    # return
    json_response = {'userAmount': userAmount, 'amount': amount, 'num': num}

    return json_response
