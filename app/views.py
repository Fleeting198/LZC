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
from sqlalchemy import and_, func, distinct
import types
from pandas import Series, DataFrame
from app import helpers


@app.route('/')
def show_index():
    return render_template('index.html')


@app.route('/check_user_id')
def show_check_user_id():
    userID = request.args.get('userID')
    strQuery = db.session.query(individual.user_id,individual.role,individual.grade).filter(individual.user_id==userID)
    results = strQuery.all()

    return jsonify(has_user=True if len(results)==1 else False)


@app.route('/summary')
def show_summary_default():
    return redirect('/summary/PPPWQHXW')


@app.route('/summary/<user_id>')
def show_summary(user_id):

    # =================================
    # 工号，日期设定
    # =================================
    userID = str(user_id)
    startDate = ''
    endDate = ''


    # =================================
    # 门禁
    # =================================
    #
    # 最近一月 distinct门禁地点名数
    # 门禁地点数
    # 地点类型 accategory

    sql = "SELECT node_des,COUNT(acrec.node_des)as con from acrec where user_id='%s' GROUP BY node_des ORDER BY con DESC"%(userID)
    # sql = db.session.query(acrec.node_des, func.count(acrec.node_des)).filter(acrec.user_id==userID)
    results = db.session.execute(sql).fetchall()

    node_des = [result.node_des for result in results] # 地点名
    count = [result.con for result in results]         # 地点门禁次数
    node_cate = []                                     # 地点分类
    total_count = sum(count)                           # 总门禁次数

    ac_items = []
    for i in range(len(node_des)):
        sql = db.session.query(ac_loc.category).filter(ac_loc.node_des==node_des[i])
        node_cate.append(helpers.translate(sql.first()))
        ac_items.append({'node_des': node_des[i], 'count': count[i], 'node_cate': node_cate[i]})

    ret_access = {'count_nodes': len(node_des), 'total_count':total_count, 'ac_items': ac_items }


    # =================================
    # 生活习惯
    # =================================
    #
    # 最近一个月
    # 时间分布 6点~7点宿舍打卡
    # 23点到5点打卡  ACPeriodCate

    from controls.GetJson_ACPeriodCate import GetJson_ACPeriodCate
    json_ACPeriodCate = GetJson_ACPeriodCate(userID, 2, startDate, endDate)
    timeDistri = json_ACPeriodCate["json_timeDistribution"]

    dict_vals = {}
    for item in timeDistri["seriesData"]:
        dict_vals[item['name']] = item['data']

    df = DataFrame(dict_vals, index=range(24))

    df['SUM'] = 0
    for col, vals in df.iteritems():
        if col == 'SUM': break
        df['SUM'] += vals

    # print df

    if 'dorm' in df:
        count_early = df.loc[6]['dorm']  # 取 6 点宿舍值，总计早起次数
    else:
        count_early = 0

    count_night = sum(df.loc[0:6]['SUM'].tolist()) + df.loc[23]['SUM']  # 取23点 ~ 5点总门禁次数

    ret_habit = {'count_early': count_early, 'count_night': count_night }


    # =================================
    # 学习
    # =================================
    #
    # 最近一个月图书馆、教学楼次数

    from controls.GetJson_ACCategory import GetJson_ACCategory
    json_ACCategory = GetJson_ACCategory(userID,startDate,startDate)

    # print json_ACCategory['seriesData']

    count_acad = count_lib = count_sci = 0
    for item in json_ACCategory['seriesData']:
        if item['name'] == 'acad':
            count_acad = item['value']
        elif item['name'] == 'lib':
            count_lib = item['value']
        elif item['name'] == 'sci':
            count_sci = item['value']
    count_total = count_sci + count_acad + count_lib

    sql = db.session.query(ac_count.sum_per_month).order_by(ac_count.sum_per_month)
    results = sql.all()

    sum_per_month = [result.sum_per_month for result in results]

    # 获取个体在全体数据中排名
    idx_user = len(sum_per_month)
    for i in range(len(sum_per_month)):
        if int(sum_per_month[i]) > count_total:
            idx_user = i
            break

    percent_asc = float(sum(sum_per_month[: idx_user])) / sum(sum_per_month)

    ret_study = {'count_lib':count_lib, 'count_acad': count_acad, 'count_sci':count_sci, 'percent_asc': percent_asc}


    # =================================
    # 人际关系
    # =================================
    # 好友 —— 等待好友结果

    # 奋斗的路上有更多同伴才更有动力，有｛｝位同学曾与我擦肩而过。</br>
    #｛｝童鞋，我们｛｝次不断相遇，难道是缘分，难道是天意。

    from controls.GetJson_ACRelation import GetJson_ACRelation
    json_ACRelation = GetJson_ACRelation(userID)

    num_relations = json_ACRelation['num_total']
    if num_relations != 0:
        top_name = json_ACRelation['nodes'][0]['name']
        top_value = int(json_ACRelation['nodes'][0]['value'])
    else:
        top_name = 'None'
        top_value = 0
    ret_social = {'num_relations': num_relations, 'top_name':top_name, 'top_value':top_value }


    # =================================
    # 消费 bill
    # =================================
    #
    # 账单： 最近一月：
    # 消费类型比例 concategory, conablilty, expenditure
    # 一月消费总额

    from controls.GetJson_expenditure import GetJson_expenditure
    json_Expenditure = GetJson_expenditure(userID, 0, 2, startDate, endDate)

    # Get total_expend 总支出
    if 'errMsg' not in json_Expenditure:
        dateTrend = json_Expenditure['json_dateTrend']
        total_expend = dateTrend['accumulatedVals'][-1]
    else:
        total_expend = 0

    # 消费分类排名
    from controls.GetJson_ConCategory import GetJson_ConCategory
    json_ConCategory = GetJson_ConCategory(userID,startDate,endDate)

    if 'errMsg' not in json_ConCategory:
        con_items = json_ConCategory['seriesData']
        top_cate = helpers.translate(con_items[0]['name'])
    else:
        top_cate = ''

    # [{'name': 'food', 'value': 2653.9}, {'name': 'shop', 'value': 177.5}, {'name': 'None', 'value': 56.5}, ...]

    # 消费能力
    from controls.GetJson_ConAbility import GetJson_ConAbility
    json_ConAbility = GetJson_ConAbility(userID)

    # 月均消费
    if 'errMsg' not in json_ConAbility:
        con_per_month = json_ConAbility['userAmount']
    else:
        con_per_month = -1

    ret_bill = {'total_expend':total_expend, 'top_cate': top_cate, 'con_per_month': con_per_month}


    # =================================
    # 滞纳金
    # =================================

    from controls.GetJson_Penalty import GetJson_Penalty
    json_Penalty = GetJson_Penalty(userID)

    # json_userAmount = json_Penalty['json_userAmount']
    # json_penalty = json_Penalty['json_penalty']

    if 'errMsg' not in json_Penalty:
        user_penalty = json_Penalty['userAmount']  # 总滞纳金
        amount = json_Penalty['amount']
        num = json_Penalty['num']
        # 获取个体在全体数据中排名
        idx_user = len(amount)
        for i in range(len(amount)):
            if int(amount[i]) > user_penalty:
                idx_user = i
                break
        # idx_user = amount.index(int(user_penalty))
        percent_asc = float(sum(num[: idx_user])) / sum(num)

        ret_penalty = {'user_penalty': user_penalty, 'percent_asc': percent_asc}
    else:
        ret_penalty = {'user_penalty': -1, 'percent_asc': -1}

    # =================================
    # 打包

    vals_summary = {'ret_access': ret_access, 'ret_habit': ret_habit, 'ret_study': ret_study,
                    'ret_social': ret_social, 'ret_bill': ret_bill, 'ret_penalty': ret_penalty }

    # print "return render_template summary"
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

    if form.validate():
        userID = form.userID.data
        modeDate = int(form.modeDate.data)
        modeTime = int(form.modeTime.data)
        startDate = form.dateRange.data[:10]
        endDate = form.dateRange.data[-10:]

        from controls.GetJson_expenditure import GetJson_expenditure
        json_response = GetJson_expenditure(userID,modeDate,modeTime,startDate,endDate)
        json_response = jsonify(json_response)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


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

    if form.validate():
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

        json_response = jsonify(json_response)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


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

    if form.validate():
        devID = form.devID.data
        modeDate = int(form.modeDate.data)
        modeTime = int(form.modeTime.data)
        startDate = form.dateRange.data[:10]
        endDate = form.dateRange.data[-10:]

        from controls.GetJson_Income import GetJson_Income
        json_response = GetJson_Income(devID,modeDate, modeTime, startDate, endDate)
        json_response = jsonify(json_response)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


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

    if form.validate():
        modeTime = int(form.modeTime.data)

        from controls.GetJson_IncomeFood import GetJson_IncomeFood
        json_response = GetJson_IncomeFood(modeTime)
        json_response = jsonify(json_response)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/acvalid')
