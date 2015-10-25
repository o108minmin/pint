# -*- coding: utf-8 -*-
# pint
# python interval library
# version Pre-Alpha 0.1.2

# Copyright (c) 2015 o108minmin

import sys as __sys__
import math as __math__
from enum import IntEnum as __IntEnum__


class roundmode(__IntEnum__):
    up = 1
    nearest = 0
    down = -1


class roundfloat:

    def split(a):
        tmp = a * (2**27 + 1)
        x = tmp - (tmp - a)
        y = a - x
        return x, y

    # succ and pred by S. M. Rump, P. Zimmermann, S. Boldo and G. Melquiond:
    def succ(a):
        absa = abs(a)
        if absa >= 2.**(-969):
            return a + absa * (2.**(-53) + 2.**(-105))
        if absa < 2.**(-1021):
            return a + absa * 2.**(-1074)
        c = 2.**(53) * a
        e = (2.**(-53) + 2.**(-105)) * abs(c)
        return (c + e) * 2.**(-53)

    def pred(a):
        absa = abs(a)
        if absa >= 2.**(-969):
            return a - absa * (2.**(-53) + 2.**(-105))
        if absa < 2.**(-1021):
            return a - absa * 2.**(-1074)
        c = 2.**(53) * a
        e = (2.**(-53) + 2.**(-105)) * abs(c)
        return (c - e) * 2.**(-53)

    # by Masahide Kashiwagi
    # 最近点丸めによる方向付き丸めのエミュレート
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
        arg1SplitUp, arg1SplitDown = roundfloat.split(arg1fix)
        arg2SplitUp, arg2SplitDown = roundfloat.split(arg2fix)
        if abs(x) > 2.**1023:
            y = arg1SplitDown * arg2SplitDown - \
                ((((x * 0.5) - (arg1SplitUp * 0.5) * arg2SplitUp) * 2. -
                  arg1SplitDown * arg2SplitUp) - arg1SplitUp * arg2SplitDown)
        else:
            y = arg1SplitDown * arg2SplitDown - \
                (((x - arg1SplitUp * arg2SplitUp) - arg1SplitDown *
                  arg2SplitUp) - arg1SplitUp * arg2SplitDown)
        return x, y

    def roundadd(a, b, rmode=roundmode.nearest):
        arg1 = float(a)
        arg2 = float(b)
        x, y = roundfloat.twosum(arg1, arg2)
        if rmode == roundmode.up:
            if x == float('inf'):
                return x
            elif x == -float('inf'):
                if arg1 == -float('inf') or arg2 == -float('inf'):
                    return x
                else:
                    return -__sys__.float_info.max
            if y > 0:
                x = roundfloat.succ(x)
        elif rmode == roundmode.down:
            if x == float('inf'):
                if arg1 == float('inf') or arg2 == float('inf'):
                    return x
                else:
                    return __sys__.float_info.max
            elif x == -float('inf'):
                return x
            if y < 0:
                x = roundfloat.pred(x)
        return x

    def roundsub(a, b, rmode=roundmode.nearest):
        return roundfloat.roundadd(a, b, rmode)

    def roundmul(a, b, rmode=roundmode.nearest):
        arg1 = float(a)
        arg2 = float(b)
        x, y = roundfloat.twoproduct(arg1, arg2)
        if rmode == roundmode.up:
            if x == float('inf'):
                return x
            elif x == -float('inf'):
                if abs(arg1) == float('inf') or abs(arg2) == float('inf'):
                    return x
                else:
                    return -sys.float_info.max
            if abs(x) >= 2.**(-969):
                if y > 0:
                    x = roundfloat.succ(x)
        elif rmode == roundmode.down:
            if x == float('inf'):
                if abs(arg1) == float('inf') or abs(arg2) == float('inf'):
                    return x
                else:
                    return __sys__.float_info.max
            elif x == -float('inf'):
                return x

            if abs(x) >= 2.**(-969):
                if y < 0.:
                    return roundfloat.pred(x)
            else:
                s1, s2 = roundfloat.twoproduct(arg1 * 2.**537, arg2 * 2.**537)
                t = (x * 2.**537) * 2.**537
                if t > s1 or (t == s1 and s2 < 0.):
                    return roundfloat.pred(x)
        return x

    def rounddiv(a, b, rmode=roundmode.nearest):
        arg1 = float(a)
        arg2 = float(b)
        if rmode == roundmode.up:
            pass
            if arg1 == 0. or arg2 == 0. or abs(arg1) == float('inf') or abs(arg2) == float('inf') or arg1 != arg1 or arg2 != arg2:
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
                return -__sys__.float_info.max

            x, y = roundfloat.twoproduct(d, arg2fix)
            if x < arg1fix or (x == arg1fix and y < 0.):
                return roundfloat.succ(d)
            return d
        elif rmode == roundmode.down:
            if arg1 == 0. or arg2 == 0. or abs(arg1) == float('inf') or abs(arg2) == float('inf') or arg1 != arg1 or arg2 != arg2:
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
                return __sys__.float_info.max
            elif d == -float('inf'):
                return d
            x, y = roundfloat.twoproduct(d, arg2fix)
            if x > arg1fix or (x == arg1fix and y > 0.):
                return roundfloat.pred(d)
            return d

    def roundsqrt(x, rmode=roundmode.nearest):
        arg = float(x)
        d = __math__.sqrt(arg)
        if rmode == roundmode.up:
            if arg < 2.**(-969):
                a2 = arg * 2.**106
                d2 = d * 2.**53
                x, y = roundfloat.twoproduct(d2, d2)
                if x < a2 or (x == a2 and y < 0.):
                    d = roundfloat.succ(d)
            x, y = roundfloat.twoproduct(d, d)
            if x < arg or (x == arg and y < 0.):
                d = roundfloat.succ(d)
        if rmode == roundmode.down:
            if arg < 2.**(-969):
                a2 = arg * 2.**106
                d2 = d * 2.**53
                x, y = roundfloat.twoproduct(d2, d2)
                if x > a2 or (x == a2 and y > 0.):
                    d = roundfloat.pred(d)
            x, y = roundfloat.twoproduct(d, d)
            if x > arg or (x == arg and y > 0.):
                d = roundfloat.pred(d)
        return d


