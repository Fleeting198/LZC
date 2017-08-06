#!/usr/bin/env python
# coding: utf-8

from app.models import db,ac_loc
from sqlalchemy import func
from functools import cmp_to_key

"""学校全部门禁类型次数比例"""


def GetJson_SchAcCategory():
    sql = "select category, count from sch_ac_category"
    results = db.session.execute(sql).fetchall()

    dataList = []  # 为了方便用python排序，用列表
    for result in results:
        category = str(result[0])
        count = int(result[1])
        dataList.append({'name': category, 'count': count})

    # 按amount属性排序
    def _cmp(a, b):
        if a['count'] < b['count']:
            return -1
        elif a['count'] > b['count']:
            return 1
        else:
            return 0

    from functools import cmp_to_key
    dataList = sorted(dataList, key=cmp_to_key(_cmp), reverse=True)

    json_response = {'data': dataList}
    return json_response
