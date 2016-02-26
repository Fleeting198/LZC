#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import jsonify
from app.models import *

from sqlalchemy import and_, func


def GetJson_ConCategory(userID, startDate, endDate):
    # Query.
    strQuery = db.session.query(dev_loc.category, func.sum(consumption.amount)).filter(
        and_(consumption.user_id == userID, dev_loc.node_id == device.node_id,
             device.dev_id == consumption.dev_id)).group_by(dev_loc.category)
    if len(startDate) != 0:
        strQuery = strQuery.filter(and_(consumption.con_datetime >= startDate, consumption.con_datetime <= endDate))

    results = strQuery.all()

    # Process data.
    from CategoryProcess import CategoryProcess
    titles, seriesData = CategoryProcess(results)

    json_response = jsonify({'titles': titles, 'seriesData': seriesData})
    return json_response