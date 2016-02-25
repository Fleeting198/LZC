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
        self.user_id = user_id
        self.role = role
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
    # node_id = db.Column(db.Integer, primary_key=True)
    node_des = db.Column(db.String(40), primary_key=True)
    category = db.Column(db.String(5))

    acrecs = db.relationship('acrec', backref=db.backref('ac_loc'))  # 属于这个地点的所有门禁记录

    def __init__(self, node_id, node_des, category):
        self.node_id=node_id
        self.node_des=node_des
        self.category=category


class acrec(db.Model):
    """
    门禁记录：工号(外键：个体 工号)，日期时间，合法，地点序号(外键：门禁地点 序号)。
    """
    user_id = db.Column(db.String(8), db.ForeignKey('individual.user_id'), primary_key=True)
    ac_datetime = db.Column(db.DateTime, primary_key=True)
    legal = db.Column(db.Integer)

    node_des = db.Column(db.String(40), db.ForeignKey('ac_loc.node_des'))
    # node_id = db.Column(db.Integer, db.ForeignKey('ac_loc.node_id'))

    def __init__(self, user_id, node_des, ac_datetime, legal):
        self.user_id = user_id
        self.node_des = node_des
        self.ac_datetime = ac_datetime
        self.legal = legal

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


class con_water_simp(db.Model):
    """
    消费表的water 类消费子表，为了减小查询时间开销而查询得到
    丢弃了用户id ，设备id 和主键信息
    """
    id = db.Column(db.Integer, primary_key=True)
    con_datetime = db.Column(db.DateTime)
    amount = db.Column(db.DECIMAL(5, 2))

    def __init__(self, con_datetime, amount):
        self.con_datetime = con_datetime
        self.amount = amount