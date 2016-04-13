#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from wtforms import StringField, RadioField, Form
from wtforms.validators import *
import LocalStrings as lstr

class Form_User(Form):
    """工号选择
    """
    userID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                  Length(min=8, max=8, message=lstr.warn_userIDLength)])

class Form_User_DR(Form_User):
    """工号，日期范围
    """
    dateRange = StringField(lstr.dateRange, validators=[Optional()])


class Form_User_DR_MD(Form_User_DR):
    """工号，日期范围，日期模式
    """
    modeDate = RadioField(lstr.modeDate, choices=[('0', lstr.opts_modeDate[0]), ('1', lstr.opts_modeDate[1]),
                                                  ('2', lstr.opts_modeDate[2]), ('3', lstr.opts_modeDate[3]),
                                                  ], default='2')


class Form_User_DR_MD_MT(Form_User_DR_MD):
    """工号，日期范围，日期模式
    """
    modeTime = RadioField(lstr.modeTime,
                          choices=[('0', lstr.opts_modeTime[0]), ('1', lstr.opts_modeTime[1]), ('2', lstr.opts_modeTime[2])],
                          default='0')


class Form_Dev_DR(Form):
    """设备号，日期范围
    """
    devID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                  Length(max=10, message=lstr.warn_userIDLength)])
    dateRange = StringField(lstr.dateRange, validators=[Optional()])


class Form_Dev_DR_MD(Form_Dev_DR):
    """设备号，日期范围，日期模式。
    """
    modeDate = RadioField(lstr.modeDate,
                          choices=[('0', lstr.opts_modeDate[0]), ('1', lstr.opts_modeDate[1]), ('2', lstr.opts_modeDate[2]),
                                   ('3', lstr.opts_modeDate[3])], default='2')


class Form_Dev_DR_MD_MT(Form_Dev_DR_MD):
    """设备号，日期范围，日期模式
    """
    modeTime = RadioField(lstr.modeTime,
                          choices=[('0', lstr.opts_modeTime[0]), ('1', lstr.opts_modeTime[1]), ('2', lstr.opts_modeTime[2])],
                          default='0')


class Form_DR_MD(Form):
    """日期范围，日期模式
    """
    dateRange = StringField(lstr.dateRange, validators=[Optional()])
    modeDate = RadioField(lstr.modeDate,
                          choices=[('0', lstr.opts_modeDate[0]), ('1', lstr.opts_modeDate[1]), ('2', lstr.opts_modeDate[2]),
                                   ('3', lstr.opts_modeDate[3])], default='2')

class Form_DR_MD_MT(Form_DR_MD):
    """日期范围，日期模式
    """
    modeTime = RadioField(lstr.modeTime,
                          choices=[('0', lstr.opts_modeTime[0]), ('1', lstr.opts_modeTime[1]), ('2', lstr.opts_modeTime[2])],
                          default='0')

class Form_MT(Form):
    modeTime = RadioField(lstr.modeTime,
                          choices=[('0', lstr.opts_modeTime[0]), ('1', lstr.opts_modeTime[1]), ('2', lstr.opts_modeTime[2])],
                          default='0')
