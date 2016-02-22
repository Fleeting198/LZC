#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 02-09 Built
# 02-11 将数据处理交给controlls，日期查询筛选
# 02-12 acperiod, income
# 02-16 Implementing dateRangePicker. Saved lots of code.
# 02-20 acvalid, accategory

from app import app
from flask import render_template, request, jsonify
from app.models import *
from app.forms import *

from sqlalchemy import and_, func
from datetime import datetime
import json
import types

import LocalStrings as lstr


@app.route('/')
def show_index():
    return render_template('index.html')


@app.route('/charts')
def show_charts():
    return render_template('charts.html')


@app.route('/charts/expenditure')
def show_chart_expenditure():
    form = Form_UserDaterangemode()
    return render_template('chart-expenditure.html', form=form)


@app.route('/charts/expenditure/getData', methods=['GET'])
def refresh_chart_expenditure():

    # 从GET获得表单值赋给wtform
    form = Form_UserDaterangemode()
    form.userID.data = request.args.get('userID')
    form.modeDate.data = request.args.get('modeDate')
    form.dateRange.data = request.args.get('dateRange')

    if form.validate():
        userID = form.userID.data
        modeDate = int(form.modeDate.data)
        startDate = form.dateRange.data[:10]
        endDate = form.dateRange.data[-10:]

        # Query.
        strQuery = db.session.query(consumption.con_datetime,consumption.amount).filter(
            consumption.user_id == userID).order_by(consumption.con_datetime)
        if len(startDate) != 0:
            strQuery = strQuery.filter(
                and_(consumption.con_datetime >= startDate, consumption.con_datetime <= endDate))
        results = strQuery.all()

        # Get columns.
        res_datetimes = [result.con_datetime for result in results]
        res_amounts = [result.amount for result in results]

        from app.controls.DateTimeValueProcess import DateTimeValueProcess
        process = DateTimeValueProcess(res_datetimes, res_amounts)

        # Get and pack dateTrend() return.
        axisLables, accumulatedVals, pointVals = process.dateTrend(modeDate)
        json_dateTrend = {'axisLables': axisLables, 'accumulatedVals': accumulatedVals, 'pointVals': pointVals}
        # json_dateTrend = jsonify(axisLables=axisLables, accumulatedVals=accumulatedVals, pointVals=pointVals)

        # Get and pack timeDistribution() return.
        axisLables, vals = process.timeDistribution()
        json_timeDistribution = {'axisLables': axisLables, 'vals':vals}
        # json_timeDistribution = jsonify(axisLables=axisLables, vals=vals)

        # 没有错误就不传errMsg。前端通过检查errMsg是否存在来判断查询是否成功。
        json_response = jsonify(json_dateTrend=json_dateTrend, json_timeDistribution=json_timeDistribution)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/acperiod')
def show_chart_acperiod():
    form = Form_UserDaterange()
    return render_template('chart-acperiod.html', form=form)


@app.route('/charts/acperiod/getData', methods=['GET'])
def refresh_chart_acperiod():
    form = Form_UserDaterange()
    form.userID.data = request.args.get('userID')
    form.dateRange.data = request.args.get('dateRange')

    if form.validate():
        userID = form.userID.data
        startDate = form.dateRange.data[:10]
        endDate = form.dateRange.data[-10:]

        # Query.
        strQuery = db.session.query(acrec.ac_datetime).filter(acrec.user_id == userID).order_by(acrec.ac_datetime)
        if len(startDate) != 0:
            strQuery = strQuery.filter(and_(acrec.ac_datetime >= startDate, acrec.ac_datetime <= endDate))
        results = strQuery.all()
        res_datetimes = [result.ac_datetime for result in results]

        # Process data.
        from app.controls.DateTimeValueProcess import DateTimeValueProcess
        process = DateTimeValueProcess(res_datetimes)

        # 包装dateTrend 返回值。
        # 这个功能暂时不需要连续值，但还是必须获取，逻辑模块写一起了。
        axisLables, accumulatedVals, pointVals = process.dateTrend(2)  # 暂时将日期模式直接设为月

        json_dateTrend = {'axisLables': axisLables, 'pointVals': pointVals}

        # timeDistribution 返回值
        axisLables, vals = process.timeDistribution()
        json_timeDistribution = {'axisLables': axisLables, 'vals': vals}

        json_response = jsonify(json_dateTrend=json_dateTrend, json_timeDistribution=json_timeDistribution)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/income')
