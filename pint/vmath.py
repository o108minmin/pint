# -*- coding: utf-8 -*-
from .core import roundfloat, roundmode
from .interval import interval
import math


def vmath():
    def sqrt(self, arg):
        #TODO: Make more better if else
        if arg.__class__.__name__ == "interval":
            answer = arg.math.sqrt(arg)
        else:
            answer = math.sqrt(arg)
        return answer
