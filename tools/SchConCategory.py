#!/usr/bin/env python
# coding: utf-8

from tools.MysqlClient import MysqlClient


class SchConCategory():
    def __init__(self):
        self.mc = MysqlClient()

    def mainFunc(self):
        sql = "select dev_loc.category, sum(consumption.amount), count(*) " \
              "from consumption, device, dev_loc " \
              "where consumption.dev_id=device.dev_id and device.node_id=dev_loc.node_id " \
              "group by dev_loc.category"
        results = self.mc.query(sql)
        for result in results:
            category = str(result[0])
            amount = float(result[1])
            count = int(result[2])

            sql = "insert into sch_con_category (category,amount,count) values ('%s',%f,%d)" % (category, amount, count)

            # 这句插入不知道为什么不起作用
            self.mc.query(sql)
            print sql
            print category,amount,count

if __name__ == '__main__':
    pj=SchConCategory()
    pj.mainFunc()