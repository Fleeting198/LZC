#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app import db


class device(db.Model):
    dev_id = db.Column(db.String(10), primary_key=True)
    location = db.Column(db.String(40))

    def __init__(self, dev_id, location, grade):
        self.dev_id = dev_id
        self.location = location


class individual(db.Model):
    user_id = db.Column(db.String(8), primary_key=True)
    role = db.Column(db.String(3))
    grade = db.Column(db.String(2))

    def __init__(self, user_id, role, grade):
        self.user_id = user_id
        self.role = role
        self.grade = grade


class acnode(db.Model):
    node_id = db.Column(db.Integer, primary_key=True)
    node_des = db.Column(db.String(40))

    def __init__(self, node_id, node_des):
        self.node_id=node_id
        self.node_des=node_des


class acrec(db.Model):
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

