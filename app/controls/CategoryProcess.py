#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import LocalStrings as lstr


def CategoryProcess(results):
    tmp_data = {}  # 暂时用以累加数据 {'title0': val1, 'title1': val2, ...}
    titles = []  # ['title0', 'title1', ...]
    seriesData = []  # [{value: , name: }, {value: , name: }, ...]
    # trans = {'food': lstr.food, 'water': lstr.water}

    for result in results:
        # Into titles.
        if result[0] not in titles:
            titles.append(str(result[0]))
        # Into tmp_data.
        tmp_data[str(result[0])] = float(result[1])

    print tmp_data

    # From tmp_data to seriesData.
    for k, v in tmp_data.iteritems():
        # 汉化seriesData 中的lable。
        k = translate(k)
        seriesData.append({'value': v, 'name': k})

    # 汉化titles。
    titles = [translate(title) for title in titles]

    return titles, seriesData


def translate(ipt):
    if ipt in lstr.dictTrans:
        return lstr.dictTrans[ipt]
    return ipt