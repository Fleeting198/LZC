#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def CategoryProcess(results):
    tmp_data = {}  # 暂时用以累加数据 {'title0': val1, 'title1': val2, ...}
    titles = []  # ['title0', 'title1', ...]
    seriesData = []  # [{value: , name: }, {value: , name: }, ...]

    for result in results:
        # Into titles.
        if result[0] not in titles:
            titles.append(str(result[0]))
        # Into tmp_data.
        tmp_data[str(result[0])] = float(result[1])

    # From tmp_data to seriesData.
    for k, v in tmp_data.iteritems():
        seriesData.append({'value': v, 'name': k})

    return titles, seriesData


