# -*- coding: utf-8 -*-

from sys import float_info
import math
from math import ldexp
from pint.roundmode import roundmode
'''
# Calculate addition, subtraction, multiplication, division and root with rounding mode.

# using exsample
from pint import roundfloat as rf
from pint import roundmode as rdm

# Calculate 0.25 + 0.1 with rounding to up.
rf.rdadd(0.25, 0.1, rdm.up)

# Calculate 0.25 - 0.1 with rounding to down
rf.rdsub(0.25, 0.1, rdm.down)
'''


'''
constants

L = ldexp
M = minus
P = plus
LM969 = ldexp(1, -969)
'''
L27P1 = ldexp(1, 27) + 1
L28 = ldexp(1, 28)
LM28 = ldexp(1, -28)
L53 = ldexp(1, 53)
LM53 = ldexp(1, -53)
L105 = ldexp(1, 105)
LM105 = ldexp(1, -105)
L106 = ldexp(1, 106)
L537 = ldexp(1, 537)
L918 = ldexp(1, 918)
L996 = ldexp(1, 996)
LM969 = ldexp(1, -969)
LM1021 = ldexp(1, -1021)
L1023 = ldexp(1, 1023)
LM1023 = ldexp(1, -1023)
LM1074 = ldexp(1, -1074)
LM53PLM105 = (ldexp(1, -53) + ldexp(1, -105))

def split(a):
    tmp = a * (L27P1)
    x = tmp - (tmp - a)
    y = a - x
    return x, y

# succ and pred by S. M. Rump:
def succ(a):
    abs_a = abs(a)
    if abs_a >= LM969:
        return a + abs_a * LM53PLM105
    if abs_a <= LM1021:
        return a + LM1074
    c = L53 * a
    e = LM53PLM105 * abs(c)
    return (c + e) * LM53

def pred(a):
    abs_a = abs(a)
    if abs_a >= LM969:
        return a - abs_a * LM53PLM105
    if abs_a <= LM1021:
        return a - LM1074
    c = L53 * a
    e = LM53PLM105 * abs(c)
    return (c - e) * LM53

# by Masahide Kashiwagi
# http://verifiedby.me/adiary/029

def fasttwosum(a, b):
    x = a + b
    tmp = x - a
    y = b - tmp
    return x, y

def twosum(a, b):
    arg1 = a
    arg2 = b
    x = arg1 + arg2
    if abs(arg1) > abs(arg2):
        tmp = x - arg1
        y = arg2 - tmp
    else:
        tmp = x - arg2
        y = arg1 - tmp
    return x, y

def twoproduct(a, b):
    arg1 = a
    arg2 = b
    x = arg1 * arg2
    if abs(arg1) > L996:
        arg1fix = arg1 * LM28
        arg2fix = arg2 * L28
    elif abs(arg2) > L996:
        arg1fix = arg1 * L28
        arg2fix = arg2 * LM28
    else:
        arg1fix = arg1
        arg2fix = arg2
    aH, aL = split(arg1fix)
    bH, bL = split(arg2fix)
    if abs(x) > L1023:
        y = aL * bL - ((((x * 0.5) - (aH * 0.5) * bH) * 2. - aL * bH) - aH * bL)
    else:
        y = aL * bL - (((x - aH * bH) - aL * bH) - aH * bL)
    return x, y

def rdadd(a, b, rmode=roundmode.nearest):
    arg1 = a
    arg2 = b
    x, y = twosum(arg1, arg2)
    if rmode == roundmode.up:
        if x == float('inf'):
            return x
        elif x == -float('inf'):
            if arg1 == -float('inf') or arg2 == -float('inf'):
                return x
            else:
                return -float_info.max
        if y > 0:
            x = succ(x)
    elif rmode == roundmode.down:
        if x == float('inf'):
            if arg1 == float('inf') or arg2 == float('inf'):
                return x
            else:
                return float_info.max
        elif x == -float('inf'):
            return x
        if y < 0:
            x = pred(x)
    return x

