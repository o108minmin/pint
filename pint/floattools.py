#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import fractions
'''
floattools

tools for floating point number

'''

def stringtofraction(arg):
    '''
    arg : str
    -> fractions.Fraction

    (jp)
    引数argから近似分数を生成します。
    返り値はfractions.Fractionとして返されます。
    詳細はfractionsを見てください。

    引数の形式は以下の通りです。

    # 整数
    stringtofraction("1")
    # 小数
    stringtofraction("0.1")
    # 指数表記
    stringtofraction("1e100")
    # 小数と指数表記
    stringtofraction("3.14e100")


    (en)
    Generate fractions.Fraction from arg

    Exsample
    # integer
    stringtofraction("1")
    # floating point number
    stringtofraction("0.1")
    stringtofraction("1e100")
    stringtofraction("3.14e100")
    '''
    if arg.find("e") >= 0:
        arg_num, arg_e = arg.split("e")
        e = fractions.Fraction(10, 1) ** int(arg_e)
    else:
        arg_num = arg
        e = fractions.Fraction(1, 1)
    if arg_num.find(".") >= 0:
        arg_up, arg_down = arg_num.split(".")
        ans = fractions.Fraction(int(arg_down), 10 ** len(arg_down))
        ans += fractions.Fraction(int(arg_up), 1)
    else:
        ans = fractions.Fraction(int(arg_num), 1)
    ans *= e
    return ans
