# coding:utf-8
from app import app
from app import db
from flask import render_template, request
from app.models import *
# 在view中处理业务逻辑？


@app.route('/')
def index():
    return render_template('base.html')  # 模版路径名一定要写全


# 传给前端的数据格式：
# 'data':[消费金额按时间顺序],
@app.route('/expenditure', methods=['GET'])
def chart_expenditure():
    # 获取参数
    user_id = request.args.get('user_id')
    if user_id and len(user_id) == 8:  # 检查参数合法
        # 查询
        print "Query:" + user_id
        # results = consumption.query.first()
        results = []
        results = db.session.query(consumption).filter_by(user_id=user_id).all()
        # results = consumption.query.filter_by(user_id=user_id).all()
        print results
        print len(results)
    else:
        pass
    return render_template('chart-expenditure.html')
