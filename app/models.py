from app import db

class Device(db.Model):
    dev_id = db.Column(db.String(10), primary_key=True)
    location = db.Column(db.String(40))

class Individual(db.Model):
    user_id = db.Column(db.String(8), primary_key=True)
    role = db.Column(db.String(3))
    grade = db.Column(db.String(2))

class ACRec(db.Model):
    node_id = db.Column(db.Integer, primary_key=True)
    node_des = db.Column(db.String(40))
    ac_datetime = db.Column(db.DateTime)

class consumption(db.Model):
    user_id = db.Column(db.String(8), primary_key=True)
    dev_id = db.Column(db.String(10))
    con_datetime = db.Column(db.DateTime)
    amount = db.Column(db.DECIMAL(5, 2))

    def __init__(self, user_id, dev_id, con_datetime, amount):
        self.user_id = user_id
        self.dev_id = dev_id
        self.con_datetime = con_datetime
        self.amount = amount

    def __repr__(self):
        return '<ID: %r; Device: %r; Date: %r; Amount: %r>' \
               % (self.user_id, self.dev_id, self.con_datetime, self.amount)
