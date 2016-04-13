#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 02-09 Built
# 02-11 将数据处理交给controlls，日期查询筛选
# 02-12 acperiod, income
# 02-16 Implementing dateRangePicker. Saved lots of code.
# 02-20 acvalid, accategory

from app import app
from flask import render_template, request, jsonify, redirect
from app.models import *
from app.forms import *
from sqlalchemy import func
from app import helpers
import types


@app.route('/')
def show_index():
    return render_template('index.html')


@app.route('/check_user_id')
def show_check_user_id():
    userID = request.args.get('userID')
    strQuery = db.session.query(individual.user_id,individual.role,individual.grade).filter(individual.user_id==userID)
    return jsonify(has_user=True if len(strQuery.all())==1 else False)

def check_user_id(userID):
    strQuery = individual.query.filter(individual.user_id == userID)
    return True if len(strQuery.all()) == 1 else False

def check_dev_id(devID):
    strQuery = device.query.filter(devID = devID)
    return True if len(strQuery.all()) == 1 else False

# 访问 Summary 页面的默认工号
@app.route('/summary')
def show_summary_default():
    return redirect('/summary/PPPWQHXW')

# 按工号 user_id 获取信息，刷新页面
@app.route('/summary/<user_id>')
def show_summary(user_id):
    # Summary 页面用的默认工号及日期设定
    userID = str(user_id)
    startDate = ''
    endDate = ''

    from controls.GetJson_Summary import GetJson_Summary
    vals_summary = GetJson_Summary(user_id,startDate,endDate)

    return render_template('summarization/summarization.html', userID=userID, startDate=startDate, endDate=endDate, vals_summary=vals_summary)


@app.route('/charts')
def show_charts():
    return render_template('charts/charts.html')


@app.route('/charts/expenditure')
def show_chart_expenditure():
    form = Form_User_DR_MD_MT()
    return render_template('charts/chart-expenditure.html', form=form)


@app.route('/charts/expenditure/getData', methods=['GET'])
def refresh_chart_expenditure():
    form = Form_User_DR_MD_MT()
    form.userID.data = request.args.get('userID')
    form.modeDate.data = request.args.get('modeDate')
    form.modeTime.data = request.args.get('modeTime')
    form.dateRange.data = request.args.get('dateRange')

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])
    if not check_user_id(form.userID.data):
        return jsonify(errMsg=lstr.warn_userIDNon)

    userID = form.userID.data
    modeDate = int(form.modeDate.data)
    modeTime = int(form.modeTime.data)
    startDate = form.dateRange.data[:10]
    endDate = form.dateRange.data[-10:]

    from controls.GetJson_expenditure import GetJson_expenditure
    json_response = GetJson_expenditure(userID,modeDate,modeTime,startDate,endDate)
    return jsonify(json_response)


@app.route('/charts/acperiodcate')
def show_chart_acperiodcate():
    form = Form_User_DR_MD()
    return render_template('charts/chart-acperiodcate.html', form=form)


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

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])
    if not check_user_id(form.userID.data):
        return jsonify(errMsg=lstr.warn_userIDNon)

    userID = form.userID.data
    startDate = form.dateRange.data[:10]
    endDate = form.dateRange.data[-10:]
    modeDate = int(form.modeDate.data)

    from controls.GetJson_ACPeriodCate import GetJson_ACPeriodCate
    json_response = GetJson_ACPeriodCate(userID,modeDate,startDate,endDate)

    # ===========================
    # 解包，翻译，打包
    legendLabels = json_response['json_dateTrend']['legendLabels']
    seriesData = json_response['json_dateTrend']['seriesData']

    legendLabels = map(lambda x: helpers.translate(x), legendLabels)
    for datum in seriesData:
        datum['name'] = helpers.translate(datum['name'])

    json_response['json_dateTrend']['legendLabels'] = legendLabels
    json_response['json_dateTrend']['seriesData'] = seriesData

    legendLabels = json_response['json_timeDistribution']['legendLabels']
    seriesData = json_response['json_timeDistribution']['seriesData']

    legendLabels = map(lambda x: helpers.translate(x), legendLabels)
    for datum in seriesData:
        datum['name'] = helpers.translate(datum['name'])

    json_response['json_timeDistribution']['legendLabels'] = legendLabels
    json_response['json_timeDistribution']['seriesData'] = seriesData
    # ===========================

    return jsonify(json_response)


@app.route('/charts/income')
def show_chart_income():
    form = Form_Dev_DR_MD_MT()
    return render_template('charts/chart-income.html', form=form)


@app.route('/charts/income/getData', methods=['GET'])
def refresh_chart_income():
    form = Form_Dev_DR_MD_MT()
    form.devID.data = request.args.get('devID')
    form.modeDate.data = request.args.get('modeDate')
    form.modeTime.data = request.args.get('modeTime')
    form.dateRange.data = request.args.get('dateRange')

    if not form.validate():
        return jsonify(errMsg=form.errors['devID'])

    devID = form.devID.data
    modeDate = int(form.modeDate.data)
    modeTime = int(form.modeTime.data)
    startDate = form.dateRange.data[:10]
    endDate = form.dateRange.data[-10:]

    from controls.GetJson_Income import GetJson_Income
    json_response = GetJson_Income(devID,modeDate, modeTime, startDate, endDate)
    return jsonify(json_response)


