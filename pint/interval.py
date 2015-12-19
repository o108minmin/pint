# -*- coding: utf-8 -*-

from .core import roundmode as rdm
from .core import roundfloat as rf
import math
import sys


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
        if (arg.__class__.__name__ == 'int' or
                arg.__class__.__name__ == 'float'):
            answer.inf = rf.rdadd(self.inf, arg, rdm.down)
            answer.sup = rf.rdadd(self.sup, arg, rdm.up)
        elif arg.__class__.__name__ == 'interval':
            answer.inf = rf.rdadd(self.inf, arg.inf, rdm.down)
            answer.sup = rf.rdadd(self.sup, arg.sup, rdm.up)
        return answer

    def __iadd__(self, arg):
        return interval.__add__(self, arg)

    def __radd__(self, arg):
        return interval.__add__(self, arg)

    def __sub__(self, arg):
        answer = interval(0.)
        if (
                arg.__class__.__name__ == 'int' or
                arg.__class__.__name__ == 'float'):
            answer.inf = rf.rdsub(self.inf, arg, rdm.down)
            answer.sup = rf.rdsub(self.sup, arg, rdm.up)
        elif arg.__class__.__name__ == 'interval':
            answer.inf = rf.rdsub(self.inf, arg.sup, rdm.down)
            answer.sup = rf.rdsub(self.sup, arg.inf, rdm.up)
        return answer

    def __isub__(self, arg):
        return interval.__sub__(self, arg)

    def __rsub__(self, arg):
        return interval.__sub__(self, arg)

    def __mul__(self, arg):
        answer = interval(0.)
        if (
                arg.__class__.__name__ == 'int' or
                arg.__class__.__name__ == 'float'):
            if arg >= 0.:
                answer.inf = rf.rdmul(self.inf, arg, rdm.down)
                answer.sup = rf.rdmul(self.sup, arg, rdm.up)
            else:
                answer.inf = rf.rdmul(self.sup, arg, rdm.down)
                answer.sup = rf.rdmul(self.inf, arg, rdm.up)
        elif arg.__class__.__name__ == 'interval':
            if self.inf >= 0.:
                answer.inf = rf.rdmul(
                    self.inf, arg.inf, rdm.down)
                answer.sup = rf.rdmul(
                    self.sup, arg.sup, rdm.up)
            elif arg.sup <= 0.:
                answer.inf = rf.rdmul(
                    self.sup, arg.inf, rdm.down)
                answer.sup = rf.rdmul(
                    self.sup, arg.sup, rdm.up)
            else:
                answer.inf = rf.rdmul(
                    self.sup, arg.inf, rdm.down)
                answer.sup = rf.rdmul(
                    self.sup, arg.sup, rdm.up)
        return answer

    def __imul__(self, arg):
        return interval.__mul__(self, arg)

    def __rmul__(self, arg):
        return interval.__mul__(self, arg)

    def __truediv__(self, arg):
        answer = interval(0.)
        if (
                arg.__class__.__name__ == 'int' or
                arg.__class__.__name__ == 'float'):
            if arg > 0.:
                answer.inf = rf.rddiv(self.inf, arg, rdm.down)
                answer.sup = rf.rddiv(self.sup, arg, rdm.up)
            elif arg < 0.:
                answer.inf = rf.rddiv(self.sup, arg, rdm.down)
                answer.sup = rf.rddiv(self.inf, arg, rdm.up)
            else:
                # TODO: nice error message
                print("error")
        elif arg.__class__.__name__ == 'interval':
            if arg.inf > 0.:
                if self.inf >= 0.:
                    answer.inf = rf.rddiv(
                        self.inf, arg.sup, rdm.down)
                    answer.sup = rf.rddiv(
                        self.sup, arg.inf, rdm.up)
                elif arg.sup < 0.:
                    answer.inf = rf.rddiv(
                        self.inf, arg.inf, rdm.down)
                    answer.sup = rf.rddiv(
                        self.sup, arg.sup, rdm.up)
                else:
                    answer.inf = rf.rddiv(
                        self.inf, arg.inf, rdm.down)
                    answer.sup = rf.rddiv(
                        self.sup, arg.inf, rdm.up)
            elif arg.sup < 0.:
                if self.inf >= 0.:
                    answer.inf = rf.rddiv(
                        self.sup, arg.sup, rdm.down)
                    answer.sup = rf.rddiv(
                        self.inf, arg.inf, rdm.up)
                elif self.sup < 0.:
                    answer.inf = rf.rddiv(
                        self.sup, arg.inf, rdm.down)
                    answer.sup = rf.rddiv(
                        self.inf, arg.sup, rdm.up)
                else:
                    answer.inf = rf.rddiv(
                        self.sup, arg.sup, rdm.down)
                    answer.sup = rf.rddiv(
                        self.inf, arg.sup, rdm.up)
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

    def __radd__(self, arg):
        return interval.__add__(self, arg)

    def __sub__(self, arg):
        answer = interval(0.)
        if (arg.__class__.__name__ == 'int' or
                arg.__class__.__name__ == 'float'):
            answer.inf = rf.rdsub(self.inf, arg, rdm.down)
            answer.sup = rf.rdsub(self.sup, arg, rdm.up)
        elif arg.__class__.__name__ == 'interval':
            answer.inf = rf.rdsub(self.inf, arg.sup, rdm.down)
            answer.sup = rf.rdsub(self.sup, arg.inf, rdm.up)
        return answer

    def __isub__(self, arg):
        return interval.__sub__(self, arg)

    def __rsub__(self, arg):
        return interval.__sub__(self, arg)

    def __mul__(self, arg):
        answer = interval(0.)
        arg_name = arg.__class__.__name__
        if arg_name == 'int' or arg_name == 'float':
            if arg >= 0.:
                answer.inf = rf.rdmul(self.inf, arg, rdm.down)
                answer.sup = rf.rdmul(self.sup, arg, rdm.up)
            else:
                answer.inf = rf.rdmul(self.sup, arg, rdm.down)
                answer.sup = rf.rdmul(self.inf, arg, rdm.up)
        elif arg.__class__.__name__ == 'interval':
            if self.inf >= 0.:
                answer.inf = rf.rdmul(
                    self.inf, arg.inf, rdm.down)
                answer.sup = rf.rdmul(
                    self.sup, arg.sup, rdm.up)
            elif arg.sup <= 0.:
                answer.inf = rf.rdmul(
                    self.sup, arg.inf, rdm.down)
                answer.sup = rf.rdmul(
                    self.sup, arg.sup, rdm.up)
            else:
                answer.inf = rf.rdmul(
                    self.sup, arg.inf, rdm.down)
                answer.sup = rf.rdmul(
                    self.sup, arg.sup, rdm.up)
        return answer

    def __imul__(self, arg):
        return interval.__mul__(self, arg)

    def __rmul__(self, arg):
        return interval.__mul__(self, arg)

    def __truediv__(self, arg):
        answer = interval(0.)
        if (
                arg.__class__.__name__ == 'int' or
                arg.__class__.__name__ == 'float'):
            if arg > 0.:
                answer.inf = rf.rddiv(self.inf, arg, rdm.down)
                answer.sup = rf.rddiv(self.sup, arg, rdm.up)
            elif arg < 0.:
                answer.inf = rf.rddiv(self.sup, arg, rdm.down)
                answer.sup = rf.rddiv(self.inf, arg, rdm.up)
            else:
                # TODO: nice error message
                print("error")
        elif arg.__class__.__name__ == 'interval':
            if arg.inf > 0.:
                if self.inf >= 0.:
                    answer.inf = rf.rddiv(
                        self.inf, arg.sup, rdm.down)
                    answer.sup = rf.rddiv(
                        self.sup, arg.inf, rdm.up)
                elif arg.sup < 0.:
                    answer.inf = rf.rddiv(
                        self.inf, arg.inf, rdm.down)
                    answer.sup = rf.rddiv(
                        self.sup, arg.sup, rdm.up)
                else:
                    answer.inf = rf.rddiv(
                        self.inf, arg.inf, rdm.down)
                    answer.sup = rf.rddiv(
                        self.sup, arg.inf, rdm.up)
            elif arg.sup < 0.:
                if self.inf >= 0.:
                    answer.inf = rf.rddiv(
                        self.sup, arg.sup, rdm.down)
                    answer.sup = rf.rddiv(
                        self.inf, arg.inf, rdm.up)
                elif self.sup < 0.:
                    answer.inf = rf.rddiv(
                        self.sup, arg.inf, rdm.down)
                    answer.sup = rf.rddiv(
                        self.inf, arg.sup, rdm.up)
                else:
                    answer.inf = rf.rddiv(
                        self.sup, arg.sup, rdm.down)
                    answer.sup = rf.rddiv(
                        self.inf, arg.sup, rdm.up)
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

    def __neg__(self):
        return interval(-self.sup, -self.inf)

    def __abs__(arg):
        return arg.math.fabs(arg)

    def __pow__(a, b):
        return interval.math.pow(a, b)

    def __lt__(a, b):
        if a.__class__.__name__ == "interval":
            if b.__class__.__name__ == "interval":
                return a.sup < b.inf
            else:
                return a.sup < b
        if a.__class__.__name__ == "float":
            if b.__class__.__name__ == "interval":
                return a < b.inf
            else:
                return a < b

    def __le__(a, b):
        if a.__class__.__name__ == "interval":
            if b.__class__.__name__ == "interval":
                return a.sup <= b.inf
            else:
                return a.sup <= b
        if a.__class__.__name__ == "float":
            if b.__class__.__name__ == "interval":
                return a <= b.inf
            else:
                return a <= b

    def __eq__(a, b):
        if a.__class__.__name__ == "interval":
            if b.__class__.__name__ == "interval":
                return a.sup == b.inf and b.inf == b.sup
            else:
                return a.sup == a.inf and a.sup == b
        if a.__class__.__name__ == "float":
            if b.__class__.__name__ == "interval":
                return b.sup == b.inf and b.sup == a
            else:
                return a == b
        pass

    def __ne__(a, b):
        if a.__class__.__name__ == "interval":
            if b.__class__.__name__ == "interval":
                return interval.overlap(a, b)
            else:
                return interval.overlap(a, interval(b))
        if a.__class__.__name__ == "float":
            if b.__class__.__name__ == "interval":
                return interval.overlap(interval(a), b)
            else:
                return interval.overlap(interval(a), interval(b))

    def __ge__(a, b):
        if a.__class__.__name__ == "interval":
            if b.__class__.__name__ == "interval":
                return a.inf >= b.sup
            else:
                return a.inf >= b
        if a.__class__.__name__ == "float":
            if b.__class__.__name__ == "interval":
                return a >= b.sup
            else:
                return a >= b

    def __gt__(a, b):
        if a.__class__.__name__ == "interval":
            if b.__class__.__name__ == "interval":
                return a.inf > b.sup
            else:
                return a.inf > b
        if a.__class__.__name__ == "float":
            if b.__class__.__name__ == "interval":
                return a > b.sup
            else:
                return a > b

    # interval tools
    def hull(a, b):
        if a.__class__.__name__ != "interval":
            a = interval(a)
        if b.__class__.__name__ != "interval":
            b = interval(b)
        tmp1 = a.inf
        if b.inf < tmp1:
            tmp1 = b.inf
        tmp2 = a.sup
        if b.sup > tmp2:
            tmp2 = b.sup
        return interval(tmp1, tmp2)

    def whole():
        return interval(float("inf"), -float("inf"))

    def subset(x, y):
        if y.inf <= x.inf and x.sup <= y.sup:
            return True
        else:
            return False

    def proper_subset(x, y):
        if interval.subset(x, y) and (y.inf < x.inf or x.sup < y.sup):
            return True
        else:
            return False

    def number_in(x, number):
        if x.inf < number and number < x.sup:
            return True
        else:
            return False

    def zero_in(x):
        if x.inf < 0. and 0. < x.sup:
            return True
        else:
            return False

    def overlap(x, y):
        tmp1 = x.inf
        if y.inf > tmp1:
            tmp1 = y.inf
        tmp2 = x.sup
        if y.sup < tmp2:
            tmp2 = y.sup
        if tmp1 <= tmp2:
            return True
        else:
            return False

    def norm(x):
        if x.inf >= 0.:
            return x.sup
        if x.sup <= 0.:
            return -x.inf
        tmp = -x.inf
        if x.sup > tmp:
            tmp = x.sup
        return tmp

    def mag(x):
        return interval.norm(x)

    def width(x):
        answer = rf.rdsub(x.sup, x.inf)
        return answer

    def mid(x):
        if math.fabs(x.inf) > 1. and math.fabs(x.sup) > 1.:
            return x.inf * 0.5 + x.sup * 0.5
        else:
            return (x.inf + x.sup) * 0.5

    def median(x):
        return mid(x)

    def intersect(x, y):
        tmp1 = x.inf
        if y.inf > tmp1:
            tmp1 = y.inf
        tmp2 = x.sup
        if y.sup < tmp2:
            tmp2 = y.sup
        return interval(tmp1, tmp2)

    # math functions
    class math:

        def e():
            return interval(math.e, rf.succ(math.e))

        def pi():
            return interval(math.pi, rf.succ(math.pi))

        def sqrt(arg):
            answer = interval(0.)
            answer.inf = rf.rdsqrt(arg.inf, rdm.down)
            answer.sup = rf.rdsqrt(arg.sup, rdm.up)
            return answer

        def fabs(arg):
            if arg.inf >= 0.:
                return arg
            if arg.sup <= 0.:
                return -arg
            tmp = -arg.inf
            if arg.sup > tmp:
                tmp = arg.sup
            return interval(0., tmp)

        def isnan(arg):
            if arg.inf != arg.inf:
                return True
            if arg.sup != arg.sup:
                return True
            return False

        def isinf(arg):
            if arg.inf == float("inf") or arg.inf == float("-inf"):
                return True
            if arg.sup == float("inf") or arg.sup == float("-inf"):
                return True
            return False

        def isfinite(arg):
            if interval.math.isnan(arg) == True:
                return False
            if interval.math.isinf(arg) == True:
                return False
            return True

        def pow(x, i):
            # TODO: write pow(x, interval i)
            if i.__class__.__name__ == "interval":
                pass
            answer = interval(1.)
            for times in range(0, i, 1):
                answer *= x
            return answer

        def exp(x):
            tmp1 = rf.pred(math.exp(x.inf))
            tmp1 = rf.succ(math.exp(x.inf))
            return interval(tmp1, tmp2)

        # TODO: Fix lazy expm1 (significant loss of precision)
        def expm1(x):
            return interval.math.exp(x) - 1.

        def ldexp(x, i):
            return x * (2 ** i)

        # TODO: Fix log, log2 and log10 for x(double)
        def log(x):
            tmp1 = rf.pred(math.log(x.inf))
            tmp2 = rf.succ(math.log(x.sup))
            return interval(tmp1, tmp2)

        def log2(x):
            tmp1 = rf.pred(math.log2(x.inf))
            tmp2 = rf.succ(math.log2(x.sup))
            return interval(tmp1, tmp2)

        def log10(x):
            tmp1 = rf.pred(math.log10(x.inf))
            tmp2 = rf.succ(math.log10(x.sup))
            return interval(tmp1, tmp2)

        def sin_origin(x):
            r = interval(0.)
            y = interval(1.)
            i = 1
            eps = sys.float_info.epsilon
            while True:
                intval_i = interval(i)
                y = y * x
                y = y / intval_i
                if interval.mag(y) < eps:
                    r += y * interval(-1., 1.)
                    break
                else:
                    if i % 2 != 0:
                        if i % 4 == 1:
                            r += y
                        else:
                            r -= y
                i = i + 1
            return r

        def sin_point(x):
            intval_pi = interval.math.pi()
            mid_pi = interval.mid(intval_pi)
            if x.inf >= mid_pi:
                print(x)
                return interval.math.sin_point(x - (intval_pi * 2.))
            if x.sup <= -mid_pi * 0.75:
                return -interval.math.sin_origin(x + intval_pi)
            if x.sup <= -mid_pi * 0.5:
                return -interval.math.cos_origin(-intval_pi * 0.5 - x)
            if x.sup <= -mid_pi * 0.25:
                return -interval.math.cos_origin(x + intval_pi * 0.5)
            if x.sup <= 0.:
                return -interval.math.sin_origin(-x)
            if x.sup <= mid_pi * 0.25:
                return interval.math.sin_origin(x)
            if x.sup <= mid_pi * 0.5:
                return interval.math.cos_origin(intval_pi * 0.5 - x)
            if x.sup <= mid_pi * 0.75:
                return interval.math.cos_origin(x - intval_pi * 0.5)
            return interval.math.sin_origin(intval_pi - x)

        def sin(x):
            intval_pi = interval.math.pi()
            intval_pi2 = intval_pi * 2.
            if interval.math.isinf(x) == True:
                return interval.hull(-1., 1.)
            # x is normalized to -pi < x < pi
            x_nor = x
            while (
                    x_nor.inf <= -intval_pi.sup or
                    x_nor.inf >= intval_pi.sup):
                n = math.floor((x_nor.inf / intval_pi2.inf) + 0.5)
                x_nor = x_nor - n * intval_pi2
            if math.fabs(rf.rdsub(x.sup, x.inf, rdm.down)) > intval_pi2.sup:
                return interval(-1., 1.)
            tmp1 = interval.math.sin_point(interval(x_nor.inf))
            tmp2 = interval.math.sin_point(interval(x_nor.sup))
            r = interval.hull(tmp1, tmp2)
            if interval.subset(intval_pi * 0.5, x_nor):
                r = interval.hull(r, 1.)
            if interval.subset(intval_pi * 2.5, x_nor):
                r = interval.hull(r, -1.)
            if interval.subset(-intval_pi * 0.5, x_nor):
                r = interval.hull(r, -1)
            if interval.subset(intval_pi * 1.5, x_nor):
                r = interval.hull(r, -1)
            return interval.intersect(r, interval(-1, 1))

        def cos_origin(x):
            r = interval(1.)
            y = interval(1.)
            i = 1
            eps = sys.float_info.epsilon
            while True:
                intval_i = interval(i)
                y = y * x
                y = y / intval_i
                if interval.mag(y) < eps:
                    r = r + y * interval(-1., 1.)
                    break
                else:
                    if i % 2 == 0:
                        if i % 4 == 0:
                            r = r + y
                        else:
                            r = r - y
                i = i + 1
            return r

        def cos_point(x):
            intval_pi = interval.math.pi()
            mid_pi = interval.mid(intval_pi)
            if x.inf >= mid_pi:
                return interval.math.cos_point(x - intval_pi * 2.)
            if x.sup <= -mid_pi * 0.75:
                return -interval.math.cos_origin(x + intval_pi)
            if x.sup <= -mid_pi * 0.5:
                return -interval.math.sin_origin(-intval_pi * 0.5 - x)
            if x.sup <= -mid_pi * 0.25:
                return interval.math.sin_origin(x + intval_i * 0.5)
            if x.sup <= 0.:
                return interval.math.cos_origin(-x)
            if x.sup <= mid_pi * 0.25:
                return interval.math.cos_origin(x)
            if x.sup <= mid_pi * 0.5:
                return interval.math.sin_origin(intval_pi * 0.5 - x)
            if x.sup <= mid_pi * 0.75:
                return -interval.math.sin_origin(x - intval_pi * 0.5)
            return -interval.math.cos_origin(intval_pi - x)

        def cos(x):
            intval_pi = interval.math.pi()
            intval_pi2 = intval_pi * 2.
            if interval.math.isinf(x) == True:
                return interval.hull(-1, 1)
            x_nor = x
            while x_nor <= -intval_pi.inf or x_nor >= intval_pi.sup:
                n = math.floor((x_nor.inf / intval_pi2.inf) + 0.5)
                x_nor -= n * intval_pi2
            if math.fabs(rf.rdsub(x.sup, x.inf, rdm.down)) > intval_pi2.sup:
                return interval(-1., 1.)
            tmp1 = interval.math.cos_point(interval(x_nor.inf))
            tmp2 = interval.math.cos_point(interval(x_nor.sup))
            r = interval.hull(tmp1, tmp2)
            if interval.zero_in(r):
                r = interval.hull(r, 1.)
            if interval.subset(intval_pi2, x_nor):
                r = interval.hull(r, 1.)
            if interval.subset(-intval_pi, x_nor):
                r = interval.hull(r, -1.)
            if interval.subset(intval_pi, x_nor):
                r = interval.hull(r, -1.)
            if interval.subset(intval_pi * 3., x_nor):
                r = interval.hull(r, -1.)
            return interval.intersect(r, interval(-1., 1.))

        def tan_point(x):
            tmp1 = interval.math.sin_point(interval(x))
            tmp2 = interval.math.cos_point(interval(x))
            return tmp1 / tmp2

        def tan(x):
            intval_pi = interval.math.pi()
            intval_pih = intval_pi * 0.5
            if interval.math.isinf(x) == True:
                return interval.hull(-1., 1.)
            x_nor = x
            while x_nor <= -intval_pi.inf or x_nor >= intval_pi.sup:
                n = math.floor((x_nor.inf / intval_pi2.inf) + 0.5)
                x_nor -= n * intval_pi2
            if x_nor.sup >= intval_pih:
                interval.whole()
            tmp1 = interval.math.tan_point(x_nor.inf)
            tmp2 = interval.math.tan_point(x_nor.sup)
            return interval(tmp1.inf, tmp2.sup)

        def atan_origin(x):
            r = interval(0.)
            y = interval(1.)
            i = 1
            eps = sys.float_info.epsilon
            while True:
                y = y * x
                tmp = y * interval(-1., 1.) / interval(i)
                if interval.mag(tmp) < eps:
                    r = r + tmp
                    break
                else:
                    if i % 2 != 0:
                        if i % 4 == 1:
                            r = r + y / interval(i)
                        else:
                            r = r - y / interval(i)
                i += 1
            return r

        def atan_point(x):
            intval_pi = interval.math.pi()
            intval_x = interval(x)
            if x < -math.sqrt(2.) + 1.:
                t1 = 1. / intval_x
                return -intval_pi * 0.5 - interval.math.atan_origin(t1)
            if x < -math.sqrt(2.) - 1.:
                t1 = 1. + intval_x
                t2 = 1. - intval_x
                return -intval_pi * 0.25 + interval.math.atan_origin(t1 / t2)
            if x < math.sqrt(2.) - 1.:
                return interval.math.atan_origin(intval_x)
            if x < math.sqrt(2.) + 1.:
                t1 = intval_x - 1.
                t2 = intval_x + 1.
                return intval_pi * 0.25 + interval.math.atan_origin(t1 / t2)
            return intval_pi * 0.5 - interval.mathatan_origin(1. / intval_x)

        def atan(x):
            t1 = interval.math.atan_point(x.inf)
            t2 = interval.math.atan_point(x.sup)
            return interval(t1.inf, t2.sup)