def show_chart_income():
    form = Form_DevDaterangemode()
    return render_template('chart-income.html', form=form)


@app.route('/charts/income/getData', methods=['GET'])
def refresh_chart_income():
    # 从GET获得表单值赋给wtform
    form = Form_DevDaterangemode()
    form.devID.data = request.args.get('devID')
    form.modeDate.data = request.args.get('modeDate')
    form.dateRange.data = request.args.get('dateRange')

    if form.validate():
        # 赋值给变量
        devID = form.devID.data
        modeDate = int(form.modeDate.data)
        startDate = form.dateRange.data[:10]
        endDate = form.dateRange.data[-10:]

        # Query.
        strQuery = db.session.query(consumption.con_datetime,consumption.amount).filter(
            consumption.dev_id == devID).order_by(consumption.con_datetime)
        if len(startDate) != 0:
            strQuery = strQuery.filter(
                and_(consumption.con_datetime >= startDate, consumption.con_datetime <= endDate))
        results = strQuery.all()
        # Get columns.
        res_datetimes = [result.con_datetime for result in results]
        res_amounts = [result.amount for result in results]

        # Process data.
        from app.controls.DateTimeValueProcess import DateTimeValueProcess
        process = DateTimeValueProcess(res_datetimes, res_amounts)

        # Get and pack dateTrend() return.
        axisLables, accumulatedVals, pointVals = process.dateTrend(modeDate)
        json_dateTrend = {'axisLables': axisLables, 'accumulatedVals': accumulatedVals, 'pointVals': pointVals}

        # Get and pack timeDistribution() return.
        axisLables, vals = process.timeDistribution()
        json_timeDistribution = {'axisLables': axisLables, 'vals': vals}

        # 没有错误就不传errMsg
        json_response = jsonify(json_dateTrend=json_dateTrend, json_timeDistribution=json_timeDistribution)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/acvalid')
def show_chart_acvalid():
    form = Form_UserDaterange()
    return render_template('chart-acvalid.html', form=form)


@app.route('/charts/acvalid/getData')
def refresh_chart_acvalid():
    form = Form_UserDaterange()
    form.userID.data = request.args.get('userID')
    form.dateRange.data = request.args.get('dateRange')

    if form.validate():
        userID = form.userID.data
        startDate = form.dateRange.data[:10]
        endDate = form.dateRange.data[-10:]

        # Query.
        strQuery = db.session.query(acrec.legal, func.count('*')).filter(acrec.user_id == userID).group_by(acrec.legal)
        if len(startDate) != 0:
            strQuery = strQuery.filter(and_(acrec.ac_datetime >= startDate, acrec.ac_datetime <= endDate))
        results = strQuery.all()

        # Process data.
        from controls.CategoryProcess import CategoryProcess
        titles, seriesData = CategoryProcess(results)

        json_response = {'titles': titles, 'seriesData': seriesData}
        json_response = jsonify(json_response)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/accategory')
def show_chart_accategory():
    form = Form_UserDaterange()
    return render_template('chart-accategory.html', form=form)


@app.route('/charts/accategory/getData')
def refresh_chart_accategory():
    form = Form_UserDaterange()
    form.userID.data = request.args.get('userID')
    form.dateRange.data = request.args.get('dateRange')

    if form.validate():
        userID = form.userID.data
        startDate = form.dateRange.data[:10]
        endDate = form.dateRange.data[-10:]

        # Query.
        strQuery = db.session.query(ac_loc.category, func.count('*')).filter(
            and_(ac_loc.node_des==acrec.node_des, acrec.user_id==userID)).group_by(ac_loc.category)
        if len(startDate) != 0:
            strQuery = strQuery.filter(and_(acrec.ac_datetime >= startDate, acrec.ac_datetime <= endDate))
        results = strQuery.all()

        # Process data.
        from controls.CategoryProcess import CategoryProcess
        titles, seriesData = CategoryProcess(results)

        json_response = {'titles': titles, 'seriesData': seriesData}
        json_response = jsonify(json_response)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/concategory')
