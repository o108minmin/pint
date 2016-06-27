#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import IntEnum

class roundmode(IntEnum):
    '''
    rounding mode such as INTLAB
    '''
    up = 1
    nearest = 0
    down = -1
