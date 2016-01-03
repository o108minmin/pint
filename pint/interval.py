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
        return interval.__add__(-self, arg)

    def __mul__(self, arg):
        answer = interval(0.)
        if arg.__class__.__name__ == 'interval':
            if interval.zero_in(arg) == True:
                if interval.zero_in(self) == True:
                    answer.inf = rf.rdmul(self.inf, arg.sup, rdm.down)
                    tmp = rf.rdmul(self.sup, arg.inf, rdm.down)
                    if answer.inf > tmp:
                        answer.inf = tmp
                    answer.sup = rf.rdmul(self.inf, arg.inf, rdm.up)
                    tmp = rf.rdmul(self.sup, arg.sup, rdm.up)
                    if answer.sup < tmp:
                        answer.sup = tmp
                elif self.inf >= 0.:
                    answer.inf = rf.rdmul(self.sup, arg.inf, rdm.down)
                    answer.sup = rf.rdmul(self.sup, arg.sup, rdm.up)
                elif self.sup <= 0.:
                    answer.inf = rf.rdmul(self.inf, arg.sup, rdm.down)
                    answer.sup = rf.rdmul(self.inf, arg.inf, rdm.up)
            elif arg.inf >= 0.:
                if interval.zero_in(self) == True:
                    answer.inf = rf.rdmul(self.inf, arg.sup, rdm.down)
                    answer.sup = rf.rdmul(self.sup, arg.sup, rdm.up)
                elif self.inf >= 0.:
                    answer.inf = rf.rdmul(self.inf, arg.inf, rdm.down)
                    answer.sup = rf.rdmul(self.sup, arg.sup, rdm.up)
                elif self.sup <= 0.:
                    answer.inf = rf.rdmul(self.inf, arg.sup, rdm.down)
                    answer.sup = rf.rdmul(self.sup, arg.inf, rdm.up)
            elif arg.sup <= 0.:
                if interval.zero_in(self) == True:
                    answer.inf = rf.rdmul(self.sup, arg.inf, rdm.down)
                    answer.sup = rf.rdmul(self.inf, arg.inf, rdm.up)
                elif self.inf >= 0.:
                    answer.inf = rf.rdmul(self.sup, arg.inf, rdm.down)
                    answer.sup = rf.rdmul(self.inf, arg.sup, rdm.up)
                elif self.sup <= 0.:
                    answer.inf = rf.rdmul(self.sup, arg.sup, rdm.down)
                    answer.sup = rf.rdmul(self.inf, arg.inf, rdm.up)
            else:
                # TODO: nice error message
                print("error")
        else:
            if arg >= 0.:
                answer.inf = rf.rdmul(self.inf, arg, rdm.down)
                answer.sup = rf.rdmul(self.sup, arg, rdm.up)
            elif arg < 0.:
                answer.inf = rf.rdmul(self.sup, arg, rdm.down)
                answer.sup = rf.rdmul(self.inf, arg, rdm.up)
            else:
                # TODO: nice error message
                print("error")
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
        # arg / self(interval)
        answer = interval(0.)
        if self.inf > 0. or self.sup < 0.:
            if arg >= 0.:
                answer.inf = rf.rddiv(arg, self.sup, rdm.down)
                answer.sup = rf.rddiv(arg, self.inf, rdm.up)
            else:
                answer.inf = rf.rddiv(arg, self.inf, rmd.down)
                answer.sup = rf.rddiv(arg, self.sup, rmd.up)
        else:
            # TODO: nice error message
            print("error")
        return answer

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

        def exp_point(x):
            eps = sys.float_info.epsilon
            if x == float("inf"):
                return interval(sys.float_info.max, float("inf"))
            elif x == float("inf"):
                return interval(0.)
            itv_e_sq = interval.math.sqrt(interval.math.e())
            tmp = 1. / itv_e_sq
            remainder = interval(tmp.inf, itv_e_sq.sup)
            if x >= 0.:
                # x_iは整数部分か
                x_i = math.floor(x)
                # x_fは小数部分か
                x_f = x - x_i
                if x_f >= 0.5:
                    x_f = 1.
                    x_i = 1.
            else:
                x_i = -math.floor(x)
                x_f = x - x_i
                if x_f <= -0.5:
                    x_f += 1.
                    x_i += 1.
            r = interval(1.)
            y = interval(1.)
            i = 0
            while True:
                y *= x_f
                y /= interval(i)
                if interval.mag(y) * remainder.sup < eps:
                    r += y * remainder
                    break
                else:
                    r += y
                i += 1
            if x_i >= 0.:
                r *= interval.math.pow(interval.math.e(), x_i)
            else:
                r /= interval.math.pow(interval.math.e(), -x_i)
            return r

        def exp(x):
            tmp1 = interval.math.exp_point(x.inf)
            tmp2 = interval.math.exp_point(x.sup)
            return interval(tmp1.inf, tmp2.sup)

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
                itv_i = interval(i)
                y = y * x
                y = y / itv_i
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
            itv_pi = interval.math.pi()
            mid_pi = interval.mid(itv_pi)
            if x.inf >= mid_pi:
                print(x)
                return interval.math.sin_point(x - (itv_pi * 2.))
            if x.sup <= -mid_pi * 0.75:
                return -interval.math.sin_origin(x + itv_pi)
            if x.sup <= -mid_pi * 0.5:
                return -interval.math.cos_origin(-itv_pi * 0.5 - x)
            if x.sup <= -mid_pi * 0.25:
                return -interval.math.cos_origin(x + itv_pi * 0.5)
            if x.sup <= 0.:
                return -interval.math.sin_origin(-x)
            if x.sup <= mid_pi * 0.25:
                return interval.math.sin_origin(x)
            if x.sup <= mid_pi * 0.5:
                return interval.math.cos_origin(itv_pi * 0.5 - x)
            if x.sup <= mid_pi * 0.75:
                return interval.math.cos_origin(x - itv_pi * 0.5)
            return interval.math.sin_origin(itv_pi - x)

        def sin(x):
            itv_pi = interval.math.pi()
            itv_pi2 = itv_pi * 2.
            if interval.math.isinf(x) == True:
                return interval.hull(-1., 1.)
            # x is normalized to -pi < x < pi
            x_nor = x
            while (
                    x_nor.inf <= -itv_pi.sup or
                    x_nor.inf >= itv_pi.sup):
                n = math.floor((x_nor.inf / itv_pi2.inf) + 0.5)
                x_nor = x_nor - n * itv_pi2
            if math.fabs(rf.rdsub(x.sup, x.inf, rdm.down)) > itv_pi2.sup:
                return interval(-1., 1.)
            tmp1 = interval.math.sin_point(interval(x_nor.inf))
            tmp2 = interval.math.sin_point(interval(x_nor.sup))
            r = interval.hull(tmp1, tmp2)
            if interval.subset(itv_pi * 0.5, x_nor):
                r = interval.hull(r, 1.)
            if interval.subset(itv_pi * 2.5, x_nor):
                r = interval.hull(r, -1.)
            if interval.subset(-itv_pi * 0.5, x_nor):
                r = interval.hull(r, -1)
            if interval.subset(itv_pi * 1.5, x_nor):
                r = interval.hull(r, -1)
            return interval.intersect(r, interval(-1, 1))

        def cos_origin(x):
            r = interval(1.)
            y = interval(1.)
            i = 1
            eps = sys.float_info.epsilon
            while True:
                itv_i = interval(i)
                y = y * x
                y = y / itv_i
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
            itv_pi = interval.math.pi()
            mid_pi = interval.mid(itv_pi)
            if x.inf >= mid_pi:
                return interval.math.cos_point(x - itv_pi * 2.)
            if x.sup <= -mid_pi * 0.75:
                return -interval.math.cos_origin(x + itv_pi)
            if x.sup <= -mid_pi * 0.5:
                return -interval.math.sin_origin(-itv_pi * 0.5 - x)
            if x.sup <= -mid_pi * 0.25:
                return interval.math.sin_origin(x + itv_i * 0.5)
            if x.sup <= 0.:
                return interval.math.cos_origin(-x)
            if x.sup <= mid_pi * 0.25:
                return interval.math.cos_origin(x)
            if x.sup <= mid_pi * 0.5:
                return interval.math.sin_origin(itv_pi * 0.5 - x)
            if x.sup <= mid_pi * 0.75:
                return -interval.math.sin_origin(x - itv_pi * 0.5)
            return -interval.math.cos_origin(itv_pi - x)

        def cos(x):
            itv_pi = interval.math.pi()
            itv_pi2 = itv_pi * 2.
            if interval.math.isinf(x) == True:
                return interval.hull(-1, 1)
            x_nor = x
            while x_nor <= -itv_pi.inf or x_nor >= itv_pi.sup:
                n = math.floor((x_nor.inf / itv_pi2.inf) + 0.5)
                x_nor -= n * itv_pi2
            if math.fabs(rf.rdsub(x.sup, x.inf, rdm.down)) > itv_pi2.sup:
                return interval(-1., 1.)
            tmp1 = interval.math.cos_point(interval(x_nor.inf))
            tmp2 = interval.math.cos_point(interval(x_nor.sup))
            r = interval.hull(tmp1, tmp2)
            if interval.zero_in(r):
                r = interval.hull(r, 1.)
            if interval.subset(itv_pi2, x_nor):
                r = interval.hull(r, 1.)
            if interval.subset(-itv_pi, x_nor):
                r = interval.hull(r, -1.)
            if interval.subset(itv_pi, x_nor):
                r = interval.hull(r, -1.)
            if interval.subset(itv_pi * 3., x_nor):
                r = interval.hull(r, -1.)
            return interval.intersect(r, interval(-1., 1.))

        def tan_point(x):
            tmp1 = interval.math.sin_point(interval(x))
            tmp2 = interval.math.cos_point(interval(x))
            return tmp1 / tmp2

        def tan(x):
            itv_pi = interval.math.pi()
            itv_pih = itv_pi * 0.5
            if interval.math.isinf(x) == True:
                return interval.hull(-1., 1.)
            x_nor = x
            while x_nor <= -itv_pi.inf or x_nor >= itv_pi.sup:
                n = math.floor((x_nor.inf / itv_pi2.inf) + 0.5)
                x_nor -= n * itv_pi2
            if x_nor.sup >= itv_pih:
                interval.whole()
            tmp1 = interval.math.tan_point(x_nor.inf)
            tmp2 = interval.math.tan_point(x_nor.sup)
            return interval(tmp1.inf, tmp2.sup)

        def atan_origin(x):
            r = interval(0.)
            y = interval(1.)
            i = 1.
            eps = sys.float_info.epsilon
            while True:
                y = y * x
                tmp = y * interval(-1., 1.) / float(i)
                if interval.mag(tmp) < eps:
                    r = r + tmp
                    break
                else:
                    if i % 2 != 0:
                        if i % 4 == 1:
                            r = r + y / float(i)
                        else:
                            r = r - y / float(i)
                i += 1.
            return r

        def atan_point(x):
            itv_pi = interval.math.pi()
            itv_x = interval(x)
            if x < -(math.sqrt(2.) + 1.):
                t1 = 1. / itv_x
                return -itv_pi * 0.5 - interval.math.atan_origin(t1)
            if x < -(math.sqrt(2.) - 1.):
                t1 = 1. + itv_x
                t2 = 1. - itv_x
                return -itv_pi * 0.25 + interval.math.atan_origin(t1 / t2)
            if x < (math.sqrt(2.) - 1.):
                return interval.math.atan_origin(itv_x)
            if x < (math.sqrt(2.) + 1.):
                t1 = itv_x - 1.
                t2 = itv_x + 1.
                return itv_pi * 0.25 + interval.math.atan_origin(t1 / t2)
            return itv_pi * 0.5 - interval.math.atan_origin(1. / itv_x)

        def atan(x):
            t1 = interval.math.atan_point(x.inf)
            t2 = interval.math.atan_point(x.sup)
            return interval(t1.inf, t2.sup)

        def asin_point(x):
            itv_pi = interval.math.pi()
            itv_pih = itv_pi * 0.5
            if x < -1. or x > 1.:
                # TODO: nice erroe message
                return "error"
            if x == 1.:
                return itv_pih
            if x == -1.:
                return -itv_pih
            if math.fabs(x) < math.sqrt(6.) / 3.:
                t1 = interval(x) * x
                return interval.math.atan(x / interval.math.sqrt(1. - t1))
            else:
                if x > 0.:
                    t1 = 1. - x
                    t2 = 1. + interval(x)
                    return interval.math.atan(x / interval.math.sqrt(t1 * t2))
                else:
                    t1 = 1. + x
                    t2 = 1. - interval(x)
                    return interval.math.atan(x / interval.math(t1 * t2))

        def asin(x):
            t1 = interval.math.asin_point(x.inf)
            t2 = interval.math.asin_point(x.sup)
            return interval(t1.inf, t2.sup)

        def pih_m_atan_point(x):
            itv_pi = interval.math.pi()
            if x.inf < -(math.sqrt(2.) + 1.):
                return itv_pi + interval.math.atan_origin(1. / x)
            elif x.inf < -(math.sqrt(2.) - 1.):
                tmp = (1. + x) / (1. - x)
                return itv_pi * 0.75 - interval.math.atan_origin(tmp)
            elif x.inf < math.sqrt(2.) - 1.:
                return itv_pi * 0.5 - interval.math.atan_origin(x)
            elif x.inf < math.sqrt(2.) + 1.:
                tmp = (x - 1.) / (x + 1.)
                return itv_pi * 0.25 - interval.math.atan_origin(tmp)
            return interval.math.atan_origin(1. / x)

        def acos_point(x):
            itv_pi = interval.math.pi()
            if x < -1. or x > 1.:
                # TODO: nice erroe message
                print("error")
                return "error"
            elif x == 1.:
                return interval(0.)
            elif x == -1.:
                return itv_pi
            if math.fabs(x) < math.sqrt(6.) / 3.:
                tmp = interval.math.sqrt(1. - interval(x) * x)
                return interval.math.pih_m_atan_point(x / tmp)
            else:
                if x > 0.:
                    tmp = interval.math.sqrt(1. + interval(x) * (1. - x))
                    return interval.math.pih_m_atan_point(x / tmp)
                else:
                    tmp = interval.math.sqrt((1. + x) * (1. - interval(x)))
                    return interval.math.pih_m_atan_point(x / tmp)

        def acos(x):
            t1 = interval.math.acos_point(x.sup)
            t2 = interval.math.acos_point(x.inf)
            return interval(t1.inf, t2.sup)

        def atan2_point(y, x):
            itv_pi = interval.math.pi()
            itv_x = interval(x)
            itv_y = interval(y)
            if y <= x and y > -x:
                return atan(itv_x / itv_y)
            elif y > x and y > -x:
                return itv_pi * 0.5 - interval.math.atan(itv_x / itv_y)
            elif y > x and y <= -x:
                if y >= 0.:
                    return itv_pi + interval.math.atan(itv_x / itv_y)
                else:
                    return -itv_pi + interval.math.atan(itv_x / itv_y)
            return -itv_pi * 0.5 - interval.math.atan(itv_x / itv_y)

        def atan2(Iy, Ix):
            itv_pi = interval.math.pi()
            itv_pi2 = itv_pi * 2.
            if interval.zero_in(Ix) == True:
                if interval.zero_in(Iy) == True:
                    return interval(-itv_pi.sup, itv_pi.sup)
                else:
                    if Iy > 0.:
                        t1 = interval.math.atan2_point(Iy.inf, Ix.sup)
                        t2 = interval.math.atan2_point(Iy.inf, Ix.inf)
                        return interval(t1.inf, t2.sup)
                    else:
                        t1 = interval.math.atan2_point(Iy.sup, Ix.inf)
                        t2 = interval.math.atan2_point(Iy.sup, Ix.sup)
                        return interval(t1.inf, t2.sup)
            else:
                if interval.zero_in(Iy) == True:
                    if Ix > 0.:
                        t1 = interval.math.atan2_point(Iy.inf, Ix.inf)
                        t2 = interval.math.atan2_point(Iy.sup, Ix.inf)
                        return interval(t1.inf, t2.sup)
                    else:
                        if Iy.inf < 0.:
                            t1 = interval.math.atan2_point(Iy.sup, Ix.sup)
                            tmp = interval.math.atan2_point(Iy.inf, Ix.sup)
                            t2 = itv_p2 + tmp
                            return interval(t1.inf, t2.sup)
                        else:
                            t1 = interval.math.atan2_point(Iy.sup, Ix.sup)
                            t2 = interval.math.atan2_point(Iy.inf, Ix.sup)
                            return interval(t1.inf, t2.sup)
                else:
                    if Ix > 0.:
                        if Iy > 0.:
                            t1 = interval.math.atan2_point(Iy.inf, Ix.sup)
                            t2 = interval.math.atan2_point(Iy.sup, Ix.inf)
                            return interval(t1.inf, t2.sup)
                        else:
                            t1 = interval.math.atan2_point(Iy.inf, Ix.inf)
                            t2 = interval.math.atan2_point(Iy.sup, Ix.sup)
                            return interval(t1.inf, t2.sup)
                    else:
                        if Iy > 0.:
                            t1 = interval.math.atan2_point(Iy.sup, Ix.sup)
                            t2 = interval.math.atan2_point(Iy.inf, Iy.inf)
                            return interval(t1.inf, t2.sup)
                        else:
                            t1 = interval.math.atan2_point(Iy.sup, Ix.inf)
                            t2 = interval.math.atan2_point(Iy.inf, Ix.sup)
                            return interval(t1.inf, t2.sup)

        def sinh_origin(x):
            itv_exph = interval.math.e()
            itv_coshh = (itv_exph + 1. / itv_exph) * 0.5
            r = interval(0.)
            y = interval(1.)
            eps = sys.float_info.epsilon
            i = 0
            while True:
                y *= x
                y /= interval(i)
                tmp = y * interval(-itv_coshh.sup, itv_coshh.sup)
                if interval.mag(tmp) < eps:
                    r += tmp
                    break
                else:
                    if i % 2 != 0:
                        r += y
                i += 1
            return r

        def sinh_point(x):
            if x >= -0.5 and x <= 0.5:
                return sinh_origin(x)
            else:
                if x == -float("inf"):
                    return -interval(sys.float_info.max, float("inf"))
                tmp = interval.math.exp_point(x)
                return (tmp - 1. / tmp) * 0.5

        def sinh(x):
            t1 = interval.math.sinh_point(x.inf)
            t2 = interval.math.sinh_point(x.sup)
            return interval(t1.inf, t2.sup)

        def cosh_point(x):
            if x == -float("inf"):
                return interval(sys.float_info.max, float("inf"))
            tmp = interval.math.exp_point(x)
            return (tmp + 1. / tmp) * 0.5

        def cosh(x):
            t1 = interval.math.cosh_point(x.inf)
            t2 = interval.math.cosh_point(x.sup)
            r = interval.hull(t1, t2)
            if interval.zero_in(x) == True:
                r = interval.hull(r, 1.)
            return r

        def tanh_point(x):
            if x > 0.5:
                return 1. - 2. / (1. + interval.math.exp_point(2. * x))
            elif x < -0.5:
                return 2. / (1. + interval.math.exp_point(-2. * x)) - 1.
            else:
                return interval.math.sinh_origin(x) / interval.math.cosh_point(x)

        def tanh(x):
            t1 = interval.math.tanh_point(x.inf)
            t2 = interval.math.tanh_point(x.sup)
            return interval(t1.inf, t2.sup)