def show_chart_acvalid():
    form = Form_User_DR()
    return render_template('charts/chart-acvalid.html', form=form)


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

        # =======================
        titles = json_response['titles']
        seriesData = json_response['seriesData']

        titles = map(lambda x: helpers.translate(x), titles)
        for datum in seriesData:
            datum['name'] = helpers.translate(datum['name'])

        json_response['titles'] = titles
        json_response['seriesData'] = seriesData
        # =======================

        json_response = jsonify(json_response)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/accategory')
def show_chart_accategory():
    form = Form_User_DR()
    return render_template('charts/chart-accategory.html', form=form)


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

        # ==================
        titles = json_response['titles']
        seriesData = json_response['seriesData']

        for datum in seriesData:
            datum['name'] = helpers.translate(datum['name'])
        titles = [helpers.translate(title) for title in titles]

        json_response['titles'] = titles
        json_response['seriesData'] = seriesData
        # ==================

        json_response = jsonify(json_response)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/concategory')
def show_chart_concategory():
    form = Form_User_DR()
    return render_template('charts/chart-concategory.html', form=form)


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

        # ==================
        titles = json_response['titles']
        seriesData = json_response['seriesData']

        for datum in seriesData:
            datum['name'] = helpers.translate(datum['name'])
        titles = [helpers.translate(title) for title in titles]

        json_response['titles'] = titles
        json_response['seriesData'] = seriesData
        # ==================

        json_response = jsonify(json_response)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


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

    if form.validate():
        modeTime = int(form.modeTime.data)  # 赋值给变量
        from controls.GetJson_ConWaterTime import GetJson_ConWaterTime
        json_response = GetJson_ConWaterTime(modeTime)
        json_response = jsonify(json_response)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/conability')
