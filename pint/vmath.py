# -*- coding: utf-8 -*-
from .core import roundfloat, roundmode
from .interval import interval
import math


def vmath():
    def sqrt(self, arg):
        if arg.__class__.__name__ == "interval":
            answer = interval(0.)
            answer.inf = roundfloat.rdsqrt(self.inf, roundmode.down)
            answer.sup = roundfloat.rdsqrt(self.sup, roundmode.up)
        else:
            answer = math.sqrt(arg)
        return answer
