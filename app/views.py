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
import types


@app.route('/')
def show_index():
    return render_template('index.html')


@app.route('/summary')
def show_summary():

    # 最近一月 distinct门禁地点名数
    # 门禁地点数
    # 地点类型比重第二高的 accategory
    json_accategory = refresh_chart_accategory()



    # 最近一个月
    # 时间分布 6点~7点宿舍打卡
    # 23点到5点打卡

    # 图书，最近一个月图书馆次数，教学楼次数，需要教学楼二级分类？

    # 好友 —— 等待好友结果

    # 账单： 最近一月：
    # 消费类型比例 concategory, conablilty, expenditure

    # 滞纳金：penalty

    return render_template('summarization.html',data=data)


@app.route('/charts')
def show_charts():
    return render_template('charts.html')


@app.route('/charts/expenditure')
def show_chart_expenditure():
    form = Form_User_DR_MD_MT()
    return render_template('chart-expenditure.html', form=form)


@app.route('/charts/expenditure/getData', methods=['GET'])
def refresh_chart_expenditure():
    form = Form_User_DR_MD_MT()
    form.userID.data = request.args.get('userID')
    form.modeDate.data = request.args.get('modeDate')
    form.modeTime.data = request.args.get('modeTime')
    form.dateRange.data = request.args.get('dateRange')

    if form.validate():
        userID = form.userID.data
        modeDate = int(form.modeDate.data)
        modeTime = int(form.modeTime.data)
        startDate = form.dateRange.data[:10]
        endDate = form.dateRange.data[-10:]

        from controls.GetJson_expenditure import GetJson_expenditure
        json_response = GetJson_expenditure(userID,modeDate,modeTime,startDate,endDate)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


# @app.route('/charts/acperiod')
# def show_chart_acperiod():
#     form = Form_User_DR_MD()
#     return render_template('chart-acperiod.html', form=form)


# @app.route('/charts/acperiod/getData', methods=['GET'])
# def refresh_chart_acperiod():
#     form = Form_User_DR_MD()
#     form.userID.data = request.args.get('userID')
#     form.dateRange.data = request.args.get('dateRange')
#     form.modeDate.data = request.args.get('modeDate')
#
#     if form.validate():
#         userID = form.userID.data
#         startDate = form.dateRange.data[:10]
#         endDate = form.dateRange.data[-10:]
#         modeDate = int(form.modeDate.data)
#
#         # Query.
#         strQuery = db.session.query(acrec.ac_datetime).filter(acrec.user_id == userID).order_by(acrec.ac_datetime)
#         if len(startDate) != 0:
#             strQuery = strQuery.filter(and_(acrec.ac_datetime >= startDate, acrec.ac_datetime <= endDate))
#         results = strQuery.all()
#         res_datetimes = [result.ac_datetime for result in results]
#
#         # Process data.
#         from app.controls.DateTimeValueProcess import DateTimeValueProcess
#         process = DateTimeValueProcess(res_datetimes)
#
#         # 包装dateTrend 返回值。
#         # 这个功能暂时不需要连续值，但还是必须获取，逻辑模块写一起了。
#         axisLabels, accumulatedVals, pointVals = process.get_date_trend(modeDate)
#
#         json_dateTrend = {'axisLabels': axisLabels, 'pointVals': pointVals}
#
#         # timeDistribution 返回值
#         axisLabels, vals = process.get_time_distribution()
#         json_timeDistribution = {'axisLabels': axisLabels, 'vals': vals}
#
#         json_response = jsonify(json_dateTrend=json_dateTrend, json_timeDistribution=json_timeDistribution)
#     else:
#         json_response = jsonify(errMsg=form.errors)
#     return json_response


@app.route('/charts/acperiodcate')
def show_chart_acperiodcate():
    form = Form_User_DR_MD()
    return render_template('chart-acperiodcate.html', form=form)


