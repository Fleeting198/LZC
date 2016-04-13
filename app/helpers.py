#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import LocalStrings as lstr

def translate(ipt):
    """根据dict翻译字符串，若字典中不存在则返回原输入
    :param ipt: 要翻译的字符串
    """
    if ipt in lstr.dictTrans:
        return lstr.dictTrans[ipt]
    return ipt