# -*- coding: utf-8 -*-
from .core import roundfloat, roundmode
from .interval import interval
import math


class vmath:
    arg_type = None
    math_type = None
    return_type = None
    pn_class = ["interval"]

    def __init__(self, arg_type = None, math_type = None,return_type = None):
        self.arg_type = arg_type
        self.math_type = math_type
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
        if self.math_type != None:
            tmp = self.math_type(arg[0])
            arg_name = tmp.__class__.__name__
        else:
            arg_name = arg[0].__class__.__name__
        pn_class_much = [x for x in vmath.pn_class if x == arg_name]
        if len(pn_class_much) == 1:
            answer = arg[0].math.sqrt(arg[0])
        else:
            answer = math.sqrt(arg[0])
        if self.return_type != None:
            answer = self.return_type(answer)
        return answer
