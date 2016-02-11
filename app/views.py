# coding:utf-8
# 02-09 Built by 陈骏杰
# 02-11 将数据处理交给dataProcess中脚本 by 陈骏杰

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
def data_expenditure():

    from datetime import datetime

    # 获取参数
    user_id = request.args.get('user_id')   # 工号
    mode_date = int(request.args.get('mode_date'))  # 日期模式：周、月、季、年
    startDate = request.args.get('startDate')  # 起始时间
    endDate = request.args.get('endDate')   # 结束时间

    # 定义回传变量
    json_response = 0

    if user_id and len(user_id) == 8:  # 检查参数合法
        # 查询
        # print "Query:" + user_id
        # 根据传入的起止日期组合4 种情况
        if len(startDate) != 0 and len(endDate) != 0 and \
                (datetime.strptime(startDate, "%Y-%m-%d") > datetime.strptime(endDate, "%Y-%m-%d")):
            results = consumption.query.filter(
                and_(consumption.user_id == user_id, consumption.con_datetime >= startDate,
                     consumption.con_datetime <= endDate)).order_by(consumption.con_datetime).all()
        elif len(startDate) != 0 and len(endDate) == 0:
            results = consumption.query.filter(
                and_(consumption.user_id == user_id, consumption.con_datetime >= startDate))\
                .order_by(consumption.con_datetime).all()
        elif len(startDate) == 0 and len(endDate) != 0:
            results = consumption.query.filter(
                and_(consumption.user_id == user_id, consumption.con_datetime <= endDate))\
                .order_by(consumption.con_datetime).all()
        else:
            results = consumption.query.filter(consumption.user_id == user_id)\
                .order_by(consumption.con_datetime).all()

        mdates = [result.con_datetime for result in results]  # 构造日期数组作为图表x轴标记
        mamounts = [result.amount for result in results]   # 构造对应的消费值

        # 调用处理模块处理原始数据
        from app.dataProcess import expenditure
        mdates, mamounts = expenditure.main(mdates, mamounts, mode_date)

        mdates = map(lambda x: str(x), mdates)
        mamounts = map(lambda x: float(x), mamounts)

        # print mdates
        # print mamounts

        # 构造返回json
        try:
            json_response = jsonify(mdates=mdates, mamounts=mamounts)
        except Exception,e:
            print e

    return json_response
