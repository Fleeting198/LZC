# coding:utf-8
from app import app
from flask import render_template, request, jsonify
from app.models import *

import json
# 在view中处理业务逻辑？

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

    # 获取参数
    user_id = request.args.get('user_id')
    # mode_date = request.args.get('mode_date')

    # 定义回传变量
    json_response = 0

    if user_id and len(user_id) == 8:  # 检查参数合法
        # 查询
        # print "Query:" + user_id
        results = consumption.query.filter(consumption.user_id==user_id).order_by(consumption.con_datetime).all()
        # print len(results)

        # 构造日期数组作为图表x轴标记
        mdates = [result.con_datetime for result in results]

        # 构造对应的消费值
        # data = [float(Decimal(result.amount).to_eng_string()) for result in results]
        mamounts = [float(result.amount) for result in results]

        # 构造返回json
        try:
            str_response = {"date": mdates, "data": mamounts}
            # json_response = jsonify(str_response)
            json_response = jsonify(mdates=mdates, mamounts=mamounts)
        except Exception,e:
            print e

    return json_response
