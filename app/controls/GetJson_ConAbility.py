#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import jsonify
from app.models import *

def GetJson_ConAbility(userID):
    # search for user conability & role
    strQuery = db.session.query(conability.amount_avg, conability.role).filter(conability.user_id == userID)
    results = strQuery.first()

    # unpacking results
    userAmount, role = results

    strQueryLine = db.session.query(conability_line.amount_avg, conability_line.num).filter(
        conability_line.role == role).order_by(conability_line.amount_avg)
    resultsLine = strQueryLine.all()

    # process conability for all
    amount = [result.amount_avg for result in resultsLine]
    num = [result.num for result in resultsLine]

    # return
    json_userAmount = {'userAmount': str(userAmount)}
    json_conability = {'amount': amount, 'num': num}
    json_response = jsonify(json_userAmount=json_userAmount, json_conability=json_conability)

    return json_response