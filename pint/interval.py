# -*- coding: utf-8 -*-

from .core import roundmode,roundfloat

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
            answer.inf = roundfloat.rdadd(self.inf, arg, roundmode.down)
            answer.sup = roundfloat.rdadd(self.sup, arg, roundmode.up)
        elif arg.__class__.__name__ == 'interval':
            answer.inf = roundfloat.rdadd(self.inf, arg.inf, roundmode.down)
            answer.sup = roundfloat.rdadd(self.sup, arg.sup, roundmode.up)
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
            answer.inf = roundfloat.rdsub(self.inf, arg, roundmode.down)
            answer.sup = roundfloat.rdsub(self.sup, arg, roundmode.up)
        elif arg.__class__.__name__ == 'interval':
            answer.inf = roundfloat.rdsub(self.inf, arg.sup, roundmode.down)
            answer.sup = roundfloat.rdsub(self.sup, arg.inf, roundmode.up)
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
                answer.inf = roundfloat.rdmul(self.inf, arg, roundmode.down)
                answer.sup = roundfloat.rdmul(self.sup, arg, roundmode.up)
            else:
                answer.inf = roundfloat.rdmul(self.sup, arg, roundmode.down)
                answer.sup = roundfloat.rdmul(self.inf, arg, roundmode.up)
        elif arg.__class__.__name__ == 'interval':
            if self.inf >= 0.:
                answer.inf = roundfloat.rdmul(
                    self.inf, arg.inf, roundmode.down)
                answer.sup = roundfloat.rdmul(
                    self.sup, arg.sup, roundmode.up)
            elif arg.sup <= 0.:
                answer.inf = roundfloat.rdmul(
                    self.sup, arg.inf, roundmode.down)
                answer.sup = roundfloat.rdmul(
                    self.sup, arg.sup, roundmode.up)
            else:
                answer.inf = roundfloat.rdmul(
                    self.sup, arg.inf, roundmode.down)
                answer.sup = roundfloat.rdmul(
                    self.sup, arg.sup, roundmode.up)
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
                answer.inf = roundfloat.rddiv(self.inf, arg, roundmode.down)
                answer.sup = roundfloat.rddiv(self.sup, arg, roundmode.up)
            elif arg < 0.:
                answer.inf = roundfloat.rddiv(self.sup, arg, roundmode.down)
                answer.sup = roundfloat.rddiv(self.inf, arg, roundmode.up)
            else:
                # TODO: nice error message
                print("error")
        elif arg.__class__.__name__ == 'interval':
            if arg.inf > 0.:
                if self.inf >= 0.:
                    answer.inf = roundfloat.rddiv(
                        self.inf, arg.sup, roundmode.down)
                    answer.sup = roundfloat.rddiv(
                        self.sup, arg.inf, roundmode.up)
                elif arg.sup < 0.:
                    answer.inf = roundfloat.rddiv(
                        self.inf, arg.inf, roundmode.down)
                    answer.sup = roundfloat.rddiv(
                        self.sup, arg.sup, roundmode.up)
                else:
                    answer.inf = roundfloat.rddiv(
                        self.inf, arg.inf, roundmode.down)
                    answer.sup = roundfloat.rddiv(
                        self.sup, arg.inf, roundmode.up)
            elif arg.sup < 0.:
                if self.inf >= 0.:
                    answer.inf = roundfloat.rddiv(
                        self.sup, arg.sup, roundmode.down)
                    answer.sup = roundfloat.rddiv(
                        self.inf, arg.inf, roundmode.up)
                elif self.sup < 0.:
                    answer.inf = roundfloat.rddiv(
                        self.sup, arg.inf, roundmode.down)
                    answer.sup = roundfloat.rddiv(
                        self.inf, arg.sup, roundmode.up)
                else:
                    answer.inf = roundfloat.rddiv(
                        self.sup, arg.sup, roundmode.down)
                    answer.sup = roundfloat.rddiv(
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

    def __radd__(self, arg):
        return interval.__add__(self, arg)

    def __sub__(self, arg):
        answer = interval(0.)
        if (arg.__class__.__name__ == 'int' or
            arg.__class__.__name__ == 'float'):
            answer.inf = roundfloat.rdsub(self.inf, arg, roundmode.down)
            answer.sup = roundfloat.rdsub(self.sup, arg, roundmode.up)
        elif arg.__class__.__name__ == 'interval':
            answer.inf = roundfloat.rdsub(self.inf, arg.sup, roundmode.down)
            answer.sup = roundfloat.rdsub(self.sup, arg.inf, roundmode.up)
        return answer

    def __isub__(self, arg):
        return interval.__sub__(self, arg)

    def __rsub__(self, arg):
        return interval.__sub__(self, arg)

    def __mul__(self, arg):
        answer = interval(0.)
        if arg.__class__.__name__ == 'int' or arg.__class__.__name__ == 'float':
            if arg >= 0.:
                answer.inf = roundfloat.rdmul(self.inf, arg, roundmode.down)
                answer.sup = roundfloat.rdmul(self.sup, arg, roundmode.up)
            else:
                answer.inf = roundfloat.rdmul(self.sup, arg, roundmode.down)
                answer.sup = roundfloat.rdmul(self.inf, arg, roundmode.up)
        elif arg.__class__.__name__ == 'interval':
            if self.inf >= 0.:
                answer.inf = roundfloat.rdmul(
                    self.inf, arg.inf, roundmode.down)
                answer.sup = roundfloat.rdmul(
                    self.sup, arg.sup, roundmode.up)
            elif arg.sup <= 0.:
                answer.inf = roundfloat.rdmul(
                    self.sup, arg.inf, roundmode.down)
                answer.sup = roundfloat.rdmul(
                    self.sup, arg.sup, roundmode.up)
            else:
                answer.inf = roundfloat.rdmul(
                    self.sup, arg.inf, roundmode.down)
                answer.sup = roundfloat.rdmul(
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
                answer.inf = roundfloat.rddiv(self.inf, arg, roundmode.down)
                answer.sup = roundfloat.rddiv(self.sup, arg, roundmode.up)
            elif arg < 0.:
                answer.inf = roundfloat.rddiv(self.sup, arg, roundmode.down)
                answer.sup = roundfloat.rddiv(self.inf, arg, roundmode.up)
            else:
                # TODO: nice error message
                print("error")
        elif arg.__class__.__name__ == 'interval':
            if arg.inf > 0.:
                if self.inf >= 0.:
                    answer.inf = roundfloat.rddiv(
                        self.inf, arg.sup, roundmode.down)
                    answer.sup = roundfloat.rddiv(
                        self.sup, arg.inf, roundmode.up)
                elif arg.sup < 0.:
                    answer.inf = roundfloat.rddiv(
                        self.inf, arg.inf, roundmode.down)
                    answer.sup = roundfloat.rddiv(
                        self.sup, arg.sup, roundmode.up)
                else:
                    answer.inf = roundfloat.rddiv(
                        self.inf, arg.inf, roundmode.down)
                    answer.sup = roundfloat.rddiv(
                        self.sup, arg.inf, roundmode.up)
            elif arg.sup < 0.:
                if self.inf >= 0.:
                    answer.inf = roundfloat.rddiv(
                        self.sup, arg.sup, roundmode.down)
                    answer.sup = roundfloat.rddiv(
                        self.inf, arg.inf, roundmode.up)
                elif self.sup < 0.:
                    answer.inf = roundfloat.rddiv(
                        self.sup, arg.inf, roundmode.down)
                    answer.sup = roundfloat.rddiv(
                        self.inf, arg.sup, roundmode.up)
                else:
                    answer.inf = roundfloat.rddiv(
                        self.sup, arg.sup, roundmode.down)
                    answer.sup = roundfloat.rddiv(
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

    def __neg__(self):
        return interval(-self.sup,-self.inf)

    # interval tools
    def hull(a, b):
        tmp1 = a.inf
        if b.inf < tmp1:
            tmp1 = b.inf
        tmp2 = a.sup
        if b.sup > tmp2:
            tmp2 = b.sup
        return interval(tmp1, tmp2)

    def whole():
        return interval(float("inf"), -float("inf"))

    #math functions
    class math:
        def sqrt(arg):
            answer = interval(0.)
            answer.inf = roundfloat.rdsqrt(arg.inf, roundmode.down)
            answer.sup = roundfloat.rdsqrt(arg.sup, roundmode.up)
            return answer

        def fabs(arg):
            if arg.inf >= 0.:
                return arg;
            if arg.sup <= 0.:
                return -arg;
            tmp = -arg.inf;
            if arg.sup > tmp:
                tmp = arg.sup;
            return interval(0., tmp);
