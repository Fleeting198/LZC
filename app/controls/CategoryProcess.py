#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def CategoryProcess(results):
    vals = {}  # = {'title0': val1, 'title1': val2, ...}
    titles = []  # ['title0', 'title1', ...]

    for result in results:
        # Into titles.
        if result[0] not in titles:
            titles.append(str(result[0]))
        # Into tmp_data.
        vals[str(result[0])] = float(result[1])

    return titles, vals
