#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import jsonify
from app.models import *

def GetJson_ConWaterTime(modeTime):
    # Query.
    if modeTime == 0:
        strQuery = db.session.query(con_food_24h.con_axis, con_food_24h.sum_amount).order_by(con_food_24h.con_axis)
        axisLabels = []
        for i in range(24):
            axisLabels.append(str((i + 1) % 24) + u'点')
    elif modeTime == 1:
        axisLabels = [u'周一', u'周二', u'周三', u'周四', u'周五', u'周六', u'周日', ]
        strQuery = db.session.query(con_food_7d.con_axis, con_food_7d.sum_amount).order_by(con_food_7d.con_axis)
    elif modeTime == 2:
        axisLabels = [u'一月', u'二月', u'三月', u'四月', u'五月', u'六月', u'七月', u'八月', u'九月', u'十月', u'十一月', u'十二月', ]
        strQuery = db.session.query(con_food_12m.con_axis, con_food_12m.sum_amount).order_by(
            con_food_12m.con_axis)
    results = strQuery.all()

    vals = [float(result.sum_amount) for result in results]

    json_timeDistribution = {'axisLabels': axisLabels, 'vals': vals}
    json_response = jsonify(json_timeDistribution=json_timeDistribution)

    return json_response