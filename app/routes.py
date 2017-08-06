#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import render_template, request, jsonify
from sqlalchemy import func

from app import app
from app import helpers
from app.forms import *
from app.models import *


@app.route('/check_user_id')
def show_check_user_id():
    userID = request.args.get('userID')
    dbQuery = db.session.query(individual.user_id, individual.role, individual.grade).filter(
        individual.user_id == userID)
    return jsonify(has_user=True if len(dbQuery.all()) == 1 else False)


def check_user_id(userID):
    dbQuery = individual.query.filter(individual.user_id == userID)
    return True if len(dbQuery.all()) == 1 else False


# ==================
@app.route('/')
def index():
    return render_template('index.html')


# ========================
# 门禁类型比例
# ========================
@app.route('/charts/accategory')
def show_chart_accategory():
    form = Form_AcCategory()
    return render_template('charts/individual/access/chart-accategory.html', form=form)


@app.route('/charts/accategory/getData')
def refresh_chart_accategory():
    form = Form_AcCategory()
    form.userID.data = request.args.get('userID')
    form.dateRange.data = request.args.get('dateRange')

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])
    if not check_user_id(form.userID.data):
        return jsonify(errMsg=lstr.warn_userIDNon)

    userID = form.userID.data
    startDate = form.dateRange.data[:10]
    endDate = form.dateRange.data[-10:]

    from app.functions.individual.access.GetJson_AcCategory import GetJson_AcCategory
    json_response = GetJson_AcCategory(userID, startDate, endDate)

    if 'errMsg' not in json_response:
        helpers.translateSeriesData(json_response['seriesData'])

    return jsonify(json_response)


# ========================
# 门禁日期变化
# ========================
@app.route('/charts/acdatetrend')
def show_chart_acdatetrend():
    form = Form_AcDateTrend()
    return render_template('charts/individual/access/chart-acdatetrend.html', form=form)


@app.route('/charts/acdatetrend/getData', methods=['GET'])
def refresh_chart_acdatetrend():
    form = Form_AcDateTrend()
    form.userID.data = request.args.get('userID')
    form.modeDate.data = request.args.get('modeDate')
    form.dateRange.data = request.args.get('dateRange')

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])
    if not check_user_id(form.userID.data):
        return jsonify(errMsg=lstr.warn_userIDNon)

    userID = form.userID.data
    modeDate = form.modeDate.data
    startDate = form.dateRange.data[:10]
    endDate = form.dateRange.data[-10:]

    from app.functions.individual.access.GetJson_AcDateTrend import GetJson_AcDateTrend
    json_response = GetJson_AcDateTrend(userID, startDate, endDate, modeDate)

    if 'errMsg' not in json_response:
        helpers.translateSeriesData(json_response['seriesData'])
        helpers.translateStatRows(json_response['statRows'])

    return jsonify(json_response)


# ========================
# 门禁时间分布
# ========================
@app.route('/charts/actimedistr')
def show_chart_actimedistr():
    form = Form_AcTimeDistr()
    return render_template('charts/individual/access/chart-actimedistr.html', form=form)


@app.route('/charts/actimedistr/getData', methods=['GET'])
def refresh_chart_actimedistr():
    form = Form_AcTimeDistr()
    form.userID.data = request.args.get('userID')
    form.dateRange.data = request.args.get('dateRange')

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])
    if not check_user_id(form.userID.data):
        return jsonify(errMsg=lstr.warn_userIDNon)

    userID = form.userID.data
    startDate = form.dateRange.data[:10]
    endDate = form.dateRange.data[-10:]

    from app.functions.individual.access.GetJson_AcTimeDistri import GetJson_AcTimeDistri
    json_response = GetJson_AcTimeDistri(userID, startDate, endDate)

    if 'errMsg' not in json_response:
        helpers.translateSeriesData(json_response['seriesData'])
        helpers.translateStatRows(json_response['statRows'])

    return jsonify(json_response)


# ========================
# 消费类型比例
# ========================
@app.route('/charts/concategory')
def show_chart_concategory():
    form = Form_Concategory()
    return render_template('charts/individual/consumption/chart-concategory.html', form=form)


