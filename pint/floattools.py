#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import fractions

def stringtofraction(arg):
    if math.floor(float(arg)) != math.ceil(float(arg)):
        arg_up, arg_down = arg.split(".")
        ans = fractions.Fraction(0, 1)
        for i in range(0, len(arg_down)):
            ans += fractions.Fraction(int(arg_down[i]), 10 ** (i + 1))
        ans += fractions.Fraction(int(arg_up), 1)
    else:
        ans = fractions.Fraction(int(arg), 1)
    return ans
