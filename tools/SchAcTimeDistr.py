#!/usr/bin/env python
# coding: UTF-8

from tools.MysqlClient import MysqlClient


class SchAcTimeDistri:
    def __init__(self):
        self.mc = MysqlClient()

    def mainfunc(self):
        sql = "select ac_datetime, category " \
              "from acrec,ac_loc " \
              "where acrec.node_id=ac_loc.node_id " \
              "order by acrec.ac_datetime"
        results = self.mc.query(sql)

        dateList = [result[0] for result in results]
        categoryList = [result[1] for result in results]
        valList = [1] * len(categoryList)

        from app.functions.Pro_TimeDistr import get_time_distribution
        df, dfStat = get_time_distribution(dateList, categoryList, valList)

        from app.helpers import insertDataFrameToDBTable2
        insertDataFrameToDBTable2(df, 'sch_ac_timedistr', self.mc)


if __name__ == '__main__':
    ts = SchAcTimeDistri()
    ts.mainfunc()