@app.route('/charts/foodIncome')
def show_chart_foodIncome():
    form = Form_MT()
    return render_template('charts/chart-foodIncome.html', form=form)


@app.route('/charts/foodIncome/getData', methods=['GET'])
def refresh_chart_foodIncome():
    """
    获得设备地点表中分类为“餐饮”的地点的设备的金额总数。
    """
    form = Form_MT()
    form.modeTime.data = request.args.get('modeTime')

    if not form.validate():
        return jsonify(errMsg=form.errors)

    modeTime = int(form.modeTime.data)

    from controls.GetJson_IncomeFood import GetJson_IncomeFood
    json_response = GetJson_IncomeFood(modeTime)
    return jsonify(json_response)


@app.route('/charts/acvalid')
def show_chart_acvalid():
    form = Form_User_DR()
    return render_template('charts/chart-acvalid.html', form=form)


@app.route('/charts/acvalid/getData')
def refresh_chart_acvalid():
    form = Form_User_DR()
    form.userID.data = request.args.get('userID')
    form.dateRange.data = request.args.get('dateRange')

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])
    if not check_user_id(form.userID.data):
        return jsonify(errMsg=lstr.warn_userIDNon)

    userID = form.userID.data
    startDate = form.dateRange.data[:10]
    endDate = form.dateRange.data[-10:]

    from controls.GetJson_ACValid import GetJson_ACValid
    json_response = GetJson_ACValid(userID, startDate, endDate)

    # =======================
    titles = json_response['titles']
    seriesData = json_response['seriesData']

    titles = map(lambda x: helpers.translate(x), titles)
    for datum in seriesData:
        datum['name'] = helpers.translate(datum['name'])

    json_response['titles'] = titles
    json_response['seriesData'] = seriesData
    # =======================

    return jsonify(json_response)


@app.route('/charts/accategory')
def show_chart_accategory():
    form = Form_User_DR()
    return render_template('charts/chart-accategory.html', form=form)


@app.route('/charts/accategory/getData')
def refresh_chart_accategory():
    form = Form_User_DR()
    form.userID.data = request.args.get('userID')
    form.dateRange.data = request.args.get('dateRange')

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])
    if not check_user_id(form.userID.data):
        return jsonify(errMsg=lstr.warn_userIDNon)

    userID = form.userID.data
    startDate = form.dateRange.data[:10]
    endDate = form.dateRange.data[-10:]

    from controls.GetJson_ACCategory import GetJson_ACCategory

    json_response = GetJson_ACCategory(userID, startDate, endDate)

    # ==================
    titles = json_response['titles']
    seriesData = json_response['seriesData']

    for datum in seriesData:
        datum['name'] = helpers.translate(datum['name'])
    titles = [helpers.translate(title) for title in titles]

    json_response['titles'] = titles
    json_response['seriesData'] = seriesData
    # ==================

    return jsonify(json_response)


@app.route('/charts/concategory')
def show_chart_concategory():
    form = Form_User_DR()
    return render_template('charts/chart-concategory.html', form=form)


@app.route('/charts/concategory/getData')
def refresh_chart_concategory():
    form = Form_User_DR()
    form.userID.data = request.args.get('userID')
    form.dateRange.data = request.args.get('dateRange')

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])
    if not check_user_id(form.userID.data):
        return jsonify(errMsg=lstr.warn_userIDNon)

    userID = form.userID.data
    startDate = form.dateRange.data[:10]
    endDate = form.dateRange.data[-10:]

    from controls.GetJson_ConCategory import GetJson_ConCategory
    json_response = GetJson_ConCategory(userID, startDate, endDate)

    # ==================
    titles = json_response['titles']
    seriesData = json_response['seriesData']

    for datum in seriesData:
        datum['name'] = helpers.translate(datum['name'])
    titles = [helpers.translate(title) for title in titles]

    json_response['titles'] = titles
    json_response['seriesData'] = seriesData
    # ==================

    return jsonify(json_response)


@app.route('/charts/number')
def show_chart_number():
    # return render_template('charts/chart-number.html')
    return render_template('charts/chart-numberBar.html')


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
    json_response = jsonify(json_numberTotal = json_numberTotal, json_numberGradeB = json_numberGradeB,
                            json_numberGradePg = json_numberGradePg, json_numberGradeDr = json_numberGradeDr)
    return json_response


@app.route('/charts/conwatertime')
def show_chart_conWaterTime():
    form = Form_DR_MD_MT()
    return render_template('charts/chart-conwatertime.html', form=form)


@app.route('/charts/conwatertime/getData', methods=['GET'])
def refresh_chart_conWaterTime():
    form = Form_MT()
    form.modeTime.data = request.args.get('modeTime')

    if not form.validate():
        return jsonify(errMsg=form.errors)

    modeTime = int(form.modeTime.data)  # 赋值给变量
    from controls.GetJson_ConWaterTime import GetJson_ConWaterTime
    json_response = GetJson_ConWaterTime(modeTime)
    return jsonify(json_response)


