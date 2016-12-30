#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *
from sqlalchemy import and_, func

def GetJson_ACValid(userID, startDate, endDate):
    # Query.
    strQuery = db.session.query(acrec.legal, func.count('*')).filter(acrec.user_id == userID).group_by(acrec.legal)
    if len(startDate) != 0:
        strQuery = strQuery.filter(and_(acrec.ac_datetime >= startDate, acrec.ac_datetime <= endDate))
    results = strQuery.all()

    # Process data.
    from ProCate import CategoryProcess
    titles, vals = CategoryProcess(results)

    # seriesData = []  # [{value: , name: }, {value: , name: }, ...]
    seriesData = []
    for k, v in vals.iteritems():
        seriesData.append({'value': v, 'name': k})

    json_response = {'titles': titles, 'seriesData': seriesData}
    return json_response