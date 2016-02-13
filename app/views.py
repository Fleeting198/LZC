# coding:utf-8
# 02-09 Built by 陈骏杰
#   expenditure
# 02-11 将数据处理交给dataProcess中脚本，日期查询筛选
# 02-12 acperiod, income

from app import app
from flask import render_template, request, jsonify
from app.models import *
from app.forms import *

from sqlalchemy import and_
from datetime import datetime

@app.route('/')
def show_index():
    return render_template('index.html')


@app.route('/charts')
def show_charts():
    return render_template('charts.html')


@app.route('/charts/expenditure')
def show_chart_expenditure():
    form = form_expenditure()
    return render_template('chart-expenditure.html', form=form)


@app.route('/charts/expenditure/getData', methods=['GET'])
def refresh_chart_expenditure():
    form = form_expenditure()
    json_response = jsonify(valid=0)

    print form.errors

    if form.validate():
        user_id = form.user_id
        mode_date = form.mode_date
        startDate = form.startDate
        endDate = form.endDate

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
        from app.controlls import expenditure
        mdates, mamounts, mamounts_point = expenditure.main(mdates, mamounts, mode_date)

        # 构造返回json
        json_response = jsonify(valid=1, mdates=mdates, mamounts=mamounts, mamounts_point=mamounts_point)

    return json_response


@app.route('/charts/acperiod')
def show_chart_acperiod():
    return render_template('chart-acperiod.html')


@app.route('/charts/acperiod/refresh', methods=['GET'])
def refresh_chart_acperiod():
    json_response = jsonify(valid=0)

    user_id = request.args.get('user_id')
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')

    if not (user_id and len(user_id) == 8):
        return json_response

    recordQuery = acrec.query.filter(acrec.user_id == user_id).order_by(acrec.ac_datetime)

    if len(startDate) != 0 and len(endDate) != 0 and (
        datetime.strptime(startDate, "%Y-%m-%d") > datetime.strptime(endDate, "%Y-%m-%d")):
        recordQuery = recordQuery.filter(
            and_(acrec.ac_datetime >= startDate, acrec.ac_datetime <= endDate))
    elif len(startDate) != 0 and len(endDate) == 0:
        recordQuery = recordQuery.filter(acrec.ac_datetime >= startDate)
    elif len(startDate) == 0 and len(endDate) != 0:
        recordQuery = recordQuery.filter(acrec.ac_datetime <= endDate)

    results = recordQuery.all()

    mdates = [result.ac_datetime for result in results]

    from app.controlls import acperiod
    mperiods, mcounts = acperiod.main(mdates)

    # 构造返回json
    json_response = jsonify(valid=1, mperiods=mperiods, mcounts=mcounts)

    return json_response


@app.route('/charts/income')
def show_chart_income():
    return render_template('chart-income.html')


@app.route('/charts/income/refresh', methods=['GET'])
def refresh_chart_income():

    dev_id = request.args.get('dev_id')
    mode_date = int(request.args.get('mode_date'))  # 日期模式：周、月、季、年
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')

    json_response = jsonify(valid=0)

    if not dev_id:
        return json_response

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
    from app.controlls import income
    mdates, mamounts, mamounts_point = income.main(mdates, mamounts, mode_date)

    mdates = map(lambda x: str(x), mdates)
    mamounts = map(lambda x: float(x), mamounts)
    mamounts_point = map(lambda x: float(x), mamounts_point)

    # 构造返回json
    json_response = jsonify(valid=1, mdates=mdates, mamounts=mamounts, mamounts_point=mamounts_point)

    return json_response