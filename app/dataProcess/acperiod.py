# coding=utf-8
#
# 02-12 Built by 陈骏杰
#   输入：某人日期范围内所有门禁
#   处理：依据时间段对门禁时间分类计数
#   输出：时间段标签list，对应门禁平均次数

from datetime import time

def main(mdates):
    mcounts = [0,0,0,0]  # 各时间段的平均门禁计数
    mtimes = map(lambda d: d.time(), mdates)  # 只取时间
    mdates = map(lambda d: d.date(), mdates)
    mdates = list(set(mdates))
    len_mdates = len(mdates)

    # 时间段分布：
    # 23~5 5~12 12~20 20~23
    period = (time(5), time(12), time(20), time(23))

    for i in range(len(mtimes)):
        if mtimes[i] >= period[0] and mtimes[i] < period[1]:
            mcounts[1] += 1
        elif mtimes[i] >= period[1] and mtimes[i] < period[2]:
            mcounts[2] += 1
        elif mtimes[i] >= period[2] and mtimes[i] < period[3]:
            mcounts[3] += 1
        else:
            mcounts[0] += 1

    for i in range(len(mcounts)):
        mcounts[i] = float(mcounts[i])
        mcounts[i] = mcounts[i]/len_mdates if len_mdates != 0 else 0
        mcounts[i] = round(mcounts[i], 2)

    mperiods = ('23点~5点', '5点~12点', '12点~20点', '20点~23点')

    return mperiods, mcounts