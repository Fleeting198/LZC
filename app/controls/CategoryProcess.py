#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import operator

def CategoryProcess(ipt_list):
    """
    :param ipt_list:队列，元素为元组(名称，值)
    """

    vals = {}  # = {'title0': val1, 'title1': val2, ...}
    titles = []  # ['title0', 'title1', ...]

    for result in ipt_list:
        titles.append(str(result[0]))
        # Into tmp_data.
        vals[str(result[0])] = float(result[1])

    # 若项目数量少，直接返回，否则将比例小的归入其他
    if len(vals) < 4: return titles, vals

    titles = []
    list_vals=[]
    total_sum = 0
    for k, v in vals.iteritems():
        list_vals.append({k:v})
        total_sum += v

    list_vals = sorted(vals.iteritems(), key=operator.itemgetter(1), reverse=True)

    cur_count = 0
    tmp_vals = []

    for val in list_vals:
        if cur_count / float(total_sum) < 0.9:
            cur_count += val[1]
            tmp_vals.append(val)
            titles.append(val[0])
    titles.append('other')

    if cur_count != total_sum:
        tmp_vals.append(('other', total_sum - cur_count))

    list_vals = {}
    for i in xrange(len(tmp_vals)):
        list_vals[tmp_vals[i][0]] = round(tmp_vals[i][1],2)

    return titles, list_vals
