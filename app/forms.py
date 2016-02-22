#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 02-13 创建。试图应用flask_admin的datepicker失败。
# 02-14 日期域改回StringField，暂时使用直接引入Datetimepick，因为flask-admin的picker无法运行。
# 02-16 Implementing dateRangePicker.
# 02-22 Form 类根据输入重构继承，而不是每个功能定义一个类。

from wtforms import StringField, RadioField, Form
from wtforms.validators import *
import LocalStrings as lstr



class Form_UserDaterange(Form):
    """
    工号日期范围
    """
    userID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                  Length(min=8, max=8, message=lstr.warn_userIDLength)])
    dateRange = StringField(lstr.dateRange, validators=[Optional()])


class Form_UserDaterangemode(Form_UserDaterange):
    """
    在Form_UserDaterange 基础上加上日期模式。
    """
    modeDate = RadioField(lstr.modeDate,
                          choices=[('0', lstr.Day), ('1', lstr.Wek), ('2', lstr.Mon), ('3', lstr.Qtr), ('4', lstr.Yer)],
                          default='0')


class Form_DevDaterange(Form):
    """
    设备号日期范围
    """
    devID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                  Length(max=10, message=lstr.warn_userIDLength)])
    dateRange = StringField(lstr.dateRange, validators=[Optional()])


class Form_DevDaterangemode(Form_UserDaterange):
    """
    Form_DevDaterange 基础上加上日期模式。
    """
    modeDate = RadioField(lstr.modeDate,
                          choices=[('0', lstr.Day), ('1', lstr.Wek), ('2', lstr.Mon), ('3', lstr.Qtr), ('4', lstr.Yer)],
                          default='0')

