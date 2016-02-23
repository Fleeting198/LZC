#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import LocalStrings as lstr

def translate(ipt):
    if ipt in lstr.dictTrans:
        return lstr.dictTrans[ipt]
    return ipt