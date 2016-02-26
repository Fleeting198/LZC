#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 02-13 创建。试图应用flask_admin的datepicker失败。
# 02-14 日期域改回StringField，暂时使用直接引入Datetimepick，因为flask-admin的picker无法运行。
# 02-16 Implementing dateRangePicker.
# 02-22 Form 类根据输入重构继承，而不是每个功能定义一个类。
# 02-23 其实并继承不了。添加Form_DaterangeMode。

from wtforms import StringField, RadioField, Form
from wtforms.validators import *
import LocalStrings as lstr


class Form_User(Form):
    """
    工号选择
    """
    userID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                  Length(min=8, max=8, message=lstr.warn_userIDLength)])

class Form_User_DR(Form):
    """
    工号，日期范围
    """
    userID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                  Length(min=8, max=8, message=lstr.warn_userIDLength)])
    dateRange = StringField(lstr.dateRange, validators=[Optional()])


class Form_User_DR_MD(Form):
    """
    工号，日期范围，日期模式
    """
    userID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                  Length(min=8, max=8, message=lstr.warn_userIDLength)])
    dateRange = StringField(lstr.dateRange, validators=[Optional()])
    modeDate = RadioField(lstr.modeDate,
                          choices=[('0', lstr.opts_modeDate[0]), ('1', lstr.opts_modeDate[1]), ('2', lstr.opts_modeDate[2]),
                                   ('3', lstr.opts_modeDate[3]), ('4', lstr.opts_modeDate[4])],
                          default='2')


class Form_User_DR_MD_MT(Form):
    """
    工号，日期范围，日期模式
    """
    userID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                  Length(min=8, max=8, message=lstr.warn_userIDLength)])
    dateRange = StringField(lstr.dateRange, validators=[Optional()])
    modeDate = RadioField(lstr.modeDate,
                          choices=[('0', lstr.opts_modeDate[0]), ('1', lstr.opts_modeDate[1]), ('2', lstr.opts_modeDate[2]),
                                   ('3', lstr.opts_modeDate[3]), ('4', lstr.opts_modeDate[4])], default='2')
    modeTime = RadioField(lstr.modeTime,
                          choices=[('0', lstr.opts_modeTime[0]), ('1', lstr.opts_modeTime[1]), ('2', lstr.opts_modeTime[2])],
                          default='0')


class Form_Dev_DR(Form):
    """
    设备号，日期范围
    """
    devID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                  Length(max=10, message=lstr.warn_userIDLength)])
    dateRange = StringField(lstr.dateRange, validators=[Optional()])


class Form_Dev_DR_MD(Form):
    """
    设备号，日期范围，日期模式。
    """
    devID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                 Length(max=10, message=lstr.warn_userIDLength)])
    dateRange = StringField(lstr.dateRange, validators=[Optional()])
    modeDate = RadioField(lstr.modeDate,
                          choices=[('0', lstr.opts_modeDate[0]), ('1', lstr.opts_modeDate[1]), ('2', lstr.opts_modeDate[2]),
                                   ('3', lstr.opts_modeDate[3]), ('4', lstr.opts_modeDate[4])], default='2')


class Form_Dev_DR_MD_MT(Form):
    """
    设备号，日期范围，日期模式
    """
    devID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                 Length(max=10, message=lstr.warn_userIDLength)])
    dateRange = StringField(lstr.dateRange, validators=[Optional()])
    modeDate = RadioField(lstr.modeDate,
                          choices=[('0', lstr.opts_modeDate[0]), ('1', lstr.opts_modeDate[1]), ('2', lstr.opts_modeDate[2]),
                                   ('3', lstr.opts_modeDate[3]), ('4', lstr.opts_modeDate[4])], default='2')
    modeTime = RadioField(lstr.modeTime,
                          choices=[('0', lstr.opts_modeTime[0]), ('1', lstr.opts_modeTime[1]), ('2', lstr.opts_modeTime[2])],
                          default='0')


class Form_DR_MD(Form):
    """
    日期范围，日期模式
    """
    dateRange = StringField(lstr.dateRange, validators=[Optional()])
    modeDate = RadioField(lstr.modeDate,
                          choices=[('0', lstr.opts_modeDate[0]), ('1', lstr.opts_modeDate[1]), ('2', lstr.opts_modeDate[2]),
                                   ('3', lstr.opts_modeDate[3]), ('4', lstr.opts_modeDate[4])], default='2')

class Form_DR_MD_MT(Form):
    """
    日期范围，日期模式
    """
    dateRange = StringField(lstr.dateRange, validators=[Optional()])
    modeDate = RadioField(lstr.modeDate,
                          choices=[('0', lstr.opts_modeDate[0]), ('1', lstr.opts_modeDate[1]), ('2', lstr.opts_modeDate[2]),
                                   ('3', lstr.opts_modeDate[3]), ('4', lstr.opts_modeDate[4])], default='2')
    modeTime = RadioField(lstr.modeTime,
                          choices=[('0', lstr.opts_modeTime[0]), ('1', lstr.opts_modeTime[1]), ('2', lstr.opts_modeTime[2])],
                          default='0')

class Form_MT(Form):
    modeTime = RadioField(lstr.modeTime,
                          choices=[('0', lstr.opts_modeTime[0]), ('1', lstr.opts_modeTime[1]), ('2', lstr.opts_modeTime[2])],
                          default='0')