@app.route('/charts/conability')
def show_chart_conability():
    form = Form_User()
    return render_template('charts/chart-conability.html', form=form)


@app.route('/charts/conability/getData', methods=['GET'])
def refresh_chart_conability():
    form = Form_User()
    form.userID.data = request.args.get('userID')

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])

    userID = form.userID.data

    from controls.GetJson_ConAbility import GetJson_ConAbility
    json_response = GetJson_ConAbility(userID)
    return jsonify(json_response)


@app.route('/charts/conwater')
def show_chart_conwater():
    return render_template('charts/chart-conwater.html')


@app.route('/charts/penalty')
def show_chart_penalty():
    form = Form_User()
    return render_template('charts/chart-penalty.html', form=form)


@app.route('/charts/penalty/getData', methods=['GET'])
def refresh_chart_penalty():
    form = Form_User()
    form.userID.data = request.args.get('userID')

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])

    userID = form.userID.data

    from controls.GetJson_Penalty import GetJson_Penalty
    json_response = GetJson_Penalty(userID)
    return jsonify(json_response)


@app.route('/charts/relation')
def show_chart_relation():
    form = Form_User()
    return render_template('charts/chart-relation.html', form=form)


@app.route('/charts/relation/getData', methods=['GET'])
def refresh_chart_relation():
    form = Form_User()
    form.userID.data = request.args.get('userID')

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])

    userID = form.userID.data
    from controls.GetJson_ACRelation import GetJson_ACRelation
    json_response = GetJson_ACRelation(userID)
    return jsonify(json_response)


# =====================================
# Summary 所用图表获取json返回的路由
# =====================================

@app.route('/summary/GetJson_penalty', methods=['GET'])
def refresh_summary_penalty():
    userID = request.args.get('userID')

    from controls.GetJson_Penalty import GetJson_Penalty
    json_response = GetJson_Penalty(userID)
    return jsonify(json_response)


@app.route('/summary/GetJson_accategory', methods=['GET'])
def refresh_summary_accategory():

    userID = request.args.get('userID')
    startDate = request.args.get('startDate')
    endDate = request.args.get('startDate')

    from controls.GetJson_ACCategory import GetJson_ACCategory
    json_response = GetJson_ACCategory(userID, startDate, endDate)

    if 'errMsg' not in json_response:
        titles = json_response['titles']
        seriesData = json_response['seriesData']

        for datum in seriesData:
            datum['name'] = helpers.translate(datum['name'])
        titles = [helpers.translate(title) for title in titles]

        json_response['titles'] = titles
        json_response['seriesData'] = seriesData

    return jsonify(json_response)


@app.route('/summary/GetJson_concategory', methods=['GET'])
def refresh_summary_concategory():

    userID = request.args.get('userID')
    startDate = request.args.get('startDate')
    endDate = request.args.get('startDate')

    from controls.GetJson_ConCategory import GetJson_ConCategory
    json_response = GetJson_ConCategory(userID, startDate, endDate)

    if 'errMsg' not in json_response:
        titles = json_response['titles']
        seriesData = json_response['seriesData']

        for datum in seriesData:
            datum['name'] = helpers.translate(datum['name'])
        titles = [helpers.translate(title) for title in titles]

        json_response['titles'] = titles
        json_response['seriesData'] = seriesData

    return jsonify(json_response)


@app.route('/summary/GetJson_acperiodcate', methods=['GET'])
def refresh_summary_acperiodcate():

    userID = request.args.get('userID')
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')

    modeDate = 2

    from controls.GetJson_ACPeriodCate import GetJson_ACPeriodCate
    json_response = GetJson_ACPeriodCate(userID, modeDate, startDate, endDate)

    if 'errMsg' not in json_response:
        # 解包，翻译，打包
        legendLabels = json_response['json_dateTrend']['legendLabels']
        seriesData = json_response['json_dateTrend']['seriesData']

        legendLabels = map(lambda x: helpers.translate(x), legendLabels)
        for datum in seriesData:
            datum['name'] = helpers.translate(datum['name'])

        json_response['json_dateTrend']['legendLabels'] = legendLabels
        json_response['json_dateTrend']['seriesData'] = seriesData

        legendLabels = json_response['json_timeDistribution']['legendLabels']
        seriesData = json_response['json_timeDistribution']['seriesData']

        legendLabels = map(lambda x: helpers.translate(x), legendLabels)
        for datum in seriesData:
            datum['name'] = helpers.translate(datum['name'])

        json_response['json_timeDistribution']['legendLabels'] = legendLabels
        json_response['json_timeDistribution']['seriesData'] = seriesData

    return jsonify(json_response)


@app.route('/summary/GetJson_relation', methods=['GET'])
def refresh_summary_relation():
    userID = request.args.get('userID')

    from controls.GetJson_ACRelation import GetJson_ACRelation
    json_response = GetJson_ACRelation(userID)
    return jsonify(json_response)

# =====================================
# Summary End
# =====================================