def show_chart_concategory():
    form = Form_UserDaterange()
    return render_template('chart-concategory.html', form=form)


@app.route('/charts/concategory/getData')
def refresh_chart_concategory():
    form = Form_UserDaterange()
    form.userID.data = request.args.get('userID')
    form.dateRange.data = request.args.get('dateRange')

    if form.validate():
        userID = form.userID.data
        startDate = form.dateRange.data[:10]
        endDate = form.dateRange.data[-10:]

        # Query.
        strQuery = db.session.query(dev_loc.category, func.sum(consumption.amount)).filter(
            and_(consumption.user_id == userID, dev_loc.node_id == device.node_id, device.dev_id == consumption.dev_id)).group_by(dev_loc.category)
        if len(startDate) != 0:
            strQuery = strQuery.filter(and_(consumption.con_datetime >= startDate, consumption.con_datetime <= endDate))

        results = strQuery.all()

        # Process data.
        from controls.CategoryProcess import CategoryProcess
        titles, seriesData = CategoryProcess(results)

        json_response = {'titles': titles, 'seriesData': seriesData}
        json_response = jsonify(json_response)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/number')
def show_chart_number():
    return render_template('chart-number.html')


@app.route('/charts/number/getData', methods=['GET'])
def refresh_chart_number():
    # 查询
    strQuery = db.session.query(individual.role, func.count('*')).group_by(individual.role)
    results = strQuery.all()

    json_number = {}
    for result in results:
        json_number[result[0]] = result[1]

    json_number['teacher']=json_number.pop(u'老师')
    json_number['other']=json_number.pop(u'其他')
    json_number['stu1']=json_number.pop(u'本科生')
    json_number['stu2']=json_number.pop(u'研究生')
    json_number['stu3']=json_number.pop(u'博士生')

    json_response = jsonify(json_number)
    return json_response

#
# @app.route('/charts/acdatetime')
# def show_chart_expenditure():
#     form = Form_expenditure()
#     return render_template('chart-expenditure.html', form=form)
#
#
# @app.route('/charts/acdatetime/getData', methods=['GET'])
# def refresh_chart_expenditure():
#     form = Form_expenditure()
#     form.userID.data = request.args.get('userID')
#     form.modeDate.data = request.args.get('modeDate')
#     form.dateRange.data = request.args.get('dateRange')
#
#     if form.validate():
#         userID = form.userID.data
#         modeDate = int(form.modeDate.data)
#         startDate = form.dateRange.data[:10]
#         endDate = form.dateRange.data[-10:]
#
#         # Query.
#         strQuery = db.session.query(consumption.con_datetime, consumption.amount).filter(
#             consumption.user_id == userID).order_by(consumption.con_datetime)
#         if len(startDate) != 0:
#             strQuery = strQuery.filter(and_(consumption.con_datetime >= startDate, consumption.con_datetime <= endDate))
#         results = strQuery.all()
#
#         # Get columns.
#         res_datetimes = [result.con_datetime for result in results]
#         res_amounts = [result.amount for result in results]
#
#         from app.controls.DateTimeValueProcess import DateTimeValueProcess
#         process = DateTimeValueProcess(res_datetimes, res_amounts)
#
#         # Get and pack dateTrend() return.
#         axisLables, accumulatedVals, pointVals = process.dateTrend(modeDate)
#         json_dateTrend = {'axisLables': axisLables, 'accumulatedVals': accumulatedVals, 'pointVals': pointVals}
#         # json_dateTrend = jsonify(axisLables=axisLables, accumulatedVals=accumulatedVals, pointVals=pointVals)
#
#         # Get and pack timeDistribution() return.
#         axisLables, vals = process.timeDistribution()
#         json_timeDistribution = {'axisLables': axisLables, 'vals': vals}
#         # json_timeDistribution = jsonify(axisLables=axisLables, vals=vals)
#
#         # 没有错误就不传errMsg。前端通过检查errMsg是否存在来判断查询是否成功。
#         json_response = jsonify(json_dateTrend=json_dateTrend, json_timeDistribution=json_timeDistribution)
#     else:
#         json_response = jsonify(errMsg=form.errors)
#     return json_response
#
