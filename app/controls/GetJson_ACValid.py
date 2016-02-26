#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import jsonify
from app.models import *
from sqlalchemy import and_, func

def GetJson_ACValid(userID, startDate, endDate):
    # Query.
    strQuery = db.session.query(acrec.legal, func.count('*')).filter(acrec.user_id == userID).group_by(acrec.legal)
    if len(startDate) != 0:
        strQuery = strQuery.filter(and_(acrec.ac_datetime >= startDate, acrec.ac_datetime <= endDate))
    results = strQuery.all()

    # Process data.
    from CategoryProcess import CategoryProcess
    titles, seriesData = CategoryProcess(results)

    json_response = jsonify({'titles': titles, 'seriesData': seriesData})
    return json_response