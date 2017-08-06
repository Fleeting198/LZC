#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import operator


def CategoryProcess(ipt_list, fold=True):
    """
    :param ipt_list:输入队列，元素为元组(名称，值)
    """
    # 类型名称为key 数量为val
    vals = {}  # {'title0': val1, 'title1': val2, ...}

    for result in ipt_list:
        vals[str(result[0])] = float(result[1])

    # 若项目数量少，直接返回
    if len(vals) < 4 and not fold:
        return vals

    # 若项目数量较多，将值最小的几个归到其他类中

    sumValue = sum(vals.values())
    list_vals = sorted(vals.items(), key=operator.itemgetter(1), reverse=True)

    cur_count = 0
    tmp_vals = []

    for val in list_vals:
        if cur_count / float(sumValue) < 0.9:
            cur_count += val[1]
            tmp_vals.append(val)

    if cur_count != sumValue:
        tmp_vals.append(('other', sumValue - cur_count))

    list_vals = {}
    for i in range(len(tmp_vals)):
        list_vals[tmp_vals[i][0]] = round(tmp_vals[i][1], 2)

    return list_vals
