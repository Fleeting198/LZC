# coding:utf-8
# 02-09 Built by 陈骏杰
# 02-11 将数据处理交给dataProcess中脚本，日期查询筛选 by C

from app import app
from flask import render_template, request, jsonify
from app.models import *

from sqlalchemy import and_


@app.route('/')
def index():
    return render_template('base.html')  # 模版路径名一定要写全


# 仅仅加载图表，json传递由js发起。
@app.route('/expenditure')
def chart_expenditure():
    return render_template('chart-expenditure.html')


# 传给前端的数据格式：
# 'data':[消费金额按时间顺序],
@app.route('/expenditure/refresh', methods=['GET'])
def refresh_expenditure():
    from datetime import datetime

    user_id = request.args.get('user_id')
    mode_date = int(request.args.get('mode_date'))  # 日期模式：周、月、季、年
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')

    # 定义回传变量
    json_response = 0

    if not(user_id and len(user_id) == 8):
        return json_response

    # 查询
    # 根据传入的起止日期组合4 种情况
    # 太长了啊能不能优化下
    if len(startDate) != 0 and len(endDate) != 0 and (datetime.strptime(startDate, "%Y-%m-%d") > datetime.strptime(endDate, "%Y-%m-%d")):
        results = Consumption.query.filter(
            and_(Consumption.user_id == user_id, Consumption.con_datetime >= startDate, Consumption.con_datetime <= endDate)).order_by(Consumption.con_datetime).all()
    elif len(startDate) != 0 and len(endDate) == 0:
        results = Consumption.query.filter(
            and_(Consumption.user_id == user_id, Consumption.con_datetime >= startDate)).order_by(Consumption.con_datetime).all()
    elif len(startDate) == 0 and len(endDate) != 0:
        results = Consumption.query.filter(
            and_(Consumption.user_id == user_id, Consumption.con_datetime <= endDate)).order_by(Consumption.con_datetime).all()
    else:
        results = Consumption.query.filter(Consumption.user_id == user_id).order_by(Consumption.con_datetime).all()

    mdates = [result.con_datetime for result in results]  # 构造日期数组作为图表x轴标记
    mamounts = [result.amount for result in results]   # 构造对应的消费值

    # 调用处理模块
    from app.dataProcess import expenditure
    mdates, mamounts, mamounts_point = expenditure.main(mdates, mamounts, mode_date)

    mdates = map(lambda x: str(x), mdates)
    mamounts = map(lambda x: float(x), mamounts)
    mamounts_point = map(lambda x: float(x), mamounts_point)

    # 构造返回json
    try:
        json_response = jsonify(mdates=mdates, mamounts=mamounts, mamounts_point=mamounts_point)
    except Exception,e:
        print e

    return json_response


@app.route('/acperiod')
def chart_acperiod():
    return render_template('chart-acperiod.html')


@app.route('/acperiod/refresh', methods=['GET'])
def refresh_acperiod():
    from datetime import datetime
    json_response = 0
    user_id = request.args.get('user_id')
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')

    if not (user_id and len(user_id) == 8):
        return json_response

    if len(startDate) != 0 and len(endDate) != 0 and (
        datetime.strptime(startDate, "%Y-%m-%d") > datetime.strptime(endDate, "%Y-%m-%d")):
        results = acrec.query.filter(and_(acrec.user_id == user_id, acrec.ac_datetime >= startDate, acrec.ac_datetime <= endDate)).order_by(
            acrec.ac_datetime).all()
    elif len(startDate) != 0 and len(endDate) == 0:
        results = acrec.query.filter(
            and_(acrec.user_id == user_id, acrec.ac_datetime >= startDate)).order_by(acrec.ac_datetime).all()
    elif len(startDate) == 0 and len(endDate) != 0:
        results = acrec.query.filter(
            and_(acrec.user_id == user_id, acrec.ac_datetime <= endDate)).order_by(acrec.ac_datetime).all()
    else:
        results = acrec.query.filter(acrec.user_id == user_id).all()

    mdates = [result.ac_datetime for result in results]

    from app.dataProcess import acperiod
    mperiods, mcounts = acperiod.main(mdates)

    # 构造返回json
    try:
        json_response = jsonify(mperiods=mperiods, mcounts=mcounts)
    except Exception, e:
        print e

    return json_response
