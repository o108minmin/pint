# -*- coding: utf-8 -*-
from .core import roundfloat, roundmode
from .interval import interval
import math


class vmath:
    arg_type = None
    return_type = None
    pn_class = ["interval"]

    def __init__(self, arg_type = None, math_type = None,return_type = None):
        self.arg_type = arg_type
        self.return_type = return_type

    def self_remove(args):
        args_tmp = list(args)
        if args[0].__class__.__name__ == "vmath":
            args_tmp.pop(0)
        return args_tmp

    def sqrt(*args):
        if args[0].__class__.__name__ == "vmath":
            self = args[0]
        else:
            self = vmath()
        arg = vmath.self_remove(args)
        if self.arg_type != None:
            arg[0] = self.arg_type(arg[0])
        arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            answer = arg[0].math.sqrt(arg[0])
        else:
            answer = math.sqrt(arg[0])
        if self.return_type != None:
            answer = self.return_type(answer)
        return answer

    def ceil(*args):
        if args[0].__class__.__name__ == "vmath":
            self = args[0]
        else:
            self = vmath()
        arg = vmath.self_remove(args)
        if self.arg_type != None:
            arg[0] = self.arg_type(arg[0])
        arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            answer = arg[0].math.ceil(arg[0])
        else:
            answer = math.ceil(arg[0])
        if self.return_type != None:
            answer = self.return_type(answer)
        return answer

    def copysign(*args):
        if args[0].__class__.__name__ == "vmath":
            self = args[0]
        else:
            self = vmath()
        arg = vmath.self_remove(args)
        if self.arg_type != None:
            arg[0] = self.arg_type(arg[0])
        arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            answer = arg[0].math.copysign(arg[0], arg[1])
        else:
            answer = math.copysign(arg[0], arg[1])
        if self.return_type != None:
            answer = self.return_type(answer)
        return answer

    def fabs(*args):
        if args[0].__class__.__name__ == "vmath":
            self = args[0]
        else:
            self = vmath()
        arg = vmath.self_remove(args)
        if self.arg_type != None:
            arg[0] = self.arg_type(arg[0])
        arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            answer = arg[0].math.fabs(arg[0])
        else:
            answer = math.fabs(arg[0])
        if self.return_type != None:
            answer = self.return_type(answer)
        return answer

    def factorial(*args):
        if args[0].__class__.__name__ == "vmath":
            self = args[0]
        else:
            self = vmath()
        arg = vmath.self_remove(args)
        if self.arg_type != None:
            arg[0] = self.arg_type(arg[0])
        arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            answer = arg[0].math.factorial(arg[0])
        else:
            answer = math.factorial(arg[0])
        if self.return_type != None:
            answer = self.return_type(answer)
        return answer

    def floor(*args):
        if args[0].__class__.__name__ == "vmath":
            self = args[0]
        else:
            self = vmath()
        arg = vmath.self_remove(args)
        if self.arg_type != None:
            arg[0] = self.arg_type(arg[0])
        arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            answer = arg[0].math.floor(arg[0])
        else:
            answer = math.floor(arg[0])
        if self.return_type != None:
            answer = self.return_type(answer)
        return answer

    def fmod(*args):
        if args[0].__class__.__name__ == "vmath":
            self = args[0]
        else:
            self = vmath()
        arg = vmath.self_remove(args)
        if self.arg_type != None:
            arg[0] = self.arg_type(arg[0])
            arg[1] = self.arg_type(arg[1])
        arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            answer = arg[0].math.fmod(arg[0], arg[1])
        else:
            answer = math.fmod(arg[0], arg[1])
        if self.return_type != None:
            answer = self.return_type(answer)
        return answer

    def frexp(*args):
        if args[0].__class__.__name__ == "vmath":
            self = args[0]
        else:
            self = vmath()
        arg = vmath.self_remove(args)
        if self.arg_type != None:
            arg[0] = self.arg_type(arg[0])
        arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            ans1, ans2 = arg[0].math.frexp(arg[0])
        else:
            ans1, ans2 = math.frexp(arg[0])
        if self.return_type != None:
            ans1 = self.return_type(ans1)
            ans2 = self.return_type(ans2)
        return ans1, ans2

    def fsum(*args):
        if args[0].__class__.__name__ == "vmath":
            self = args[0]
        else:
            self = vmath()
        arg = vmath.self_remove(args)
        if self.arg_type != None:
            arg[0] = self.arg_type(arg[0])
        arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            answer = arg[0].math.fsum(arg[0])
        else:
            answer = math.fsum(arg[0])
        if self.return_type != None:
            answer = self.return_type(answer)
        return answer

    def gcd(*args):
        if args[0].__class__.__name__ == "vmath":
            self = args[0]
        else:
            self = vmath()
        arg = vmath.self_remove(args)
        if self.arg_type != None:
            arg[0] = self.arg_type(arg[0])
            arg[1] = self.arg_type(arg[1])
        arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            answer = arg[0].math.gcd(arg[0], arg[1])
        else:
            answer = math.gcd(arg[0], arg[1])
        if self.return_type != None:
            answer = self.return_type(answer)
        return answer

    def isclose(*args, rel_tol = 1e-09, abs_tol = 0.0):
        if args[0].__class__.__name__ == "vmath":
            self = args[0]
        else:
            self = vmath()
        arg = vmath.self_remove(args)
        if self.arg_type != None:
            arg[0] = self.arg_type(arg[0])
        arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            t1 = rel_tol
            t2 = abs_tol
            answer = arg[0].math.isclose(arg[0], arg[1], rel_tol = t1, abs_tol = t2)
        else:
            answer = math.isclose(arg[0], arg[1], rel_tol = rel_tol, abs_tol = abs_tol)
        if self.return_type != None:
            answer = self.return_type(answer)
        return answer

    def isfinite(*args):
        if args[0].__class__.__name__ == "vmath":
            self = args[0]
        else:
            self = vmath()
        arg = vmath.self_remove(args)
        if self.arg_type != None:
            arg[0] = self.arg_type(arg[0])
        arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            answer = arg[0].math.isfinite(arg[0])
        else:
            answer = math.isfinite(arg[0])
        if self.return_type != None:
            answer = self.return_type(answer)
        return answer

    def isinf(*args):
        if args[0].__class__.__name__ == "vmath":
            self = args[0]
        else:
            self = vmath()
        arg = vmath.self_remove(args)
        if self.arg_type != None:
            arg[0] = self.arg_type(arg[0])
        arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            answer = arg[0].math.isinf(arg[0])
        else:
            answer = math.isinf(arg[0])
        if self.return_type != None:
            answer = self.return_type(answer)
        return answer

    def isnan(*args):
        if args[0].__class__.__name__ == "vmath":
            self = args[0]
        else:
            self = vmath()
        arg = vmath.self_remove(args)
        if self.arg_type != None:
            arg[0] = self.arg_type(arg[0])
        arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            answer = arg[0].math.isnan(arg[0])
        else:
            answer = math.isnan(arg[0])
        if self.return_type != None:
            answer = self.return_type(answer)
        return answer

    def ldexp(*args):
        if args[0].__class__.__name__ == "vmath":
            self = args[0]
        else:
            self = vmath()
        arg = vmath.self_remove(args)
        if self.arg_type != None:
            arg[0] = self.arg_type(arg[0])
        arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            answer = arg[0].math.ldexp(arg[0], arg[1])
        else:
            answer = math.ldexp(arg[0], arg[1])
        if self.return_type != None:
            answer = self.return_type(answer)
        return answer

    def modf(*args):
        if args[0].__class__.__name__ == "vmath":
            self = args[0]
        else:
            self = vmath()
        arg = vmath.self_remove(args)
        if self.arg_type != None:
            arg[0] = self.arg_type(arg[0])
        arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            ans1, ans2 = arg[0].math.modf(arg[0])
        else:
            ans1, ans2 = math.modf(arg[0])
        if self.return_type != None:
            ans1 = self.return_type(ans1)
            ans2 = self.return_type(ans2)
        return ans1, ans2

    def trunc(*args):
        if args[0].__class__.__name__ == "vmath":
            self = args[0]
        else:
            self = vmath()
        arg = vmath.self_remove(args)
        if self.arg_type != None:
            arg[0] = self.arg_type(arg[0])
        arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            answer = arg[0].math.trunc(arg[0])
        else:
            answer = math.trunc(arg[0])
        if self.return_type != None:
            answer = self.return_type(answer)
        return answer