@app.route('/charts/acperiodcate/getData', methods=['GET'])
def refresh_chart_acperiodcate():
    """
    门禁分类日期趋势时间分布    -C
    Codes mainly in controls.ACPeriodCate.py.
    """
    form = Form_User_DR_MD()
    form.userID.data = request.args.get('userID')
    form.dateRange.data = request.args.get('dateRange')
    form.modeDate.data = request.args.get('modeDate')

    if form.validate():
        userID = form.userID.data
        startDate = form.dateRange.data[:10]
        endDate = form.dateRange.data[-10:]
        modeDate = int(form.modeDate.data)

        from controls.GetJson_ACPeriodCate import GetJson_ACPeriodCate
        json_response = GetJson_ACPeriodCate(userID,modeDate,startDate,endDate)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/income')
def show_chart_income():
    form = Form_Dev_DR_MD_MT()
    return render_template('chart-income.html', form=form)


@app.route('/charts/income/getData', methods=['GET'])
def refresh_chart_income():
    form = Form_Dev_DR_MD_MT()
    form.devID.data = request.args.get('devID')
    form.modeDate.data = request.args.get('modeDate')
    form.modeTime.data = request.args.get('modeTime')
    form.dateRange.data = request.args.get('dateRange')

    if form.validate():
        devID = form.devID.data
        modeDate = int(form.modeDate.data)
        modeTime = int(form.modeTime.data)
        startDate = form.dateRange.data[:10]
        endDate = form.dateRange.data[-10:]

        from controls.GetJson_Income import GetJson_Income
        json_response = GetJson_Income(devID,modeDate, modeTime, startDate, endDate)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/foodIncome')
def show_chart_foodIncome():
    form = Form_MT()
    return render_template('chart-foodIncome.html', form=form)


@app.route('/charts/foodIncome/getData', methods=['GET'])
def refresh_chart_foodIncome():
    """
    获得设备地点表中分类为“餐饮”的地点的设备的金额总数。
    """
    form = Form_MT()
    form.modeTime.data = request.args.get('modeTime')

    if form.validate():
        modeTime = int(form.modeTime.data)

        from controls.GetJson_IncomeFood import GetJson_IncomeFood
        json_response = GetJson_IncomeFood(modeTime)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/acvalid')
def show_chart_acvalid():
    form = Form_User_DR()
    return render_template('chart-acvalid.html', form=form)


@app.route('/charts/acvalid/getData')
def refresh_chart_acvalid():
    form = Form_User_DR()
    form.userID.data = request.args.get('userID')
    form.dateRange.data = request.args.get('dateRange')

    if form.validate():
        userID = form.userID.data
        startDate = form.dateRange.data[:10]
        endDate = form.dateRange.data[-10:]

        from controls.GetJson_ACValid import GetJson_ACValid
        json_response = GetJson_ACValid(userID, startDate, endDate)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/accategory')
def show_chart_accategory():
    form = Form_User_DR()
    return render_template('chart-accategory.html', form=form)


@app.route('/charts/accategory/getData')
def refresh_chart_accategory():
    form = Form_User_DR()
    form.userID.data = request.args.get('userID')
    form.dateRange.data = request.args.get('dateRange')

    if form.validate():
        userID = form.userID.data
        startDate = form.dateRange.data[:10]
        endDate = form.dateRange.data[-10:]

        from controls.GetJson_ACCategory import GetJson_ACCategory
        json_response = GetJson_ACCategory(userID, startDate, endDate)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/concategory')
def show_chart_concategory():
    form = Form_User_DR()
    return render_template('chart-concategory.html', form=form)


@app.route('/charts/concategory/getData')
def refresh_chart_concategory():
    form = Form_User_DR()
    form.userID.data = request.args.get('userID')
    form.dateRange.data = request.args.get('dateRange')

    if form.validate():
        userID = form.userID.data
        startDate = form.dateRange.data[:10]
        endDate = form.dateRange.data[-10:]

        from controls.GetJson_ConCategory import GetJson_ConCategory
        json_response = GetJson_ConCategory(userID, startDate, endDate)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/number')
def show_chart_number():
    # return render_template('chart-number.html')
    return render_template('chart-numberBar.html')


