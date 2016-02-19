#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 02-09 Built -陈
# 02-11 将数据处理交给controlls，日期查询筛选
# 02-12 acperiod, income
# 02-16 Implementing dateRangePicker. Saved lots of code.

from app import app
from flask import render_template, request, jsonify
from app.models import *
from app.forms import *

from sqlalchemy import and_
from datetime import datetime
import json

import types


@app.route('/')
def show_index():
    return render_template('index.html')


# Ignore this.
@app.route('/test')
def show_test():
    return app.config['SQLALCHEMY_DATABASE_URI']


@app.route('/charts')
def show_charts():
    return render_template('charts.html')


@app.route('/charts/expenditure')
def show_chart_expenditure():
    form = form_expenditure()
    return render_template('chart-expenditure.html', form=form)


@app.route('/charts/expenditure/getData', methods=['GET'])
def refresh_chart_expenditure():

    # 从GET获得表单值赋给wtform
    form = form_expenditure()
    form.userID.data = request.args.get('userID')
    form.modeDate.data = request.args.get('modeDate')
    form.dateRange.data = request.args.get('dateRange')

    if form.validate():
        # 赋值给变量
        userID = form.userID.data
        modeDate = int(form.modeDate.data)
        startDate = form.dateRange.data[:10]
        endDate = form.dateRange.data[-10:]

        # 查询
        strQuery = consumption.query.filter(consumption.user_id == userID).order_by(consumption.con_datetime)

        if len(startDate) != 0 and len(endDate) != 0:
            strQuery = strQuery.filter(
                and_(consumption.con_datetime >= startDate, consumption.con_datetime <= endDate))
        elif len(startDate) != 0 and len(endDate) == 0:
            strQuery = strQuery.filter(consumption.con_datetime >= startDate)
        elif len(startDate) == 0 and len(endDate) != 0:
            strQuery = strQuery.filter(consumption.con_datetime <= endDate)

        results = strQuery.all()

        # 取出需要的列
        mdates = [result.con_datetime for result in results]
        mamounts = [result.amount for result in results]

        from app.controls.DataProcess import DateTimeValueProcess
        process = DateTimeValueProcess(mdates, mamounts)

        # 包装dateTrend 返回值
        axisLables, accumulatedVals, pointVals = process.dateTrend(modeDate)
        json_dateTrend = {'axisLables': axisLables, 'accumulatedVals': accumulatedVals, 'pointVals': pointVals}
        # json_dateTrend = jsonify(axisLables=axisLables, accumulatedVals=accumulatedVals, pointVals=pointVals)

        # timeDistribution 返回值
        axisLables, vals = process.timeDistribution()
        json_timeDistribution = {'axisLables': axisLables, 'vals':vals}
        # json_timeDistribution = jsonify(axisLables=axisLables, vals=vals)

        # 没有错误就不传errMsg
        json_response = jsonify(json_dateTrend=json_dateTrend, json_timeDistribution=json_timeDistribution)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/acperiod')
def show_chart_acperiod():
    form = form_acperiod()
    return render_template('chart-acperiod.html', form=form)


@app.route('/charts/acperiod/getData', methods=['GET'])
def refresh_chart_acperiod():
    form = form_acperiod()
    form.userID.data = request.args.get('userID')
    form.dateRange.data = request.args.get('dateRange')

    if form.validate():
        userID = form.userID.data
        startDate = form.dateRange.data[:10]
        endDate = form.dateRange.data[-10:]

        # 查询
        strQuery = acrec.query.filter(acrec.user_id == userID).order_by(acrec.ac_datetime)
        if len(startDate) != 0 and len(endDate) != 0:
            strQuery = strQuery.filter(and_(acrec.ac_datetime >= startDate, acrec.ac_datetime <= endDate))
        elif len(startDate) != 0 and len(endDate) == 0:
            strQuery = strQuery.filter(acrec.ac_datetime >= startDate)
        elif len(startDate) == 0 and len(endDate) != 0:
            strQuery = strQuery.filter(acrec.ac_datetime <= endDate)

        results = strQuery.all()

        mdates = [result.ac_datetime for result in results]

        from app.controls.DataProcess import DateTimeValueProcess
        process = DateTimeValueProcess(mdates)

        # 包装dateTrend 返回值
        axisLables, accumulatedVals, pointVals = process.dateTrend(2)  # 暂时将日期模式直接设为月
        # 没有记连续值的需要
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
    form = form_income()
    return render_template('chart-income.html', form=form)


@app.route('/charts/income/getData', methods=['GET'])
def refresh_chart_income():
    # 从GET获得表单值赋给wtform
    form = form_income()
    form.devID.data = request.args.get('devID')
    form.modeDate.data = request.args.get('modeDate')
    form.dateRange.data = request.args.get('dateRange')

    if form.validate():
        # 赋值给变量
        devID = form.devID.data
        modeDate = int(form.modeDate.data)
        startDate = form.dateRange.data[:10]
        endDate = form.dateRange.data[-10:]

        # 查询
        strQuery = consumption.query.filter(consumption.dev_id == devID).order_by(consumption.con_datetime)
        if len(startDate) != 0 and len(endDate) != 0:
            strQuery = strQuery.filter(
                and_(consumption.con_datetime >= startDate, consumption.con_datetime <= endDate))
        elif len(startDate) != 0 and len(endDate) == 0:
            strQuery = strQuery.filter(consumption.con_datetime >= startDate)
        elif len(startDate) == 0 and len(endDate) != 0:
            strQuery = strQuery.filter(consumption.con_datetime <= endDate)

        results = strQuery.all()

        # 取出需要的列
        mdates = [result.con_datetime for result in results]
        mamounts = [result.amount for result in results]

        from app.controls.DataProcess import DateTimeValueProcess
        process = DateTimeValueProcess(mdates, mamounts)

        # 包装dateTrend 返回值
        axisLables, accumulatedVals, pointVals = process.dateTrend(modeDate)
        json_dateTrend = {'axisLables': axisLables, 'accumulatedVals': accumulatedVals, 'pointVals': pointVals}

        # timeDistribution 返回值
        axisLables, vals = process.timeDistribution()
        json_timeDistribution = {'axisLables': axisLables, 'vals': vals}

        # 没有错误就不传errMsg
        json_response = jsonify(json_dateTrend=json_dateTrend, json_timeDistribution=json_timeDistribution)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response

@app.route('/charts/newChart')
def show_new():

    strQuery = consumption.query
    results = strQuery.all()
    print results

    return render_template('chart-test.html')
