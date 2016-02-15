#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 02-13 创建。试图应用flask_admin的datepicker失败。  -陈
# 02-14 日期域改回StringField，暂时使用直接引入Datetimepick，因为flask-admin的picker无法运行。

from flask.ext.wtf import Form
from wtforms import StringField, RadioField
from wtforms.validators import *
from flask_admin.form.widgets import DatePickerWidget

# 一些默认值方便测试

class form_expenditure(Form):
    user_id = StringField(u'工号', validators=[DataRequired()], default='TPPZLPHY')
    startDate = StringField(u'开始日期', validators=[Optional()] )
    endDate = StringField(u'结束日期', validators=[Optional()] )
    mode_date = RadioField(u'时间模式',
                           choices=[(0, u'日'), (1, u'周'), (2, u'月'), (3, u'季'), (4, u'年')],
                           default=0, coerce=int,)
# 未解决：Jinja2生成的RadioField中value值为字符串而不是整数，所以需要获得输入数据后转换类型。


class form_acperiod(Form):
    user_id = StringField(u'工号', validators=[DataRequired()], default='NIHHXTXQ')
    startDate = StringField(u'开始日期', validators=[Optional()])
    endDate = StringField(u'结束日期', validators=[Optional()])


class form_income(Form):
    dev_id = StringField(u'设备号', validators=[DataRequired()], default='YQSH1826')
    startDate = StringField(u'开始日期', validators=[Optional()])
    endDate = StringField(u'结束日期', validators=[Optional()])
    mode_date = RadioField(u'时间模式',
                           choices=[(0, u'日'), (1, u'周'), (2, u'月'), (3, u'季'), (4, u'年')],
                           default=0, coerce=int,)


