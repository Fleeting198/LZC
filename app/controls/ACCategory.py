#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 02-20 Built


def ACCategory(inp):
    outp = {}
    for result in inp:
        if str(result) not in outp:
            outp[str(result)] = 1
        else:
            outp[str(result)] += 1

    return outp