# coding:utf-8
# 02-13 创建。试图应用flask_admin的datepicker失败。  -陈

from flask_wtf import Form
from wtforms import StringField, DateTimeField, DateField, RadioField
from wtforms.validators import DataRequired
from flask_admin.form.widgets import DatePickerWidget

# 一些默认值方便测试

class form_expenditure(Form):
    user_id = StringField(u'工号', validators=[DataRequired()], default='TPPZLPHY')
    startDate = DateField(u'开始日期')
    endDate = DateField(u'结束日期')
    mode_date = RadioField(u'时间模式', choices=[(0, u'日'), (1, u'周'), (2, u'月'), (3, u'季'), (4, u'年')], default=0)


class form_acperiod(Form):
    user_id = StringField(u'工号', validators=[DataRequired()], default='TPPZLPHY')
    startDate = DateField(u'开始日期')
    endDate = DateField(u'结束日期')


class form_income(Form):
    dev_id = StringField(u'设备号', validators=[DataRequired()], default='YQSH1826')
    startDate = DateField(u'开始日期')
    endDate = DateField(u'结束日期')
    mode_date = RadioField(u'时间模式', choices=[(0, u'日'), (1, u'周'), (2, u'月'), (3, u'季'), (4, u'年')],default=0)

