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

def verified_digits(x, y):
    digits = 0
    str_x = format(x, '.64f')
    str_y = format(y, '.64f')
    if len(str_x) > len(str_y):
        for i in range(0, len(str_x)):
            str_y += '0'
    elif len(str_y) > len(str_x):
        for i in range(0, len(str_y)):
            str_x += '0'
    if str_x.find('e') > 0:
        x_num, x_e = str_x.split('e')
    else:
        x_num = str_x
        x_e = 0
    if str_y.find('e') > 0:
        y_num, y_e = str_y.split('e')
    else:
        y_num = str_y
        y_e = 0
    if x_e != y_e:
        return 0
    if x_num.find('.') > 0:
        x_up, x_down = x_num.split('.')
    else:
        x_up = x_num
        x_down = ''
    if y_num.find('.') > 0:
        y_up, y_down = y_num.split('.')
    else:
        y_up = y_num
        y_down = ''
    if x_up == y_up:
        digits += len(x_up)
    else:
        if len(x_up) != len(y_up):
            return 0
        tf = [x_up[i] == y_up[i] for i in range(min([len(x_up), len(y_up)]))]
        tf.append(False)
        digits += tf.index(False)
        return digits
    if x_down == y_down:
        digits += len(x_down) + 1
    else:
        tf = [x_down[i] == y_down[i] for i in range(min([len(x_down), len(y_down)]))]
        tf.append(False)
        digits += tf.index(False) + 1
    return digits
