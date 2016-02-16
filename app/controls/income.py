#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# 02-12 Built by 陈骏杰  复制expenditure.py
#   输入：日期和对应消费增量，日期模式。
#   输出：符合对应模式的日期、连续总计收入（初始量0 + 增量）、节点收入
#
#   模式：日0，周1，月2，季3，年4。
#   完成了日、月、年，未做周、季。


def main(mdates, mamounts, mode_date):
    # 日期降维，仅用字符串切片处理年、月。
    if mode_date == 0:
        mdates = map(lambda d: d.date(), mdates)
    elif mode_date == 2:
        mdates = map(lambda d: str(d.date())[:7], mdates)
    elif mode_date == 4:
        mdates = map(lambda d: str(d.date())[:4], mdates)

    i = 1
    while i < len(mdates):  # 每轮循环都要获取长度
        # 取当前和前一个记录的日期（天）
        # 若日期相同，合并日期和对应增量
        if mdates[i] == mdates[i - 1]:
            mdates = mdates[:i - 1] + mdates[i:]  # 日期去除
            mamounts[i] += mamounts[i - 1]  # 增量合并
            mamounts = mamounts[:i - 1] + mamounts[i:]  # 增量去除
        else:
            i += 1

    # 保存节点支出
    mamounts_point = mamounts[:]
    # 累加连续支出
    for i in range(1, len(mamounts)):
        mamounts[i] += mamounts[i - 1]

    mdates = map(lambda x: str(x), mdates)
    mamounts = map(lambda x: float(x), mamounts)
    mamounts_point = map(lambda x: float(x), mamounts_point)

    return mdates, mamounts, mamounts_point