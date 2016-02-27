#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *

def GetJson_ConAbility(userID):
    # search for user conability & role
    strQuery = db.session.query(conability.amount_avg, conability.role).filter(conability.user_id == userID)
    results = strQuery.first()

    # unpacking results
    userAmount, role = results
    userAmount = float(userAmount)

    strQueryLine = db.session.query(conability_line.amount, conability_line.num).filter(
        conability_line.role == role).order_by(conability_line.amount)
    resultsLine = strQueryLine.all()

    # process conability for all
    amount = [float(result.amount) for result in resultsLine]
    num = [result.num for result in resultsLine]

    # return
    json_response = {'userAmount': userAmount, 'amount':amount, 'num': num}

    return json_response