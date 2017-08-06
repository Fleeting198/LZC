#!/usr/bin/env python
# coding: UTF-8

from tools.MysqlClient import MysqlClient


class SchConTimeDistri:
    def __init__(self):
        self.mc = MysqlClient()

    def mainfunc(self):
        sql = "select con_datetime, category, amount " \
              "from consumption,device,dev_loc " \
              "where consumption.dev_id=device.dev_id and device.node_id=dev_loc.node_id " \
              "order by consumption.con_datetime "
        results = self.mc.query(sql)

        dateList = [result[0] for result in results]
        categoryList = [result[1] for result in results]
        valList = [float(result[2]) for result in results]

        from app.functions.Pro_TimeDistr import get_time_distribution
        df, dfStat = get_time_distribution(dateList, categoryList, valList)

        from app.helpers import insertDataFrameToDBTable2
        insertDataFrameToDBTable2(df, 'sch_con_timedistr', self.mc)


if __name__ == '__main__':
    ts = SchConTimeDistri()
    ts.mainfunc()
