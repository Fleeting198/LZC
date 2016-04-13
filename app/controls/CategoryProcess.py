#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import operator

def CategoryProcess(results):
    vals = {}  # = {'title0': val1, 'title1': val2, ...}
    titles = []  # ['title0', 'title1', ...]

    for result in results:
        # Into titles.
        if result[0] not in titles:
            titles.append(str(result[0]))
        # Into tmp_data.
        vals[str(result[0])] = float(result[1])

    if len(vals) < 4: return titles, vals

    titles = []
    list_vals=[]
    total_sum = 0
    for k, v in vals.iteritems():
        list_vals.append({k:v})
        total_sum += v

    list_vals = sorted(vals.iteritems(), key=operator.itemgetter(1), reverse=True)

    cur_count = 0
    final_vals = []
    for i in range(len(list_vals)):
        if  cur_count/float(total_sum) < 0.9 :
            cur_count += list_vals[i][1]
            final_vals.append(list_vals[i])
            titles.append(list_vals[i][0])
    titles.append('other')

    if cur_count != total_sum:
        final_vals.append(('other', total_sum - cur_count))

    vals = {}
    for i in range(len(final_vals)):
        vals[final_vals[i][0]] = round(final_vals[i][1],2)

    return titles, vals