@app.route('/charts/concategory/getData')
def refresh_chart_concategory():
    form = Form_Concategory()
    form.userID.data = request.args.get('userID')
    form.dateRange.data = request.args.get('dateRange')

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])
    if not check_user_id(form.userID.data):
        return jsonify(errMsg=lstr.warn_userIDNon)

    userID = form.userID.data
    startDate = form.dateRange.data[:10]
    endDate = form.dateRange.data[-10:]

    from app.functions.individual.consumption.GetJson_ConCategory import GetJson_ConCategory
    json_response = GetJson_ConCategory(userID, startDate, endDate)

    if 'errMsg' not in json_response:
        dataDict = json_response['dataDict']
        keys = list(dataDict.keys())
        for k in keys:
            v = dataDict[k]
            del dataDict[k]
            k = helpers.translate(k)
            dataDict[k] = v
        json_response['dataDict'] = dataDict
    return jsonify(json_response)


# ========================
# 消费日期变化
# ========================
@app.route('/charts/condatetrend')
def show_chart_condatetrend():
    form = Form_ConDateTrend()
    return render_template('charts/individual/consumption/chart-condatetrend.html', form=form)


@app.route('/charts/condatetrend/getData')
def refresh_chart_condatetrend():
    form = Form_ConDateTrend()
    form.userID.data = request.args.get('userID')
    form.modeDate.data = request.args.get('modeDate')
    form.dateRange.data = request.args.get('dateRange')

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])
    if not check_user_id(form.userID.data):
        return jsonify(errMsg=lstr.warn_userIDNon)

    userID = form.userID.data
    modeDate = form.modeDate.data
    startDate = form.dateRange.data[:10]
    endDate = form.dateRange.data[-10:]

    from app.functions.individual.consumption.GetJson_ConDateTrend import GetJson_ConDateTrend
    json_response = GetJson_ConDateTrend(userID, startDate, endDate, modeDate)

    if 'errMsg' not in json_response:
        helpers.translateSeriesData(json_response['seriesData'])
        helpers.translateStatRows(json_response['statRows'])

    return jsonify(json_response)


# ========================
# 消费时间分布
# ========================
@app.route('/charts/contimedistr')
def show_chart_contimedistr():
    form = Form_ConTimeDistr()
    return render_template('charts/individual/consumption/chart-contimedistr.html', form=form)


@app.route('/charts/contimedistr/getData', methods=['GET'])
def refresh_chart_contimedistr():
    form = Form_ConTimeDistr()
    form.userID.data = request.args.get('userID')
    form.dateRange.data = request.args.get('dateRange')

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])
    if not check_user_id(form.userID.data):
        return jsonify(errMsg=lstr.warn_userIDNon)

    userID = form.userID.data
    startDate = form.dateRange.data[:10]
    endDate = form.dateRange.data[-10:]

    from app.functions.individual.consumption.GetJson_ConTimeDistri import GetJson_ConTimeDistri
    json_response = GetJson_ConTimeDistri(userID, startDate, endDate)
    if 'errMsg' not in json_response:
        helpers.translateSeriesData(json_response['seriesData'])
        helpers.translateStatRows(json_response['statRows'])

    return jsonify(json_response)


# ========================
# 图书借阅违规缴费记录
# ========================
@app.route('/charts/penalty')
def show_chart_penalty():
    form = Form_Penalty()
    return render_template('charts/individual/consumption/chart-penalty.html', form=form)


@app.route('/charts/penalty/getData', methods=['GET'])
def refresh_chart_penalty():
    form = Form_Penalty()
    form.userID.data = request.args.get('userID')

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])

    userID = form.userID.data

    from app.functions.individual.consumption.GetJson_Penalty import GetJson_Penalty
    json_response = GetJson_Penalty(userID)
    return jsonify(json_response)


# ========================
# 学校门禁类型比例
# ========================
@app.route('/charts/schaccategory')
def show_chart_schaccategory():
    return render_template('charts/school/access/chart-schaccategory.html')


@app.route('/charts/schaccategory/getData')
def refresh_chart_schaccategory():
    from app.functions.school.access.GetJson_SchAcCategory import GetJson_SchAcCategory
    json_response = GetJson_SchAcCategory()

    if 'errMsg' not in json_response:
        data = json_response['data']
        for datum in data:
            datum['name'] = helpers.translate(datum['name'])
        json_response['data'] = data

    return jsonify(json_response)


# ========================
# 学校门禁日期变化
# ========================
@app.route('/charts/schacdatetrend')
def show_chart_schacdatetrend():
    form = Form_SchAcDateTrend()
    return render_template('charts/school/access/chart-schacdatetrend.html', form=form)


