#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app import db


class device(db.Model):
    """
    刷卡机：设备号，地点序号(外键：设备地点表 序号)
    """
    dev_id = db.Column(db.String(10), primary_key=True)
    node_id = db.Column(db.String, db.ForeignKey('devnode.node_id'))

    devnode = db.relationship('devnode', backref=db.backref('device'))

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

    def __init__(self, user_id, role, grade):
        self.user_id = user_id
        self.role = role
        self.grade = grade


class devnode(db.Model):
    """
    设备地点：地点序号(自增)，地点描述。
    分类：
    """
    node_id = db.Column(db.Integer, primary_key=True)
    node_des = db.Column(db.String(40))

    def __init__(self, node_id, node_des):
        self.node_id = node_id
        self.node_des = node_des


class acnode(db.Model):
    """
    门禁地点：地点序号(自增)，地点描述。
    分类：
    """
    node_id = db.Column(db.Integer, primary_key=True)
    node_des = db.Column(db.String(40))

    def __init__(self, node_id, node_des):
        self.node_id=node_id
        self.node_des=node_des


class acrec(db.Model):
    """
    门禁记录：工号(外键：个体 工号)，日期时间，合法，地点序号(外键：门禁地点 序号)
    """
    user_id = db.Column(db.String(8), db.ForeignKey('individual.user_id'), primary_key=True)
    ac_datetime = db.Column(db.DateTime, primary_key=True)
    legal = db.Column(db.Integer)
    node_id = db.Column(db.Integer, db.ForeignKey('acnode.node_id'))

    individual = db.relationship('individual', backref=db.backref('acrec'))
    acnode = db.relationship('acnode',backref=db.backref('acrec'))

    def __init__(self, user_id, node_id, ac_datetime, legal):
        self.user_id = user_id
        self.node_id = node_id
        self.ac_datetime = ac_datetime
        self.legal = legal


class consumption(db.Model):
    """
    消费记录：工号(外键：个体 工号)，日期时间，设备号(外键：设备 设备号)，金额
    """
    user_id = db.Column(db.String(8), db.ForeignKey('individual.user_id'), primary_key=True )
    con_datetime = db.Column(db.DateTime, primary_key=True)
    dev_id = db.Column(db.String(10), db.ForeignKey('device.dev_id'))
    amount = db.Column(db.DECIMAL(5, 2))

    individual = db.relationship('individual', backref=db.backref('consumption'))
    device = db.relationship('device', backref=db.backref('consumption'))

    def __init__(self, user_id, dev_id, con_datetime, amount):
        self.user_id = user_id
        self.dev_id = dev_id
        self.con_datetime = con_datetime
        self.amount = amount

