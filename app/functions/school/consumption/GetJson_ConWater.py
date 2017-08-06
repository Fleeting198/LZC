#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import db, con_water_7d, con_water_12m, con_water_24h


def GetJson_ConWater(modeTime):
    # 一天24小时
    if modeTime == 0:
        dbQuery = db.session.query(con_water_24h.sum_amount).order_by(con_water_24h.id)
        axisLabels = []
        for i in range(24):
            axisLabels.append(u'%d~%d点' % (i, i + 1))
    # 一周七天
    elif modeTime == 1:
        axisLabels = [u'周一', u'周二', u'周三', u'周四', u'周五', u'周六', u'周日', ]
        dbQuery = db.session.query(con_water_7d.sum_amount).order_by(con_water_7d.id)
    # 一年十二月
    elif modeTime == 2:
        axisLabels = [u'一月', u'二月', u'三月', u'四月', u'五月', u'六月', u'七月', u'八月', u'九月', u'十月', u'十一月', u'十二月', ]
        dbQuery = db.session.query(con_water_12m.sum_amount).order_by(con_water_12m.id)
    else:
        return {'errMsg': '时间选项超出范围'}

    results = dbQuery.all()

    vals = [float(result.sum_amount) for result in results]
    json_response = {'axisLabels': axisLabels, 'vals': vals}

    return json_response
