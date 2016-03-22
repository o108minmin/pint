#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .core import roundmode as rdm
from .core import roundfloat as rf
import math
import sys
from .floattools import stringtofraction

class interval:
    '''
    (jp)
    区間型クラス
    メンバー変数
        - inf
            infは区間の下端である
        - sup
            supは区間の上端である
        - format_spec
            format()を使用する際の第二引数
            format(self, format_spec)のように呼び出される。

            self.format_spec = '.32g'

            のように指定する。
    注意点
        - 端点にはfloat型しか取ることができない


    (en)
    interval class
    member variables
        - inf
            inf is infimum of the interval
        - sup
            sup is supremum of the interval
        - format_spec
            The second parameter of format()
    warning
        - This class is only for float class
    '''

    inf = 0.
    sup = 0.
    format_spec = ''

    def __init__(self, *args):
        length = len(args)
        if length == 0:
            self.sup = 0.
            self.inf = 0.
        else:
            if length >= 1:
                if args[0].__class__.__name__ == "interval":
                    self.inf = args[0].inf
                    self.sup = args[0].sup
                elif args[0].__class__.__name__ == "str":
                    a0 = stringtofraction(args[0])
                    self.inf = rf.rddiv(a0.numerator, a0.denominator, rdm.down)
                    self.sup = rf.rddiv(a0.numerator, a0.denominator, rdm.up)
                else:
                    self.inf = args[0]
                    self.sup = args[0]
            if length >= 2:
                if args[0].__class__.__name__ == "interval":
                    self.sup = args[1].sup
                if args[1].__class__.__name__ == "str":
                    a1 = stringtofraction(args[1])
                    self.sup = rf.rddiv(a1.numerator, a1.denominator, rdm.up)
                else:
                    self.sup = args[1]

    def __add__(self, arg):
        ans = interval(0.)
        if arg.__class__.__name__ == 'interval':
            ans.inf = rf.rdadd(self.inf, arg.inf, rdm.down)
            ans.sup = rf.rdadd(self.sup, arg.sup, rdm.up)
        else:
            ans.inf = rf.rdadd(self.inf, arg, rdm.down)
            ans.sup = rf.rdadd(self.sup, arg, rdm.up)
        return ans

    def __iadd__(self, arg):
        return interval.__add__(self, arg)

    def __radd__(self, arg):
        return interval.__add__(self, arg)

    def __sub__(self, arg):
        ans = interval(0.)
        if arg.__class__.__name__ == 'interval':
            ans.inf = rf.rdsub(self.inf, arg.sup, rdm.down)
            ans.sup = rf.rdsub(self.sup, arg.inf, rdm.up)
        else:
            ans.inf = rf.rdsub(self.inf, arg, rdm.down)
            ans.sup = rf.rdsub(self.sup, arg, rdm.up)
        return ans

    def __isub__(self, arg):
        return interval.__sub__(self, arg)

    def __rsub__(self, arg):
        return interval.__add__(-self, arg)

    def __mul__(self, arg):
        ans = interval(0.)
        if arg.__class__.__name__ == 'interval':
            if interval.zero_in(arg) is True:
                if interval.zero_in(self) is True:
                    ans.inf = rf.rdmul(self.inf, arg.sup, rdm.down)
                    tmp = rf.rdmul(self.sup, arg.inf, rdm.down)
                    if ans.inf > tmp:
                        ans.inf = tmp
                    ans.sup = rf.rdmul(self.inf, arg.inf, rdm.up)
                    tmp = rf.rdmul(self.sup, arg.sup, rdm.up)
                    if ans.sup < tmp:
                        ans.sup = tmp
                elif self.inf >= 0.:
                    ans.inf = rf.rdmul(self.sup, arg.inf, rdm.down)
                    ans.sup = rf.rdmul(self.sup, arg.sup, rdm.up)
                elif self.sup <= 0.:
                    ans.inf = rf.rdmul(self.inf, arg.sup, rdm.down)
                    ans.sup = rf.rdmul(self.inf, arg.inf, rdm.up)
            elif arg.inf >= 0.:
                if interval.zero_in(self) is True:
                    ans.inf = rf.rdmul(self.inf, arg.sup, rdm.down)
                    ans.sup = rf.rdmul(self.sup, arg.sup, rdm.up)
                elif self.inf >= 0.:
                    ans.inf = rf.rdmul(self.inf, arg.inf, rdm.down)
                    ans.sup = rf.rdmul(self.sup, arg.sup, rdm.up)
                elif self.sup <= 0.:
                    ans.inf = rf.rdmul(self.inf, arg.sup, rdm.down)
                    ans.sup = rf.rdmul(self.sup, arg.inf, rdm.up)
            elif arg.sup <= 0.:
                if interval.zero_in(self) is True:
                    ans.inf = rf.rdmul(self.sup, arg.inf, rdm.down)
                    ans.sup = rf.rdmul(self.inf, arg.inf, rdm.up)
                elif self.inf >= 0.:
                    ans.inf = rf.rdmul(self.sup, arg.inf, rdm.down)
                    ans.sup = rf.rdmul(self.inf, arg.sup, rdm.up)
                elif self.sup <= 0.:
                    ans.inf = rf.rdmul(self.sup, arg.sup, rdm.down)
                    ans.sup = rf.rdmul(self.inf, arg.inf, rdm.up)
        else:
            if arg >= 0.:
                ans.inf = rf.rdmul(self.inf, arg, rdm.down)
                ans.sup = rf.rdmul(self.sup, arg, rdm.up)
            elif arg < 0.:
                ans.inf = rf.rdmul(self.sup, arg, rdm.down)
                ans.sup = rf.rdmul(self.inf, arg, rdm.up)
        return ans

    def __imul__(self, arg):
        return interval.__mul__(self, arg)

    def __rmul__(self, arg):
        return interval.__mul__(self, arg)

    def __truediv__(self, arg):
        ans = interval(0.)
        if arg.__class__.__name__ == 'interval':
            if arg.inf > 0.:
                if self.inf >= 0.:
                    ans.inf = rf.rddiv(
                        self.inf, arg.sup, rdm.down)
                    ans.sup = rf.rddiv(
                        self.sup, arg.inf, rdm.up)
                elif arg.sup < 0.:
                    ans.inf = rf.rddiv(
                        self.inf, arg.inf, rdm.down)
                    ans.sup = rf.rddiv(
                        self.sup, arg.sup, rdm.up)
                else:
                    ans.inf = rf.rddiv(
                        self.inf, arg.inf, rdm.down)
                    ans.sup = rf.rddiv(
                        self.sup, arg.inf, rdm.up)
            elif arg.sup < 0.:
                if self.inf >= 0.:
                    ans.inf = rf.rddiv(
                        self.sup, arg.sup, rdm.down)
                    ans.sup = rf.rddiv(
                        self.inf, arg.inf, rdm.up)
                elif self.sup < 0.:
                    ans.inf = rf.rddiv(
                        self.sup, arg.inf, rdm.down)
                    ans.sup = rf.rddiv(
                        self.inf, arg.sup, rdm.up)
                else:
                    ans.inf = rf.rddiv(
                        self.sup, arg.sup, rdm.down)
                    ans.sup = rf.rddiv(
                        self.inf, arg.sup, rdm.up)
            else:
                if arg > 0.:
                    ans.inf = rf.rddiv(self.inf, arg, rdm.down)
                    ans.sup = rf.rddiv(self.sup, arg, rdm.up)
                elif arg < 0.:
                    ans.inf = rf.rddiv(self.sup, arg, rdm.down)
                    ans.sup = rf.rddiv(self.inf, arg, rdm.up)
                elif arg == 0.:
                    sys.stderr.write("ZeroDivisionError ")
                    sys.exit()
        else:
            ans = interval.__truediv__(self, interval(arg))
        return ans

    def __itruediv__(self, arg):
        return interval.__truediv__(self, arg)

    def __rtruediv__(self, arg):
        # arg / self(interval)
        ans = interval(0.)
        if self.inf > 0. or self.sup < 0.:
            if arg >= 0.:
                ans.inf = rf.rddiv(arg, self.sup, rdm.down)
                ans.sup = rf.rddiv(arg, self.inf, rdm.up)
            else:
                ans.inf = rf.rddiv(arg, self.inf, rdm.down)
                ans.sup = rf.rddiv(arg, self.sup, rdm.up)
        elif self == 0.:
            sys.stderr.write("ZeroDivisionError ")
            sys.exit()
        return ans

    @staticmethod
    def format(arg, *format_spec):
        if len(format_spec) != 0 and format_spec[0] != '':
            ans_inf = format(arg.inf, format_spec[0])
            ans_sup = format(arg.sup, format_spec[0])
        elif arg.format_spec != '':
            ans_inf = format(arg.inf, arg.format_spec)
            ans_sup = format(arg.sup, arg.format_spec)
        else:
            ans_inf = format(arg.inf)
            ans_sup = format(arg.sup)
        return '[' + ans_inf + ',' + ans_sup + ']'

    def __format__(self, *format_spec):
        return self.format(self, *format_spec)

    def str(self):
        ans_inf = str(self.inf)
        ans_sup = str(self.sup)
        return '[' + ans_inf + ',' + ans_sup + ']'

    def __str__(self, *args):
        return self.str()

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
        else:
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
        else:
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
        else:
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
        else:
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
        else:
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
        else:
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
        ans = rf.rdsub(x.sup, x.inf)
        return ans

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
        '''
        math functions

        calling exsample

        interval.math.sqrt(interval(2.))
        '''

        @staticmethod
        def e():
            return interval(math.e, rf.succ(math.e))

        @staticmethod
        def pi():
            return interval(math.pi, rf.succ(math.pi))

        @staticmethod
        def sqrt(arg):
            ans = interval(0.)
            ans.inf = rf.rdsqrt(arg.inf, rdm.down)
            ans.sup = rf.rdsqrt(arg.sup, rdm.up)
            return ans

        @staticmethod
        def fabs(arg):
            if arg.inf >= 0.:
                return arg
            if arg.sup <= 0.:
                return -arg
            tmp = -arg.inf
            if arg.sup > tmp:
                tmp = arg.sup
            return interval(0., tmp)

        @staticmethod
        def isnan(arg):
            if arg.inf != arg.inf:
                return True
            if arg.sup != arg.sup:
                return True
            return False

        @staticmethod
        def isinf(arg):
            if arg.inf == float("inf") or arg.inf == float("-inf"):
                return True
            if arg.sup == float("inf") or arg.sup == float("-inf"):
                return True
            return False

        @staticmethod
        def isfinite(arg):
            if interval.math.isnan(arg) is True:
                return False
            if interval.math.isinf(arg) is True:
                return False
            return True

        @staticmethod
        def pow_point(x, i):
            ans = interval(1.)
            xp = interval(x)
            while i != 0:
                if i % 2 != 0:
                    ans *= xp
                i = i // 2
                xp *= xp
            return ans

        @staticmethod
        def pow(x, i):
            if i.__class__.__name__ == "interval":
                return interval.math.exp(i * interval.math.log(x))
            ans = interval(0.)
            xp = interval(0.)
            if i == 0:
                return interval(1.)
            if i >= 0:
                a = i
            else:
                a = -i
            if a % 2 == 0 and interval.number_in(x, 0):
                ans = interval.hull(0., interval.math.pow_point(x.mag(), a))
            else:
                ans = interval.hull(interval.math.pow_point(x.inf, a), interval.math.pow_point(x.sup, a))
            if i < 0.:
                ans = 1. / ans
            return ans

        @staticmethod
        def ln2():
            eps = sys.float_info.epsilon
            x2 = interval.math.sqrt(interval.math.sqrt(interval(2.)))
            x2m1 = x2 - 1.
            cinv = 1. / interval.hull(x2, 1.)
            tmp = interval(0.)
            xn = interval(-1.)
            xn2 = interval(-1.)
            i = 1
            while True:
                xn = -xn * x2m1
                xn2 = -xn2 * cinv * x2m1
                t = xn2 / interval(i)
                if interval.mag(t) < eps:
                    tmp += t
                    break
                else:
                    tmp += xn / interval(i)
                i += 1
            tmp = tmp * 4
            return tmp

        @staticmethod
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
            i = 1
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

        @staticmethod
        def exp(x):
            tmp1 = interval.math.exp_point(x.inf)
            tmp2 = interval.math.exp_point(x.sup)
            return interval(tmp1.inf, tmp2.sup)

        def expm1_origin(x):
            ans = interval(0.)
            y = interval(1.)
            sqrt_e = interval.math.sqrt(interval.math.e())
            re = interval((1. / sqrt_e).inf, sqrt_e.sup)
            i = 1.
            while True:
                y *= x
                y /= i
                if y.mag() * re.sup < sys.float_info.epsilon:
                    ans += y * re
                    break
                else:
                    ans += y
                i += 1.
            return ans

        @staticmethod
        def expm1_point(x):
            if x >= -0.5 and x <= 0.5:
                return interval.math.expm1_origin(x)
            else:
                return interval.math.exp_point(x) - 1.

        @staticmethod
        def expm1(x):
            ans_inf = interval.math.expm1_point(x.inf)
            ans_sup = interval.math.expm1_point(x.sup)
            return interval(ans_inf.inf, ans_sup.sup)

        @staticmethod
        def ldexp(x, i):
            return x * (2 ** i)

        @staticmethod
        def log_point(x, rd):
            eps = sys.float_info.epsilon
            itv_sqrt2 = interval.math.sqrt(interval(2.))
            if x == float("inf"):
                if rd == 1:
                    return float("inf")
                else:
                    return sys.float_info.max
            if x == 0.:
                if rd == 1:
                    return -sys.float_info.max
                else:
                    return -float("inf")
            x2, p_i = math.frexp(x)
            p = p_i
            while x2 > 4. * math.sqrt(2.) - 4.:
                x2 = x2 * 0.5
                p = p + 1.
            while x2 > 4. - 2. * math.sqrt(2.):
                tmp = x2 / itv_sqrt2
                if rd == -1:
                    x2 = tmp.inf
                else:
                    x2 = tmp.sup
                p += 0.5
            while x2 < 2. - math.sqrt(2.):
                x2 *= 2.
                p -= 1.
            while x2 < 2. * math.sqrt(2.) - 2.:
                tmp = x2 * itv_sqrt2
                if rd == -1:
                    x2 = tmp.inf
                else:
                    x2 = tmp.sup
                p -= 0.5
            x2m1 = x2 - 1.
            cinv = 1. / interval.hull(x2, 1.)
            r = interval(0.)
            xn = interval(-1.)
            xn2 = interval(-1.)
            i = 1
            while True:
                xn = -xn * x2m1
                xn2 = -xn2 * cinv * x2m1
                tmp = xn2 / interval(i)
                if interval.mag(tmp) < eps:
                    r += tmp
                    break
                else:
                    r += xn / interval(i)
                i += 1
            r += interval.math.ln2() * p
            if rd == -1:
                return r.inf
            else:
                return r.sup

        @staticmethod
        def log(x, base=math.e):
            if x.inf < 0.:
                sys.stderr.write("math domain error ")
                sys.exit()
            t1 = interval.math.log_point(x.inf, -1)
            t2 = interval.math.log_point(x.sup, 1)
            if base != math.e:
                b1 = interval.math.log_point(base, -1)
                b2 = interval.math.log_point(base, 1)
                return interval(t1, t2) / interval(b1, b2)
            else:
                return interval(t1, t2)

        @staticmethod
        def log2(x):
            return interval.math.log(x, 2)

        @staticmethod
        def log10(x):
            return interval.math.log(x, 10)

        @staticmethod
        def log1p_origin(x):
            eps = sys.float_info.epsilon
            cinv = 1. / interval.hull(x + interval(1.), 1.)
            r = interval(0.)
            xn = interval(-1.)
            xn2 = interval(-1.)
            i = 1
            while True:
                xn = -xn * x
                xn2 = -xn2 * cinv * x
                tmp = xn2 / interval(i)
                if interval.mag(tmp) < eps:
                    r += xn2 / interval(i)
                    break
                else:
                    r += xn / interval(i)
                i += 1
            return r

        @staticmethod
        def log1p_point(x, rd):
            f3m2sqrt2 = 3. - 2. * math.sqrt(2.)
            if x >= -f3m2sqrt2 and x <= f3m2sqrt2:
                tmp = interval.math.log1p_origin(x)
                if rd == -1:
                    return tmp.inf
                else:
                    return tmp.sup
            else:
                tmp = x + interval(1.)
                if rd == -1:
                    return interval.math.log_point(tmp.inf, -1)
                else:
                    return interval.math.log_point(tmp.sup, 1)

        @staticmethod
        def log1p(x):
            if x.inf < -1.:
                sys.stderr.write("math domain error ")
                sys.exit()
            else:
                t1 = interval.math.log1p_point(x.inf, -1)
                t2 = interval.math.log1p_point(x.sup, 1)
                return (t1, t2)

        @staticmethod
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

        @staticmethod
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

        @staticmethod
        def sin(x):
            itv_pi = interval.math.pi()
            itv_pi2 = itv_pi * 2.
            if interval.math.isinf(x) is True:
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

        @staticmethod
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

        @staticmethod
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

        @staticmethod
        def cos(x):
            itv_pi = interval.math.pi()
            itv_pi2 = itv_pi * 2.
            if interval.math.isinf(x) is True:
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

        @staticmethod
        def tan_point(x):
            tmp1 = interval.math.sin_point(interval(x))
            tmp2 = interval.math.cos_point(interval(x))
            return tmp1 / tmp2

        @staticmethod
        def tan(x):
            itv_pi = interval.math.pi()
            itv_pih = itv_pi * 0.5
            if interval.math.isinf(x) is True:
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

        @staticmethod
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

        @staticmethod
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

        @staticmethod
        def atan(x):
            t1 = interval.math.atan_point(x.inf)
            t2 = interval.math.atan_point(x.sup)
            return interval(t1.inf, t2.sup)

        @staticmethod
        def asin_point(x):
            itv_pi = interval.math.pi()
            itv_pih = itv_pi * 0.5
            if x < -1. or x > 1.:
                sys.stderr.write("math domain error ")
                sys.exit()
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

        @staticmethod
        def asin(x):
            t1 = interval.math.asin_point(x.inf)
            t2 = interval.math.asin_point(x.sup)
            return interval(t1.inf, t2.sup)

        @staticmethod
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

        @staticmethod
        def acos_point(x):
            itv_pi = interval.math.pi()
            if x < -1. or x > 1.:
                sys.stderr.write("math domain error ")
                sys.exit()
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

        @staticmethod
        def acos(x):
            t1 = interval.math.acos_point(x.sup)
            t2 = interval.math.acos_point(x.inf)
            return interval(t1.inf, t2.sup)

        @staticmethod
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

        @staticmethod
        def atan2(Iy, Ix):
            itv_pi = interval.math.pi()
            itv_pi2 = itv_pi * 2.
            if interval.zero_in(Ix) is True:
                if interval.zero_in(Iy) is True:
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
                if interval.zero_in(Iy) is True:
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

        @staticmethod
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

        @staticmethod
        def sinh_point(x):
            if x >= -0.5 and x <= 0.5:
                return sinh_origin(x)
            else:
                if x == -float("inf"):
                    return -interval(sys.float_info.max, float("inf"))
                tmp = interval.math.exp_point(x)
                return (tmp - 1. / tmp) * 0.5

        @staticmethod
        def sinh(x):
            t1 = interval.math.sinh_point(x.inf)
            t2 = interval.math.sinh_point(x.sup)
            return interval(t1.inf, t2.sup)

        @staticmethod
        def cosh_point(x):
            if x == -float("inf"):
                return interval(sys.float_info.max, float("inf"))
            tmp = interval.math.exp_point(x)
            return (tmp + 1. / tmp) * 0.5

        @staticmethod
        def cosh(x):
            t1 = interval.math.cosh_point(x.inf)
            t2 = interval.math.cosh_point(x.sup)
            r = interval.hull(t1, t2)
            if interval.zero_in(x) is True:
                r = interval.hull(r, 1.)
            return r

        @staticmethod
        def tanh_point(x):
            if x > 0.5:
                return 1. - 2. / (1. + interval.math.exp_point(2. * x))
            elif x < -0.5:
                return 2. / (1. + interval.math.exp_point(-2. * x)) - 1.
            else:
                return interval.math.sinh_origin(x) / interval.math.cosh_point(x)

        @staticmethod
        def tanh(x):
            t1 = interval.math.tanh_point(x.inf)
            t2 = interval.math.tanh_point(x.sup)
            return interval(t1.inf, t2.sup)

        @staticmethod
        def asinh_point(x):
            if x < -0.5:
                tmp = interval.math.sqrt(1. + interval(x) * x)
                return -interval.math.log(-x + interval.math.sqrt(1. + interval(x) * x))
            elif x <= 0.5:
                tmp = 1. + interval.math.sqrt(1. + interval(x) * x)
                return interval.math.log1p((1. + x / tmp) * x)
            else:
                return interval.math.sqrt(x + interval.math.sqrt(1. + interval(x) * x))

        @staticmethod
        def asinh(x):
            t1 = interval.math.asinh_point(x.inf)
            t2 = interval.math.asinh_point(x.sup)
            return interval(t1.inf, t2.sup)

        @staticmethod
        def acosh_point(x):
            if x < -0.5:
                sys.stderr.write("math domain error ")
                sys.exit()

            elif x == 1.:
                return interval(0.)
            elif x <= 1.5:
                y = interval(x - 1.)
                return interval.math.log1p(y + interval.math.sqrt((interval(x) + 1.)))
            else:
                return interval.math.log(x + interval.math.sqrt(interval(x) * x - 1.))

        @staticmethod
        def acosh(x):
            t1 = interval.math.acosh_point(x.inf)
            t2 = interval.math.acosh_point(x.sup)
            return interval(t1.inf, t2.sup)

        @staticmethod
        def hypot(x, y):
            if x * x == interval(float("inf")) or y * y == interval(float("inf")):
                max_arg = max(x, y)
                min_arg = min(x, y)
                ans = max_arg * interval.math.sqrt(1. + (max_arg / min_arg) ** 2)
                return ans
            else:
                return interval.math.sqrt(x * x + y * y)
