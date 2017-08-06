#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app import db


class device(db.Model):
    """刷卡机：设备号，地点序号(外键：设备地点表 序号)
    """
    dev_id = db.Column(db.String(10), primary_key=True)
    node_id = db.Column(db.String, db.ForeignKey('dev_loc.node_id'))

    consumptions = db.relationship('consumption', backref=db.backref('device'))  # 设备所有消费记录


class individual(db.Model):
    """个体：卡号，角色[老师，学生，其他]，年级[只有学生描述年级]
    """
    user_id = db.Column(db.String(8), primary_key=True)  # 卡号
    role = db.Column(db.String(3))  # 角色
    grade = db.Column(db.String(2))  # 年级

    acrecs = db.relationship('acrec', backref=db.backref('individual'))  # 此卡号所有门禁记录
    consumptions = db.relationship('consumption', backref=db.backref('individual'))  # 此卡号所有消费记录


class dev_loc(db.Model):
    """设备地点：地点序号(自增)，地点描述。
    分类：
    """
    node_id = db.Column(db.Integer, primary_key=True)
    node_des = db.Column(db.String(40))
    category = db.Column(db.String(5))

    devices = db.relationship('device', backref=db.backref('dev_loc'))  # 属于这个地点的所有设备


class ac_loc(db.Model):
    """门禁地点：地点序号(自增)，地点描述。
    分类：
    """
    node_id = db.Column(db.Integer, primary_key=True)
    node_des = db.Column(db.String(40))
    category = db.Column(db.String(5))

    acrecs = db.relationship('acrec', backref=db.backref('ac_loc'))  # 属于这个地点的所有门禁记录


class acrec(db.Model):
    """门禁记录：卡号(外键：个体 卡号)，日期时间，合法，地点序号(外键：门禁地点 序号)。
    """
    user_id = db.Column(db.String(8), db.ForeignKey('individual.user_id'), primary_key=True)
    ac_datetime = db.Column(db.DateTime, primary_key=True)
    legal = db.Column(db.Integer)
    node_id = db.Column(db.Integer, db.ForeignKey('ac_loc.node_id'))

    # legal 为1 合法，否则非法。
    def is_legal(self):
        return True if self.legal == 1 else False


class consumption(db.Model):
    """消费记录：卡号(外键：个体 卡号)，日期时间，设备号(外键：设备 设备号)，金额
    """
    user_id = db.Column(db.String(8), db.ForeignKey('individual.user_id'), primary_key=True)
    con_datetime = db.Column(db.DateTime, primary_key=True)
    dev_id = db.Column(db.String(10), db.ForeignKey('device.dev_id'))
    amount = db.Column(db.DECIMAL(5, 2))


class sch_con_datetrend(db.Model):
    id_date = db.Column(db.Date, primary_key=True)
    discipline = db.Column(db.DECIMAL(5, 2))
    # recharge = db.Column(db.DECIMAL(5, 2))
    food = db.Column(db.DECIMAL(5, 2))
    sport = db.Column(db.DECIMAL(5, 2))
    water = db.Column(db.DECIMAL(5, 2))
    shop = db.Column(db.DECIMAL(5, 2))
    study = db.Column(db.DECIMAL(5, 2))
    med = db.Column(db.DECIMAL(5, 2))
    none = db.Column(db.DECIMAL(5, 2))


class sch_ac_datetrend(db.Model):
    id_date = db.Column(db.Date, primary_key=True)
    dorm = db.Column(db.Integer)
    sci = db.Column(db.Integer)
    acad = db.Column(db.Integer)
    sport = db.Column(db.Integer)
    lib = db.Column(db.Integer)
    med = db.Column(db.Integer)
    admin = db.Column(db.Integer)
    none = db.Column(db.Integer)


class sch_con_timedistr(db.Model):
    id_time = db.Column(db.Date, primary_key=True)
    discipline = db.Column(db.DECIMAL(5, 2))
    # recharge = db.Column(db.DECIMAL(5, 2))
    food = db.Column(db.DECIMAL(5, 2))
    sport = db.Column(db.DECIMAL(5, 2))
    water = db.Column(db.DECIMAL(5, 2))
    shop = db.Column(db.DECIMAL(5, 2))
    study = db.Column(db.DECIMAL(5, 2))
    med = db.Column(db.DECIMAL(5, 2))
    none = db.Column(db.DECIMAL(5, 2))


class sch_ac_timedistr(db.Model):
    id_time = db.Column(db.Integer, primary_key=True)
    dorm = db.Column(db.Integer)
    sci = db.Column(db.Integer)
    acad = db.Column(db.Integer)
    sport = db.Column(db.Integer)
    lib = db.Column(db.Integer)
    med = db.Column(db.Integer)
    admin = db.Column(db.Integer)
    none = db.Column(db.Integer)


class ac_relation_confdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    left_user_id = db.Column(db.String)
    right_user_id = db.Column(db.String)
    suppCount = db.Column(db.Integer)
    confRate = db.Column(db.Float)


class conability(db.Model):
    """个人月消费能力：卡号,月平均消费金额(保留2位小数),角色[老师，学生]
    """
    user_id = db.Column(db.String(8), primary_key=True)
    amount_avg = db.Column(db.DECIMAL())
    role = db.Column(db.String(3))


class conability_line(db.Model):
    """月消费能力统计：月平均消费金额(取整),人数,角色[老师，学生]
    """
    amount = db.Column(db.Integer(), primary_key=True)
    num = db.Column(db.Integer())
    role = db.Column(db.String(3))


class penalty_line(db.Model):
    """滞纳金缴纳情况统计：缴纳总额(取整),人数
    """
    amount = db.Column(db.Integer(), primary_key=True)
    num = db.Column(db.Integer())


# 用于查询食物和用水消费时间分布的现成表
class con_food_1440i(db.Model):
    con_axis = db.Column(db.Time, primary_key=True)
    sum_amount = db.Column(db.DECIMAL())


class con_food_12m(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sum_amount = db.Column(db.DECIMAL())


class con_food_7d(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sum_amount = db.Column(db.DECIMAL())


class con_food_24h(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sum_amount = db.Column(db.DECIMAL())


class con_water_1440i(db.Model):
    con_axis = db.Column(db.Time, primary_key=True)
    sum_amount = db.Column(db.DECIMAL())


class con_water_12m(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sum_amount = db.Column(db.DECIMAL())


class con_water_7d(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sum_amount = db.Column(db.DECIMAL())


class con_water_24h(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sum_amount = db.Column(db.DECIMAL())


class ac_study(db.Model):
    user_id = db.Column(db.String(8), primary_key=True)
    count_acad = db.Column(db.Integer())
    count_lib = db.Column(db.Integer())
    count_sci = db.Column(db.Integer())

    def count_study(self):
        return self.count_lib + self.count_sci + self.count_acad


class con_statistics(db.Model):
    user_id = db.Column(db.String(8), primary_key=True)
    total_vals = db.Column(db.Float)  # 消费总金额
    total_times = db.Column(db.Integer)  # 消费总次数
    per = db.Column(db.Float)