class interval:
    inf = 0.
    sup = 0.

    def __init__(self, *args):
        length = len(args)
        if length == 1:
            self.inf = float(args[0])
            self.sup = float(args[0])
        elif length >= 2:
            self.inf = float(args[0])
            self.sup = float(args[1])
        else:
            self.inf = 0.
            self.sup = 0.

    def __add__(self, arg):
        answer = interval(0.)
        if arg.__class__.__name__ == 'int' or arg.__class__.__name__ == 'float':
            answer.inf = roundfloat.roundadd(self.inf, arg, roundmode.down)
            answer.sup = roundfloat.roundadd(self.sup, arg, roundmode.up)
        elif arg.__class__.__name__ == 'interval':
            answer.inf = roundfloat.roundadd(self.inf, arg.inf, roundmode.down)
            answer.sup = roundfloat.roundadd(self.sup, arg.sup, roundmode.up)
        return answer

    def __iadd__(self, arg):
        return interval.__add__(self, arg)

    def __radd__(self, arg):
        return interval.__add__(self, arg)

    def __sub__(self, arg):
        answer = interval(0.)
        if arg.__class__.__name__ == 'int' or arg.__class__.__name__ == 'float':
            answer.inf = roundfloat.roundsub(self.inf, arg, roundmode.down)
            answer.sup = roundfloat.roundsub(self.sup, arg, roundmode.up)
        elif arg.__class__.__name__ == 'interval':
            answer.inf = roundfloat.roundsub(self.inf, arg.sup, roundmode.down)
            answer.sup = roundfloat.roundsub(self.sup, arg.inf, roundmode.up)
        return answer

    def __isub__(self, arg):
        return interval.__sub__(self, arg)

    def __rsub__(self, arg):
        return interval.__sub__(self, arg)

    def __mul__(self, arg):
        answer = interval(0.)
        if arg.__class__.__name__ == 'int' or arg.__class__.__name__ == 'float':
            if arg >= 0.:
                answer.inf = roundfloat.roundmul(self.inf, arg, roundmode.down)
                answer.sup = roundfloat.roundmul(self.sup, arg, roundmode.up)
            else:
                answer.inf = roundfloat.roundmul(self.sup, arg, roundmode.down)
                answer.sup = roundfloat.roundmul(self.inf, arg, roundmode.up)
        elif arg.__class__.__name__ == 'interval':
            if self.inf >= 0.:
                answer.inf = roundfloat.roundmul(
                    self.inf, arg.inf, roundmode.down)
                answer.sup = roundfloat.roundmul(
                    self.sup, arg.sup, roundmode.up)
            elif arg.sup <= 0.:
                answer.inf = roundfloat.roundmul(
                    self.sup, arg.inf, roundmode.down)
                answer.sup = roundfloat.roundmul(
                    self.sup, arg.sup, roundmode.up)
            else:
                answer.inf = roundfloat.roundmul(
                    self.sup, arg.inf, roundmode.down)
                answer.sup = roundfloat.roundmul(
                    self.sup, arg.sup, roundmode.up)
        return answer

    def __imul__(self, arg):
        return interval.__mul__(self, arg)

    def __rmul__(self, arg):
        return interval.__mul__(self, arg)

    def __truediv__(self, arg):
        answer = interval(0.)
        if arg.__class__.__name__ == 'int' or arg.__class__.__name__ == 'float':
            if arg > 0.:
                answer.inf = roundfloat.rounddiv(self.inf, arg, roundmode.down)
                answer.sup = roundfloat.rounddiv(self.sup, arg, roundmode.up)
            elif arg < 0.:
                answer.inf = roundfloat.rounddiv(self.sup, arg, roundmode.down)
                answer.sup = roundfloat.rounddiv(self.inf, arg, roundmode.up)
            else:
                # TODO: nice error message
                print("error")
        elif arg.__class__.__name__ == 'interval':
            if arg.inf > 0.:
                if self.inf >= 0.:
                    answer.inf = roundfloat.rounddiv(
                        self.inf, arg.sup, roundmode.down)
                    answer.sup = roundfloat.rounddiv(
                        self.sup, arg.inf, roundmode.up)
                elif arg.sup < 0.:
                    answer.inf = roundfloat.rounddiv(
                        self.inf, arg.inf, roundmode.down)
                    answer.sup = roundfloat.rounddiv(
                        self.sup, arg.sup, roundmode.up)
                else:
                    answer.inf = roundfloat.rounddiv(
                        self.inf, arg.inf, roundmode.down)
                    answer.sup = roundfloat.rounddiv(
                        self.sup, arg.inf, roundmode.up)
            elif arg.sup < 0.:
                if self.inf >= 0.:
                    answer.inf = roundfloat.rounddiv(
                        self.sup, arg.sup, roundmode.down)
                    answer.sup = roundfloat.rounddiv(
                        self.inf, arg.inf, roundmode.up)
                elif self.sup < 0.:
                    answer.inf = roundfloat.rounddiv(
                        self.sup, arg.inf, roundmode.down)
                    answer.sup = roundfloat.rounddiv(
                        self.inf, arg.sup, roundmode.up)
                else:
                    answer.inf = roundfloat.rounddiv(
                        self.sup, arg.sup, roundmode.down)
                    answer.sup = roundfloat.rounddiv(
                        self.inf, arg.sup, roundmode.up)
            else:
                pass
        return answer

    def __itruediv__(self, arg):
        return interval.__truediv__(self, arg)

    def __rtruediv__(self, arg):
        return interval.__truediv__(self, arg)

    def __str__(self):
        return '[' + str(self.inf) + ',' + str(self.sup) + ']'

    def __repr__(self):
        return '[' + repr(self.inf) + ',' + repr(self.sup) + ']'

    # math function
    def sqrt(self):
        answer = interval(0.)
        answer.inf = roundfloat.roundsqrt(self.inf, roundmode.down)
        answer.sup = roundfloat.roundsqrt(self.sup, roundmode.up)
        return answer

