#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from wtforms import StringField, RadioField, Form
from wtforms.validators import *
import LocalStrings as lstr

class Form_Accategory(Form):
    userID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                  Length(min=8, max=8, message=lstr.warn_userIDLength)])
    dateRange = StringField(lstr.dateRange, validators=[Optional()])

class Form_Acperiodcate(Form):
    userID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                  Length(min=8, max=8, message=lstr.warn_userIDLength)])
    dateRange = StringField(lstr.dateRange, validators=[Optional()])
    modeDate = RadioField(lstr.modeDate,
                      choices=[('0', lstr.opts_modeDate[0]), ('1', lstr.opts_modeDate[1]), ('2', lstr.opts_modeDate[2]),
                               ('3', lstr.opts_modeDate[3]), ], default='2')

class Form_Acvalid(Form):
    userID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                  Length(min=8, max=8, message=lstr.warn_userIDLength)])
    dateRange = StringField(lstr.dateRange, validators=[Optional()])

class Form_Conability(Form):
    userID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                  Length(min=8, max=8, message=lstr.warn_userIDLength)])

class Form_Penalty(Form):
    userID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                  Length(min=8, max=8, message=lstr.warn_userIDLength)])


class Form_Concategory(Form):
    userID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                  Length(min=8, max=8, message=lstr.warn_userIDLength)])
    dateRange = StringField(lstr.dateRange, validators=[Optional()])


class Form_Conwatertime(Form):
    modeTime = RadioField(lstr.modeTime, choices=[('0', lstr.opts_modeTime[0]), ('1', lstr.opts_modeTime[1]),
                                                  ('2', lstr.opts_modeTime[2]), ('3', lstr.opts_modeTime[3]),
                                                  ('4', lstr.opts_modeTime[4])], default='0')
class Form_FoodIncome(Form):
    modeTime = RadioField(lstr.modeTime, choices=[('0', lstr.opts_modeTime[0]), ('1', lstr.opts_modeTime[1]),
                                                  ('2', lstr.opts_modeTime[2]), ('3', lstr.opts_modeTime[3]),
                                                  ('4', lstr.opts_modeTime[4])], default='0')


class Form_Expenditure(Form):
    userID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                  Length(min=8, max=8, message=lstr.warn_userIDLength)])
    dateRange = StringField(lstr.dateRange, validators=[Optional()])
    modeDate = RadioField(lstr.modeDate, choices=[('0', lstr.opts_modeDate[0]), ('1', lstr.opts_modeDate[1]),
                                                  ('2', lstr.opts_modeDate[2]), ('3', lstr.opts_modeDate[3]), ],
                          default='2')
    modeTime = RadioField(lstr.modeTime, choices=[('0', lstr.opts_modeTime[0]), ('1', lstr.opts_modeTime[1]),
                                                  ('2', lstr.opts_modeTime[2])], default='0')




class Form_Income(Form):
    devID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                 Length(max=10, message=lstr.warn_userIDLength)])
    dateRange = StringField(lstr.dateRange, validators=[Optional()])
    modeDate = RadioField(lstr.modeDate, choices=[('0', lstr.opts_modeDate[0]), ('1', lstr.opts_modeDate[1]),
                                                  ('2', lstr.opts_modeDate[2]), ('3', lstr.opts_modeDate[3])],
                          default='2')
    modeTime = RadioField(lstr.modeTime, choices=[('0', lstr.opts_modeTime[0]), ('1', lstr.opts_modeTime[1]),
                                                  ('2', lstr.opts_modeTime[2])], default='0')

class Form_Relation(Form):
    userID = StringField(lstr.userID, validators=[DataRequired(message=lstr.warn_userIDFill),
                                                  Length(min=8, max=8, message=lstr.warn_userIDLength)])