def rdsub(a, b, rmode=roundmode.nearest):
    return rdadd(a, -b, rmode)

def rdmul(a, b, rmode=roundmode.nearest):
    arg1 = a
    arg2 = b
    x, y = twoproduct(arg1, arg2)
    if rmode == roundmode.up:
        if x == float('inf'):
            return x
        elif x == -float('inf'):
            if math.fabs(arg1) == float('inf') or math.fabs(arg2) == float('inf'):
                return x
            else:
                return -float_info.max
        if abs(x) >= LM969:
            if y > 0:
                x = succ(x)
    elif rmode == roundmode.down:
        if x == float('inf'):
            if math.fabs(arg1) == float('inf') or math.fabs(arg2) == float('inf'):
                return x
            else:
                return float_info.max
        elif x == -float('inf'):
            return x

        if abs(x) >= LM969:
            if y < 0.:
                return pred(x)
        else:
            s1, s2 = twoproduct(arg1 * L537, arg2 * L537)
            t = (x * L537) * L537
            if t > s1 or (t == s1 and s2 < 0.):
                return pred(x)
    return x

def rddiv(a, b, rmode=roundmode.nearest):
    arg1 = a
    arg2 = b
    if rmode == roundmode.up:
        pass
        if (arg1 == 0. or arg2 == 0. or
            math.fabs(arg1) == float('inf') or math.fabs(arg2) == float('inf') or
                arg1 != arg1 or arg2 != arg2):
            return arg1 / arg2
        if arg2 < 0.:
            arg1fix = -arg1
            arg2fix = -arg2
        else:
            arg1fix = arg1
            arg2fix = arg2
        if abs(arg1fix) < LM969:
            if abs(arg2fix) < L918:
                arg1fix *= L105
                arg2fix *= L105
            else:
                if arg1fix < 0.:
                    return 0.
                else:
                    return LM1074
        d = arg1fix / arg2fix
        if d == float('inf'):
            return d
        elif d == -float('inf'):
            return -float_info.max

        x, y = twoproduct(d, arg2fix)
        if x < arg1fix or (x == arg1fix and y < 0.):
            return succ(d)
        return d
    elif rmode == roundmode.down:
        if (arg1 == 0. or arg2 == 0. or
            abs(arg1) == float('inf') or abs(arg2) == float('inf') or
                arg1 != arg1 or arg2 != arg2):
            return arg1 / arg2
        if arg2 < 0.:
            arg1fix = -arg1
            arg2fix = -arg2
        else:
            arg1fix = arg1
            arg2fix = arg2
        if abs(arg1fix) < LM969:
            if abs(arg2fix) < L918:
                arg1fix *= L105
                arg2fix *= L105
            else:
                if arg1fix < 0.:
                    return -LM1074
                else:
                    return 0
        d = arg1fix / arg2fix
        if d == float('inf'):
            return float_info.max
        elif d == -float('inf'):
            return d
        x, y = twoproduct(d, arg2fix)
        if x > arg1fix or (x == arg1fix and y > 0.):
            return pred(d)
        return d

def rdsqrt(x, rmode=roundmode.nearest):
    arg = x
    d = math.sqrt(arg)
    if rmode == roundmode.up:
        if arg < LM969:
            a2 = arg * L106
            d2 = d * L53
            x, y = twoproduct(d2, d2)
            if x < a2 or (x == a2 and y < 0.):
                d = succ(d)
        x, y = twoproduct(d, d)
        if x < arg or (x == arg and y < 0.):
            d = succ(d)
    if rmode == roundmode.down:
        if arg < LM969:
            a2 = arg * L106
            d2 = d * L53
            x, y = twoproduct(d2, d2)
            if x > a2 or (x == a2 and y > 0.):
                d = pred(d)
        x, y = twoproduct(d, d)
        if x > arg or (x == arg and y > 0.):
            d = pred(d)
    return d