@app.route('/charts/number/getData', methods=['GET'])
def refresh_chart_number():
    # query number of people by dividing into total & grades
    strQueryTotal = db.session.query(individual.role, func.count('*')).group_by(individual.role)
    # GradeB stands for 本科生的年级
    strQueryGradeB = db.session.query(individual.grade, func.count('*')).filter(individual.role == u'本科生').group_by(individual.grade)
    # GradePg stands for 研究生的年级
    strQueryGradePg = db.session.query(individual.grade, func.count('*')).filter(individual.role == u'研究生').group_by(individual.grade)
    # GradeDr stands for 博士生的年级
    strQueryGradeDr = db.session.query(individual.grade, func.count('*')).filter(individual.role == u'博士生').group_by(individual.grade)

    # go
    resultsTotal = strQueryTotal.all()
    resultsGradeB = strQueryGradeB.all()
    resultsGradePg = strQueryGradePg.all()
    resultsGradeDr = strQueryGradeDr.all()

    # process numberTotal
    json_numberTotal = {}
    for result in resultsTotal:
        json_numberTotal[result[0]] = result[1]

    json_numberTotal['teacher'] = json_numberTotal.pop(u'老师')
    json_numberTotal['other'] = json_numberTotal.pop(u'其他')
    json_numberTotal['stuB'] = json_numberTotal.pop(u'本科生')
    json_numberTotal['stuPg'] = json_numberTotal.pop(u'研究生')
    json_numberTotal['stuDr'] = json_numberTotal.pop(u'博士生')

    # process numberGrade
    grade = {'10', '11', '12', '13', '14', '15'}

    # init json
    json_numberGradeB = {'unknown': 0}
    json_numberGradePg = {'unknown': 0}
    json_numberGradeDr = {'unknown': 0}

    # func convert result to json
    def result_to_jsonUnicode(resultGrade):
        json = {'unknown': 0}
        for result in resultGrade:
            if result[0] in grade:
                json[result[0]] = result[1]
            else:
                json['unknown'] += result[1]
        return json

    # go
    json_numberGradeB = result_to_jsonUnicode(resultsGradeB)
    json_numberGradePg = result_to_jsonUnicode(resultsGradePg)
    json_numberGradeDr = result_to_jsonUnicode(resultsGradeDr)

    def result_to_jsonString(json):
        json['g10'] = json.pop(u'10')
        json['g11'] = json.pop(u'11')
        json['g12'] = json.pop(u'12')
        json['g13'] = json.pop(u'13')
        json['g14'] = json.pop(u'14')
        json['g15'] = json.pop(u'15')
        return json

    json_numberGradeB = result_to_jsonString(json_numberGradeB)
    json_numberGradePg = result_to_jsonString(json_numberGradePg)
    json_numberGradeDr = result_to_jsonString(json_numberGradeDr)

    # return
    json_response = jsonify(json_numberTotal = json_numberTotal, json_numberGradeB = json_numberGradeB, json_numberGradePg = json_numberGradePg, json_numberGradeDr = json_numberGradeDr)
    return json_response


@app.route('/charts/conwatertime')
def show_chart_conWaterTime():
    form = Form_DR_MD_MT()
    return render_template('chart-conwatertime.html', form=form)


@app.route('/charts/conwatertime/getData', methods=['GET'])
def refresh_chart_conWaterTime():
    form = Form_MT()
    form.modeTime.data = request.args.get('modeTime')

    if form.validate():
        modeTime = int(form.modeTime.data)  # 赋值给变量
        from controls.GetJson_ConWaterTime import GetJson_ConWaterTime
        json_response = GetJson_ConWaterTime(modeTime)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/conability')
def show_chart_conability():
    form = Form_User()
    return render_template('chart-conability.html', form=form)


@app.route('/charts/conability/getData', methods=['GET'])
def refresh_chart_conability():
    form = Form_User()
    form.userID.data = request.args.get('userID')

    if form.validate():
        userID = form.userID.data

        from controls.GetJson_ConAbility import GetJson_ConAbility
        json_response = GetJson_ConAbility(userID)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/conwater')
def show_chart_conwater():
    return render_template('chart-conwater.html')


@app.route('/charts/penalty')
def show_chart_penalty():
    form = Form_User()
    return render_template('chart-penalty.html', form=form)


@app.route('/charts/penalty/getData', methods=['GET'])
def refresh_chart_penalty():
    form = Form_User()
    form.userID.data = request.args.get('userID')

    if form.validate():
        userID = form.userID.data
        from controls.GetJson_Penalty import GetJson_Penalty
        json_response = GetJson_Penalty(userID)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response
