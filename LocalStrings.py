#!/usr/bin/env python
# -*- coding: UTF-8 -*-


userID = u'工号'
devID = u'设备号'
startDate = u'开始日期'
endDate = u'结束日期'
modeDate = u'日期模式'
modeTime = u'时间模式'
dateRange = u'日期范围'

warn_userIDFill = u'工号不可为空'
warn_userIDLength = u'工号长度应为8'
warn_devIDFill = u'设备号不可为空'
warn_devIDLength = u'设备号长度最大为10'

opts_modeDate = (u'日', u'周', u'月', u'季', u'年')
opts_modeTime = (u'24小时', u'7天', u'12月')

dictTrans = {
    'water' : u'生活用水',
    'shop' : u'超市',
    'recharge' : u'充值',
    'discipline' : u'违纪',
    'food' : u'餐饮',
    'sport' : u'运动',
    'med' : u'医务',
    'study' : u'学习',

    '0': u'非法',
    '1': u'合法',

    'acad': u'教学楼',
    'dorm': u'宿舍',
    'admin':u'行政',
    'lib':u'图书馆',
    'sci':u'科研',

    'none':u'其他',
    'None':u'其他',

    'SUM':u'总和',
    'PER_DORM':u'宿舍比重'
}
