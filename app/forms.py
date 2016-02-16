#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 02-13 创建。试图应用flask_admin的datepicker失败。  -陈
# 02-14 日期域改回StringField，暂时使用直接引入Datetimepick，因为flask-admin的picker无法运行。
# 02-16 Implementing dateRangePicker.

# from flask.ext.wtf import Form
from wtforms import StringField, RadioField, Form
from wtforms.validators import *
import LocalStrings as lstr


class form_expenditure(Form):
    userID = StringField(lstr.userID,
                         validators=[DataRequired(message=lstr.warn_userIDFill),
                                     Length(min=8, max=8, message=lstr.warn_userIDLength)],
                         default='TPPZLPHY', )

    dateRange = StringField(lstr.dateRange, validators=[Optional()])
    # startDate = StringField(lstr.startDate, validators=[Optional()] )
    # endDate = StringField(lstr.endDate, validators=[Optional()] )
    modeDate = RadioField(lstr.modeDate,
                          choices=[('0', lstr.Day), ('1', lstr.Wek), ('2', lstr.Mon), ('3', lstr.Qtr), ('4', lstr.Yer)],
                          default='0')


class form_acperiod(Form):
    userID = StringField(lstr.userID,
                         validators=[DataRequired(message=lstr.warn_userIDFill),
                                     Length(min=8, max=8, message=lstr.warn_userIDLength)],
                         default='NIHHXTXQ', )
    dateRange = StringField(lstr.dateRange, validators=[Optional()])



class form_income(Form):
    devID = StringField(lstr.devID,
                        validators=[DataRequired(message=lstr.warn_devIDFill),
                                    Length(max=10, message=lstr.warn_devIDLength)],
                        default='YQSH1826')

    dateRange = StringField(lstr.dateRange, validators=[Optional()])
    modeDate = RadioField(lstr.modeDate,
                          choices=[('0', lstr.Day), ('1', lstr.Wek), ('2', lstr.Mon), ('3', lstr.Qtr), ('4', lstr.Yer)],
                          default='0')


