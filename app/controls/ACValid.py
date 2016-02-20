#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 02-20 Built
# 输入：legal 数组；输出：{'valid': , 'invalid': }


def ACValid(inp):
    outp = {}
    for result in inp:
        if str(result) not in outp:
            outp[str(result)] = 1
        else:
            outp[str(result)] += 1

    outp['valid'] = outp.pop('1')
    outp['invalid'] = outp.pop('0')

    return outp
