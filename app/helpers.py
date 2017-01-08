#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import LocalStrings as lstr

def translate(ipt):
    """根据dict翻译字符串，若字典中不存在则返回原输入
    :param ipt: 要翻译的字符串
    """
    if isinstance(ipt,basestring) and ipt in lstr.dictTrans:
        return lstr.dictTrans[ipt]
    return ipt

def mergeDict(dict1, dict2):
    """dict1 = dict1 + dict2  合并相同的key的值
    :param dict1: 第一个用以合并的字典
    :param dict2: 第二个用以合并的字典
    """
    for k, v in dict2.iteritems():
        dict1[k] = dict1[k] + v if k in dict1 else 1
    return dict1