def show_chart_conability():
    form = Form_User()
    return render_template('charts/chart-conability.html', form=form)


@app.route('/charts/conability/getData', methods=['GET'])
def refresh_chart_conability():
    form = Form_User()
    form.userID.data = request.args.get('userID')

    if form.validate():
        userID = form.userID.data

        from controls.GetJson_ConAbility import GetJson_ConAbility
        json_response = GetJson_ConAbility(userID)
        json_response = jsonify(json_response)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


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

    if form.validate():
        userID = form.userID.data

        from controls.GetJson_Penalty import GetJson_Penalty
        json_response = GetJson_Penalty(userID)
        json_response = jsonify(json_response)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


@app.route('/charts/relation')
def show_chart_relation():
    form = Form_User()
    return render_template('charts/chart-relation.html', form=form)


@app.route('/charts/relation/getData', methods=['GET'])
def refresh_chart_relation():
    form = Form_User()
    form.userID.data = request.args.get('userID')

    if form.validate():
        userID = form.userID.data

        from controls.GetJson_ACRelation import GetJson_ACRelation
        json_response = GetJson_ACRelation(userID)

        json_response = jsonify(json_response)
    else:
        json_response = jsonify(errMsg=form.errors)
    return json_response


# =====================================
# Summary 所用图表获取json返回的路由
# =====================================

@app.route('/summary/GetJson_penalty', methods=['GET'])
def refresh_summary_penalty():
    userID = request.args.get('userID')

    from controls.GetJson_Penalty import GetJson_Penalty
    json_response = GetJson_Penalty(userID)
    json_response = jsonify(json_response)
    return json_response


@app.route('/summary/GetJson_accategory', methods=['GET'])
def refresh_summary_accategory():

    userID = request.args.get('userID')
    startDate = request.args.get('startDate')
    endDate = request.args.get('startDate')

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

    json_response = jsonify(json_response)
    return json_response


@app.route('/summary/GetJson_concategory', methods=['GET'])
def refresh_summary_concategory():

    userID = request.args.get('userID')
    startDate = request.args.get('startDate')
    endDate = request.args.get('startDate')

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

    json_response = jsonify(json_response)
    return json_response


@app.route('/summary/GetJson_acperiodcate', methods=['GET'])
def refresh_summary_acperiodcate():

    userID = request.args.get('userID')
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')

    modeDate = 2

    from controls.GetJson_ACPeriodCate import GetJson_ACPeriodCate

    json_response = GetJson_ACPeriodCate(userID, modeDate, startDate, endDate)

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

    json_response = jsonify(json_response)

    return json_response


@app.route('/summary/GetJson_relation', methods=['GET'])
def refresh_summary_relation():
    userID = request.args.get('userID')

    from controls.GetJson_ACRelation import GetJson_ACRelation
    json_response = GetJson_ACRelation(userID)

    json_response = jsonify(json_response)
    return json_response

# =====================================
# Summary End
# =====================================



