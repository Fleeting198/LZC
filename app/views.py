#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 02-09 Built -陈
# 02-11 将数据处理交给controlls，日期查询筛选
# 02-12 acperiod, income

from app import app
from flask import render_template, request, jsonify
from app.models import *
from app.forms import *

from sqlalchemy import and_
from datetime import datetime

import types


@app.route('/')
def show_index():
    return render_template('index.html')


# Ignore this.
@app.route('/test')
def show_test():
    # alpha = 'aaa'
    import json
    # alpha= jsonify(aaa=1)
    obj = {'aaa':1}
    alpha = json.dumps(obj)
    print alpha
    print type(alpha)
    return render_template('test.html', alpha=alpha )


@app.route('/charts')
def show_charts():
    return render_template('charts.html')


@app.route('/charts/expenditure')
def show_chart_expenditure():
    form = form_expenditure(request.form, csrf_enabled=False)
    return render_template('chart-expenditure.html', form=form)


@app.route('/charts/expenditure/getData', methods=['GET'])
def refresh_chart_expenditure():
    form = form_expenditure(request.form, csrf_enabled=False)
    json_response = jsonify(valid=0)

    if form.validate():
        # 获取表单传值
        user_id = form.user_id.data
        mode_date = int(request.args.get('mode_date'))
        startDate = '' if request.args.get('startDate')is None else str(request.args.get('startDate'))
        endDate = '' if request.args.get('endDate') is None else str(request.args.get('endDate'))

        # import types
        # print type(startDate)
        # print startDate

        # 未解决：form.startDate.data始终为None。form.mode_date.data始终为0.
        # startDate = '' if form.startDate.data is None else str(form.startDate.data)
        # endDate = '' if form.endDate.data is None else str(form.endDate.data)

        # 查询
        recordQuery = consumption.query.filter(consumption.user_id == user_id).order_by(consumption.con_datetime)

        if len(startDate) != 0 and len(endDate) != 0 and (
                    datetime.strptime(startDate, "%Y-%m-%d") > datetime.strptime(endDate, "%Y-%m-%d")):
            recordQuery = recordQuery.filter(
                and_(consumption.con_datetime >= startDate, consumption.con_datetime <= endDate))
        elif len(startDate) != 0 and len(endDate) == 0:
            recordQuery = recordQuery.filter(consumption.con_datetime >= startDate)
        elif len(startDate) == 0 and len(endDate) != 0:
            recordQuery = recordQuery.filter(consumption.con_datetime <= endDate)

        results = recordQuery.all()

        mdates = [result.con_datetime for result in results]  # 构造日期数组作为图表x轴标记
        mamounts = [result.amount for result in results]  # 构造对应的消费值

        # 调用处理模块
        from app.controls import expenditure
        mdates, mamounts, mamounts_point = expenditure.main(mdates, mamounts, mode_date)

        # 构造返回json
        json_response = jsonify(valid=1, mdates=mdates, mamounts=mamounts, mamounts_point=mamounts_point)
    else:
        print form.errors
    return json_response


@app.route('/charts/acperiod')
def show_chart_acperiod():
    form = form_acperiod(request.form, csrf_enabled=False)
    return render_template('chart-acperiod.html', form=form)


@app.route('/charts/acperiod/getData', methods=['GET'])
def refresh_chart_acperiod():
    form = form_acperiod(request.form, csrf_enabled=False)
    json_response = jsonify(valid=0)

    if form.validate():
        user_id = form.user_id.data
        startDate = '' if request.args.get('startDate') is None else str(request.args.get('startDate'))
        endDate = '' if request.args.get('endDate') is None else str(request.args.get('endDate'))

        recordQuery = acrec.query.filter(acrec.user_id == user_id).order_by(acrec.ac_datetime)
        if len(startDate) != 0 and len(endDate) != 0 and (
                    datetime.strptime(startDate, "%Y-%m-%d") > datetime.strptime(endDate, "%Y-%m-%d")):
            recordQuery = recordQuery.filter(and_(acrec.ac_datetime >= startDate, acrec.ac_datetime <= endDate))
        elif len(startDate) != 0 and len(endDate) == 0:
            recordQuery = recordQuery.filter(acrec.ac_datetime >= startDate)
        elif len(startDate) == 0 and len(endDate) != 0:
            recordQuery = recordQuery.filter(acrec.ac_datetime <= endDate)

        results = recordQuery.all()

        mdates = [result.ac_datetime for result in results]

        from app.controls import acperiod
        mperiods, mcounts = acperiod.main(mdates)

        # 构造返回json
        json_response = jsonify(valid=1, mperiods=mperiods, mcounts=mcounts)
    else:
        print form.errors

    return json_response


@app.route('/charts/income')
def show_chart_income():
    form = form_income(request.form, csrf_enabled=False)
    return render_template('chart-income.html', form=form)


@app.route('/charts/income/getData', methods=['GET'])
def refresh_chart_income():
    form = form_income(request.form, csrf_enabled=False)
    json_response = jsonify(valid=0)

    if form.validate():
        dev_id = form.dev_id.data
        mode_date = int(request.args.get('mode_date'))
        startDate = '' if request.args.get('startDate') is None else str(request.args.get('startDate'))
        endDate = '' if request.args.get('endDate') is None else str(request.args.get('endDate'))

        # 查询
        recordQuery = consumption.query.filter(consumption.dev_id == dev_id).order_by(consumption.con_datetime)
        if len(startDate) != 0 and len(endDate) != 0 and (
            datetime.strptime(startDate, "%Y-%m-%d") > datetime.strptime(endDate, "%Y-%m-%d")):
            recordQuery = recordQuery.filter(
                and_(consumption.con_datetime >= startDate, consumption.con_datetime <= endDate))
        elif len(startDate) != 0 and len(endDate) == 0:
            recordQuery = recordQuery.filter(consumption.con_datetime >= startDate)
        elif len(startDate) == 0 and len(endDate) != 0:
            recordQuery = recordQuery.filter(consumption.con_datetime <= endDate)

        results = recordQuery.all()

        mdates = [result.con_datetime for result in results]
        mamounts = [result.amount for result in results]

        # 调用处理模块
        from app.controls import income
        mdates, mamounts, mamounts_point = income.main(mdates, mamounts, mode_date)

        # 构造返回json
        json_response = jsonify(valid=1, mdates=mdates, mamounts=mamounts, mamounts_point=mamounts_point)
    else:
        print form.errors

    return json_response
