#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.models import *
from pandas import DataFrame
from app import helpers

def GetJson_Summary(userID, startDate, endDate):

    ret_access = ac_overall(userID, startDate, endDate)  # 门禁
    ret_habit = ac_time(userID, startDate, endDate)  # 生活习惯
    ret_study = ac_study(userID, startDate, endDate)  # 学习
    ret_social = relation(userID)  # 人际关系
    ret_bill = bill(userID, startDate, endDate)  # 消费 bill
    ret_penalty = con_penalty(userID)  # 滞纳金

    # 最后打包
    return {'ret_access': ret_access, 'ret_habit': ret_habit, 'ret_study': ret_study, 'ret_social': ret_social,
                    'ret_bill': ret_bill, 'ret_penalty': ret_penalty}

# 门禁
def ac_overall(userID, startDate, endDate):
    # 不同门禁地点的数量
    # 总门禁次数
    # 地点信息：名称，次数，分类

    sql = "SELECT node_des,COUNT(acrec.node_des)as con from acrec where user_id='%s' GROUP BY node_des ORDER BY con DESC" % (
        userID)
    # sql = db.session.query(acrec.node_des, func.count(acrec.node_des)).filter(acrec.user_id==userID)
    results = db.session.execute(sql).fetchall()

    if len(results)==0:
        return {'count_nodes':-1, 'total_count': -1, 'ac_items': -1}

    node_des = [result.node_des for result in results]  # 地点名
    count = [result.con for result in results]  # 地点门禁次数
    node_cate = []  # 地点分类
    total_count = sum(count)  # 总门禁次数

    ac_items = []
    for i in xrange(len(node_des)):
        sql = db.session.query(ac_loc.category).filter(ac_loc.node_des == node_des[i])  # 查询地点的分类
        node_cate.append(helpers.translate(sql.first()))  # 翻译并加入
        ac_items.append({'node_des': node_des[i], 'count': count[i], 'node_cate': node_cate[i]})

    return {'count_nodes': len(node_des), 'total_count': total_count, 'ac_items': ac_items}

# 生活习惯
def ac_time(userID, startDate, endDate):
    # 最近一个月
    # 时间分布 6点~7点宿舍打卡
    # 23点到5点打卡  ACPeriodCate

    from GetJson_ACPeriodCate import GetJson_ACPeriodCate
    json_ACPeriodCate = GetJson_ACPeriodCate(userID, 2, startDate, endDate)

    if 'errMsg' in json_ACPeriodCate:
        return {'count_early': -1, 'count_night': -1}

    timeDistri = json_ACPeriodCate["json_timeDistribution"]
    dict_vals = {}
    for item in timeDistri["seriesData"]:
        dict_vals[item['name']] = item['data']

    df = DataFrame(dict_vals, index=range(24))

    df['SUM'] = 0
    for col, vals in df.iteritems():
        if col == 'SUM': break
        df['SUM'] += vals

    count_early = df.loc[6]['dorm'] if 'dorm' in df else 0  # 取 6 点宿舍值，总计早起次数
    count_night = sum(df.loc[0:6]['SUM'].tolist()) + df.loc[23]['SUM']  # 取23点 ~ 5点总门禁次数

    return {'count_early': count_early, 'count_night': count_night}

# 学习
def ac_study(userID, startDate, endDate):
    # 最近一个月图书馆、教学楼次数

    from GetJson_ACCategory import GetJson_ACCategory
    json_ACCategory = GetJson_ACCategory(userID, startDate, startDate)

    if 'errMsg' in json_ACCategory:
        return {'count_lib': -1, 'count_acad': -1, 'count_sci': -1, 'percent_asc': -1}

    # 教学、图书馆、科研门禁计数
    count = {'acad': 0, 'lib': 0, 'sci': 0}
    for item in json_ACCategory['seriesData']:
        count[item['name']] = item['value']
    count_total = count['acad'] + count['lib'] + count['sci']

    sql = ac_count.query
    results = sql.all()
    sum_per_month = sorted([result.get_sum_per_month() for result in results])

    # 获取个体在全体数据中排名
    idx_user = len(sum_per_month)
    for i in xrange(len(sum_per_month)):
        if int(sum_per_month[i]) > count_total:
            idx_user = i
            break

    percent_asc = float(sum(sum_per_month[: idx_user])) / sum(sum_per_month)

    return {'count_lib': count['lib'], 'count_acad': count['acad'], 'count_sci': count['sci'],
                 'percent_asc': percent_asc}

# 人际关系
def relation(userID):
    # 好友数 关系最高好友名 关系最高好友值

    from GetJson_ACRelation import GetJson_ACRelation
    json_ACRelation = GetJson_ACRelation(userID)

    num_relations = json_ACRelation['num_total']
    top_name = ''
    top_value = -1

    if num_relations > 1:
        top_name = json_ACRelation['nodes'][1]['name']  # 0号是关系中心
        top_value = int(json_ACRelation['nodes'][1]['value'])
    elif num_relations == 1:    # 除了自己没有人际关系
        top_value = 0

    return {'num_relations': num_relations, 'top_name': top_name, 'top_value': top_value}

# 账单
def bill(userID, startDate, endDate):
    # 账单： 最近一月：
    # 消费类型比例 concategory, conablilty, expenditure
    # 一月消费总额

    # init
    total_expend = -1
    top_cate = ''
    con_per_month = -1

    # Get total_expend 总支出
    from GetJson_expenditure import GetJson_expenditure
    json_Expenditure = GetJson_expenditure(userID, 0, 2, startDate, endDate)
    if 'errMsg' not in json_Expenditure:
        dateTrend = json_Expenditure['json_dateTrend']
        total_expend = dateTrend['accumulatedVals'][-1]

    # 消费分类排名
    from GetJson_ConCategory import GetJson_ConCategory
    json_ConCategory = GetJson_ConCategory(userID, startDate, endDate)

    if 'errMsg' not in json_ConCategory:
        con_items = json_ConCategory['seriesData']
        top_cate = helpers.translate(con_items[0]['name'])

    # [{'name': 'food', 'value': 2653.9}, {'name': 'shop', 'value': 177.5}, {'name': 'None', 'value': 56.5}, ...]

    # 消费能力
    from GetJson_ConAbility import GetJson_ConAbility
    json_ConAbility = GetJson_ConAbility(userID)

    # 月均消费
    if 'errMsg' not in json_ConAbility:
        con_per_month = json_ConAbility['userAmount']

    return {'total_expend': total_expend, 'top_cate': top_cate, 'con_per_month': con_per_month}

# 违约金
def con_penalty(userID):
    from GetJson_Penalty import GetJson_Penalty
    json_Penalty = GetJson_Penalty(userID)

    if 'errMsg' in json_Penalty:
        return {'user_penalty': -1, 'percent_asc': -1}
    else:
        user_penalty = json_Penalty['userAmount']  # 总滞纳金
        amount = json_Penalty['amount']
        num = json_Penalty['num']
        # 获取个体在全体数据中排名
        idx_user = len(amount)
        for i in xrange(len(amount)):
            if int(amount[i]) > user_penalty:
                idx_user = i
                break
        # idx_user = amount.index(int(user_penalty))
        percent_asc = float(sum(num[: idx_user])) / sum(num)

        return {'user_penalty': user_penalty, 'percent_asc': percent_asc}