@app.route('/charts/schacdatetrend/getData')
def refresh_chart_schacdatetrend():
    form = Form_SchAcDateTrend()
    form.modeDate.data = request.args.get('modeDate')

    modeDate = form.modeDate.data

    from app.functions.school.access.GetJson_SchAcDateTrend import GetJson_SchAcDateTrend
    json_response = GetJson_SchAcDateTrend(modeDate)

    if 'errMsg' not in json_response:
        json_origin = json_response['json_origin']
        json_predict = json_response['json_predict']

        def translate(json_response):
            helpers.translateSeriesData(json_response['seriesData'])
            helpers.translateStatRows(json_response['statRows'])

        translate(json_origin)
        translate(json_predict)
        json_response = {'json_origin': json_origin, 'json_predict': json_predict}

    return jsonify(json_response)


# ========================
# 学校门禁时间分布
# ========================
@app.route('/charts/schactimedistr')
def show_chart_schactimedistr():
    return render_template('charts/school/access/chart-schactimedistr.html')


@app.route('/charts/schactimedistr/getData', methods=['GET'])
def refresh_chart_schactimedistr():
    from app.functions.school.access.GetJson_SchAcTimeDistr import GetJson_SchAcTimeDistr
    json_response = GetJson_SchAcTimeDistr()

    if 'errMsg' not in json_response:
        helpers.translateSeriesData(json_response['seriesData'])
        helpers.translateStatRows(json_response['statRows'])

    return jsonify(json_response)


# ========================
# 学校消费类型比例
# ========================
@app.route('/charts/schconcategory')
def show_chart_schconcategory():
    return render_template('charts/school/consumption/chart-schconcategory.html')


@app.route('/charts/schconcategory/getData')
def refresh_chart_schconcategory():
    from app.functions.school.consumption.GetJson_SchConCategory import GetJson_SchConCategory
    json_response = GetJson_SchConCategory()

    if 'errMsg' not in json_response:
        data = json_response['data']
        for datum in data:
            datum['name'] = helpers.translate(datum['name'])
        json_response['data'] = data
    return jsonify(json_response)


# ========================
# 学校消费日期变化
# ========================
@app.route('/charts/schcondatetrend')
def show_chart_schcondatetrend():
    form = Form_SchConDateTrend()
    return render_template('charts/school/consumption/chart-schcondatetrend.html', form=form)


@app.route('/charts/schcondatetrend/getData')
def refresh_chart_schcondatetrend():
    form = Form_SchConDateTrend()
    form.modeDate.data = request.args.get('modeDate')

    modeDate = form.modeDate.data

    from app.functions.school.consumption.GetJson_SchConDateTrend import GetJson_SchConDateTrend
    json_response = GetJson_SchConDateTrend(modeDate)

    if 'errMsg' not in json_response:
        json_origin = json_response['json_origin']
        json_predict = json_response['json_predict']

        def translate(json_response):
            helpers.translateSeriesData(json_response['seriesData'])
            helpers.translateStatRows(json_response['statRows'])

        translate(json_origin)
        translate(json_predict)
        json_response = {'json_origin': json_origin, 'json_predict': json_predict}

    return jsonify(json_response)


# ========================
# 学校消费时间分布
# ========================
@app.route('/charts/schcontimedistr')
def show_chart_schcontimedistr():
    return render_template('charts/school/consumption/chart-schcontimedistr.html')


@app.route('/charts/schcontimedistr/getData', methods=['GET'])
def refresh_chart_schcontimedistr():
    from app.functions.school.consumption.GetJson_SchConTimeDistr import GetJson_SchConTimeDistr
    json_response = GetJson_SchConTimeDistr()

    if 'errMsg' not in json_response:
        helpers.translateSeriesData(json_response['seriesData'])
        helpers.translateStatRows(json_response['statRows'])

    return jsonify(json_response)


# ========================
# 人际关系
# ========================
@app.route('/charts/relation')
def show_chart_relation():
    form = Form_Relation()
    return render_template('charts/mining/chart-relation.html', form=form)


@app.route('/charts/relation/getData', methods=['GET'])
def refresh_chart_relation():
    form = Form_Relation()
    form.userID.data = request.args.get('userID')

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])

    userID = form.userID.data
    from app.functions.mining.GetJson_ACRelation import GetJson_ACRelation
    json_response = GetJson_ACRelation(userID)

    return jsonify(json_response)


