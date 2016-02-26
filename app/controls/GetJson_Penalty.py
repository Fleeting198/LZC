#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *

def GetJson_Penalty(userID):
    # query
    strQuery = db.session.query(penalty.amount).filter(penalty.user_id == userID)
    strQueryLine = db.session.query(penalty_line.amount, penalty_line.num).order_by(penalty_line.amount)
    results = strQuery.first()
    resultsLine = strQueryLine.all()

    # unpacking results
    userAmount = results[0]

    # process conability for all
    amount = [result.amount for result in resultsLine]
    num = [result.num for result in resultsLine]

    # return
    json_userAmount = {'userAmount': str(userAmount)}
    json_penalty = {'amount': amount, 'num': num}
    json_response = {'json_userAmount':json_userAmount, 'json_penalty':json_penalty}

    return json_response