#!/usr/bin/env python
# coding: UTF-8

from app.models import *
from sqlalchemy import and_

"""贫困判定"""


def GetJson_PovertyJudge(userID):
    strQuery = db.session.query(individual.con_sum_vals, individual.con_sum_times)
    results = strQuery.all()

    strQuery = db.session.query(individual.con_sum_vals, individual.con_sum_times).filter(individual.user_id == userID)
    targetUser = strQuery.all()

    if not targetUser:
        return {'errMsg': u'没有找到记录。'}

    targetUser = targetUser[0]
    targetUser = {"name": userID, "value": (float(targetUser[0]), targetUser[1], float(targetUser[0]) / targetUser[1])}

    max_limit = 5000
    s = 0

    vals_times_list = []
    for result in results:
        if result[0] is not None:
            if s < max_limit:
                s += 1
                val = float(result[0])
                time = result[1]
                per = val / time
                if per > 20: continue
                vals_times_list.append((val, time, per))
            else:
                break

    json_response = {'vals_times_list': vals_times_list, 'targetUser': targetUser}
    return json_response