# ========================
# 消费能力
# ========================
@app.route('/charts/conability')
def show_chart_conability():
    form = Form_ConAbility()
    return render_template('charts/mining/chart-conability.html', form=form)


@app.route('/charts/conability/getData')
def refresh_chart_conability():
    form = Form_ConAbility()
    form.userID.data = request.args.get('userID')

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])
    if not check_user_id(form.userID.data):
        return jsonify(errMsg=lstr.warn_userIDNon)

    userID = form.userID.data

    from app.functions.mining.GetJson_ConAbility import GetJson_ConAbility
    json_response = GetJson_ConAbility(userID)

    return jsonify(json_response)


# ========================
# 学习和消费能力
# ========================
@app.route('/charts/studyandconability')
def show_chart_studyandconability():
    form = Form_StudyAndConAbility()
    return render_template('charts/mining/chart-studyandconability.html', form=form)


@app.route('/charts/studyandconability/getData')
def refresh_chart_studyandconability():
    form = Form_StudyAndConAbility()
    form.userID.data = request.args.get('userID')

    if not form.validate():
        return jsonify(errMsg=form.errors['userID'])
    if not check_user_id(form.userID.data):
        return jsonify(errMsg=lstr.warn_userIDNon)

    userID = form.userID.data

    from app.functions.mining.GetJson_StudyAndConAbility import GetJson_StudyAndConAbility
    json_response = GetJson_StudyAndConAbility(userID)

    return jsonify(json_response)


# ========================
# 人数统计
# ========================
@app.route('/charts/number')
def show_chart_number():
    return render_template('charts/school/chart-numberBar.html')


@app.route('/charts/number/getData', methods=['GET'])
def refresh_chart_number():
    # query number of people by dividing into total & grades
    dbQueryTotal = db.session.query(individual.role, func.count('*')).group_by(individual.role)
    # GradeB stands for 本科生的年级
    dbQueryGradeB = db.session.query(individual.grade, func.count('*')).filter(individual.role == u'本科生').group_by(
        individual.grade)
    # GradePg stands for 研究生的年级
    dbQueryGradePg = db.session.query(individual.grade, func.count('*')).filter(individual.role == u'研究生').group_by(
        individual.grade)
    # GradeDr stands for 博士生的年级
    dbQueryGradeDr = db.session.query(individual.grade, func.count('*')).filter(individual.role == u'博士生').group_by(
        individual.grade)

    # go
    resultsTotal = dbQueryTotal.all()
    resultsGradeB = dbQueryGradeB.all()
    resultsGradePg = dbQueryGradePg.all()
    resultsGradeDr = dbQueryGradeDr.all()

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

    # convert result to json
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
    json_response = jsonify(json_numberTotal=json_numberTotal, json_numberGradeB=json_numberGradeB,
                            json_numberGradePg=json_numberGradePg, json_numberGradeDr=json_numberGradeDr)
    return json_response


# ========================
# 学校宿舍用水时间分布
# ========================
@app.route('/charts/conwater')
def show_chart_conWater():
    form = Form_ConWater()
    return render_template('charts/school/consumption/chart-conwater.html', form=form)


@app.route('/charts/conwater/getData', methods=['GET'])
def refresh_chart_conWater():
    form = Form_ConWater()
    form.modeTime.data = request.args.get('modeTime')

    if not form.validate():
        return jsonify(errMsg=form.errors)

    modeTime = int(form.modeTime.data)  # 赋值给变量
    from app.functions.school.consumption.GetJson_ConWater import GetJson_ConWater
    json_response = GetJson_ConWater(modeTime)
    return jsonify(json_response)


# ========================
# 学校餐饮收入时间分布
# ========================
@app.route('/charts/confood')
def show_chart_conFood():
    form = Form_ConFood()
    return render_template('charts/school/consumption/chart-confood.html', form=form)


@app.route('/charts/confood/getData', methods=['GET'])
def refresh_chart_conFood():
    form = Form_ConFood()
    form.modeTime.data = request.args.get('modeTime')

    if not form.validate():
        return jsonify(errMsg=form.errors)

    modeTime = int(form.modeTime.data)

    from app.functions.school.consumption.GetJson_ConFood import GetJson_ConFood
    json_response = GetJson_ConFood(modeTime)
    return jsonify(json_response)
