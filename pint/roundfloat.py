# -*- coding: utf-8 -*-


from sys import float_info
import math
from math import ldexp
from pint.roundmode import roundmode as rdm

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
def split(a):
    tmp = a * (ldexp(1, 27) + 1)
    x = tmp - (tmp - a)
    y = a - x
    return x, y

# succ and pred by S. M. Rump:
def succ(a):
    abs_a = abs(a)
    if abs_a >= ldexp(1, -969):
        return a + abs_a * (ldexp(1, -53) + ldexp(1, -105))
    if abs_a <= ldexp(1, -1021):
        return a + ldexp(1, -1074)
    c = ldexp(1, 53) * a
    e = (ldexp(1, -53) + ldexp(1, -105)) * abs(c)
    return (c + e) * ldexp(1, -53)

def pred(a):
    abs_a = abs(a)
    if abs_a >= ldexp(1, -969):
        return a - abs_a * (ldexp(1, -53) + ldexp(1, -105))
    if abs_a <= ldexp(1, -1021):
        return a - ldexp(1, -1074)
    c = ldexp(1, 53) * a
    e = (ldexp(1, -53) + ldexp(1, -105)) * abs(c)
    return (c - e) * ldexp(1, -53)

# by Masahide Kashiwagi
# http://verifiedby.me/adiary/029

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
    if abs(arg1) > 2.**996:
        arg1fix = arg1 * 2.**(-28)
        arg2fix = arg2 * 2.**(28)
    elif abs(arg2) > 2.**(996):
        arg1fix = arg1 * 2.**(28)
        arg2fix = arg2 * 2.**(-28)
    else:
        arg1fix = arg1
        arg2fix = arg2
    aH, aL = split(arg1fix)
    bH, bL = split(arg2fix)
    if abs(x) > 2.**1023:
        y = aL * bL - ((((x * 0.5) - (aH * 0.5) * bH) * 2. - aL * bH) - aH * bL)
    else:
        y = aL * bL - (((x - aH * bH) - aL * bH) - aH * bL)
    return x, y

def rdadd(a, b, rmode=rdm.nearest):
    arg1 = a
    arg2 = b
    x, y = twosum(arg1, arg2)
    if rmode == rdm.up:
        if x == float('inf'):
            return x
        elif x == -float('inf'):
            if arg1 == -float('inf') or arg2 == -float('inf'):
                return x
            else:
                return -float_info.max
        if y > 0:
            x = succ(x)
    elif rmode == rdm.down:
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

def rdsub(a, b, rmode=rdm.nearest):
    return rdadd(a, -b, rmode)

def rdmul(a, b, rmode=rdm.nearest):
    arg1 = a
    arg2 = b
    x, y = twoproduct(arg1, arg2)
    if rmode == rdm.up:
        if x == float('inf'):
            return x
        elif x == -float('inf'):
            if math.fabs(arg1) == float('inf') or math.fabs(arg2) == float('inf'):
                return x
            else:
                return -float_info.max
        if abs(x) >= 2.**(-969):
            if y > 0:
                x = succ(x)
    elif rmode == rdm.down:
        if x == float('inf'):
            if math.fabs(arg1) == float('inf') or math.fabs(arg2) == float('inf'):
                return x
            else:
                return float_info.max
        elif x == -float('inf'):
            return x

        if abs(x) >= 2.**(-969):
            if y < 0.:
                return pred(x)
        else:
            s1, s2 = twoproduct(arg1 * 2.**537, arg2 * 2.**537)
            t = (x * 2.**537) * 2.**537
            if t > s1 or (t == s1 and s2 < 0.):
                return pred(x)
    return x

def rddiv(a, b, rmode=rdm.nearest):
    arg1 = a
    arg2 = b
    if rmode == rdm.up:
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
        if abs(arg1fix) < 2.**(-969):
            if abs(arg2fix) < 2.**918:
                arg1fix *= 2.**105
                arg2fix *= 2.**105
            else:
                if arg1fix < 0.:
                    return 0.
                else:
                    return 2.**(-1074)
        d = arg1fix / arg2fix
        if d == float('inf'):
            return d
        elif d == -float('inf'):
            return -float_info.max

        x, y = twoproduct(d, arg2fix)
        if x < arg1fix or (x == arg1fix and y < 0.):
            return succ(d)
        return d
    elif rmode == rdm.down:
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
        if abs(arg1fix) < 2.**(-969):
            if abs(arg2fix) < 2.**918:
                arg1fix *= 2.**105
                arg2fix *= 2.**105
            else:
                if arg1fix < 0.:
                    return -2.**(-1074)
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

def rdsqrt(x, rmode=rdm.nearest):
    arg = x
    d = math.sqrt(arg)
    if rmode == rdm.up:
        if arg < 2.**(-969):
            a2 = arg * 2.**106
            d2 = d * 2.**53
            x, y = twoproduct(d2, d2)
            if x < a2 or (x == a2 and y < 0.):
                d = succ(d)
        x, y = twoproduct(d, d)
        if x < arg or (x == arg and y < 0.):
            d = succ(d)
    if rmode == rdm.down:
        if arg < 2.**(-969):
            a2 = arg * 2.**106
            d2 = d * 2.**53
            x, y = twoproduct(d2, d2)
            if x > a2 or (x == a2 and y > 0.):
                d = pred(d)
        x, y = twoproduct(d, d)
        if x > arg or (x == arg and y > 0.):
            d = pred(d)
    return d
