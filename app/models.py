#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app import db

class device(db.Model):
    """
    刷卡机：设备号，地点序号(外键：设备地点表 序号)
    """
    dev_id = db.Column(db.String(10), primary_key=True)
    node_id = db.Column(db.String, db.ForeignKey('dev_loc.node_id'))

    consumptions = db.relationship('consumption', backref=db.backref('device'))  # 设备所有消费记录

    def __init__(self, dev_id, node_id):
        self.dev_id = dev_id
        self.node_id = node_id


class individual(db.Model):
    """
    个体：工号，角色[老师，学生，其他]，年级[只有学生描述年级]
    """
    user_id = db.Column(db.String(8), primary_key=True)
    role = db.Column(db.String(3))
    grade = db.Column(db.String(2))

    acrecs = db.relationship('acrec', backref=db.backref('individual'))  # 此工号所有门禁记录
    consumptions = db.relationship('consumption', backref=db.backref('individual'))  # 此工号所有消费记录

    def __init__(self, user_id, role, grade):
        self.set_user_id(user_id)
        self.set_role(role)
        self.set_grade(grade)

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_role(self, role):
        self.role = role

    def set_grade(self, grade):
        if self.role == '老师' or '其他':
            self.grade = self.role
        else:
            self.grade = grade


class dev_loc(db.Model):
    """
    设备地点：地点序号(自增)，地点描述。
    分类：
    """
    node_id = db.Column(db.Integer, primary_key=True)
    node_des = db.Column(db.String(40))
    category = db.Column(db.String(5))

    devices = db.relationship('device', backref=db.backref('dev_loc'))  # 属于这个地点的所有设备

    def __init__(self, node_id, node_des, category):
        self.node_id = node_id
        self.node_des = node_des
        self.category = category


class ac_loc(db.Model):
    """
    门禁地点：地点序号(自增)，地点描述。
    分类：
    """
    node_id = db.Column(db.Integer, primary_key=True)
    node_des = db.Column(db.String(40))
    category = db.Column(db.String(5))

    acrecs = db.relationship('acrec', backref=db.backref('ac_loc'))  # 属于这个地点的所有门禁记录

    def __init__(self, node_id, category):
        self.node_id=node_id
        self.category=category


class acrec(db.Model):
    """
    门禁记录：工号(外键：个体 工号)，日期时间，合法，地点序号(外键：门禁地点 序号)。
    """
    user_id = db.Column(db.String(8), db.ForeignKey('individual.user_id'), primary_key=True)
    ac_datetime = db.Column(db.DateTime, primary_key=True)
    legal = db.Column(db.Integer)
    node_id = db.Column(db.Integer, db.ForeignKey('ac_loc.node_id'))

    def __init__(self, user_id, node_id, ac_datetime, legal):
        self.user_id = user_id
        self.ac_datetime = ac_datetime
        self.legal = legal
        self.node_id = node_id

    # legal 为1 合法，否则非法。
    def is_legal(self):
        return True if self.legal == 1 else False


class consumption(db.Model):
    """
    消费记录：工号(外键：个体 工号)，日期时间，设备号(外键：设备 设备号)，金额
    """
    user_id = db.Column(db.String(8), db.ForeignKey('individual.user_id'), primary_key=True)
    con_datetime = db.Column(db.DateTime, primary_key=True)
    dev_id = db.Column(db.String(10), db.ForeignKey('device.dev_id'))
    amount = db.Column(db.DECIMAL(5, 2))

    def __init__(self, user_id, dev_id, con_datetime, amount):
        self.user_id = user_id
        self.dev_id = dev_id
        self.con_datetime = con_datetime
        self.amount = amount


class acr_friendlist(db.Model):
    """
    来自门禁表的人际关系字典
    """
    user_id = db.Column(db.String(8), db.ForeignKey('individual.user_id'), primary_key=True)
    str_relation = db.Column(db.String)

    def __init__(self, user_id, str_relation):
        self.user_id = user_id
        self.str_relation = str_relation

    def str_relation_to_dict(self):
        dict_relation = eval(self.str_relation)
        return dict_relation


class conability(db.Model):
    """
    个人月消费能力：工号,月平均消费金额(保留2位小数),角色[老师，学生]
    """
    user_id = db.Column(db.String(8), primary_key=True)
    amount_avg = db.Column(db.DECIMAL())
    role = db.Column(db.String(3))

class conability_line(db.Model):
    """
    月消费能力统计：月平均消费金额(取整),人数,角色[老师，学生]
    """
    amount = db.Column(db.Integer(), primary_key=True)
    num = db.Column(db.Integer())
    role = db.Column(db.String(3))

class penalty(db.Model):
    """
    个体滞纳金缴纳情况：工号,缴纳总额
    """
    user_id = db.Column(db.String(8), primary_key=True)
    amount = db.Column(db.DECIMAL())

class penalty_line(db.Model):
    """
    滞纳金缴纳情况统计：缴纳总额(取整),人数
    """
    amount = db.Column(db.Integer(), primary_key=True)
    num = db.Column(db.Integer())

#  用于查询食物和用水消费时间分布的现成表
class con_food_12m(db.Model):
    con_axis = db.Column(db.Integer(), primary_key=True)
    sum_amount = db.Column(db.DECIMAL())

class con_food_7d(db.Model):
    con_axis = db.Column(db.Integer(), primary_key=True)
    sum_amount = db.Column(db.DECIMAL())

class con_food_24h(db.Model):
    con_axis = db.Column(db.Integer(), primary_key=True)
    sum_amount = db.Column(db.DECIMAL())

class con_water_12m(db.Model):
    con_axis = db.Column(db.Integer(), primary_key=True)
    sum_amount = db.Column(db.DECIMAL())

class con_water_7d(db.Model):
    con_axis = db.Column(db.Integer(), primary_key=True)
    sum_amount = db.Column(db.DECIMAL())

class con_water_24h(db.Model):
    con_axis = db.Column(db.Integer(), primary_key=True)
    sum_amount = db.Column(db.DECIMAL())


# 用以查询图书馆、科研、教学楼访问次数的现成表
class ac_count(db.Model):
    user_id = db.Column(db.Integer(), primary_key=True)
    count_acad = db.Column(db.Integer())
    count_lib = db.Column(db.Integer())
    count_sci = db.Column(db.Integer())

    def __init__(self, user_id, count_acad, count_lib, count_sci):
        self.user_id = user_id
        self.count_acad = count_acad
        self.count_lib = count_lib
        self.count_sci = count_sci

    def get_sum(self):
        return self.count_acad + self.count_sci + self.count_lib

    def get_sum_per_month(self):
        return self.get_sum() / 12.0
