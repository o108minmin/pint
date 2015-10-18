# -*- coding: utf-8 -*-
#pint
#python interval library
#version 0.1.1
#まだ著作権関連の処理ができていないため、大変危険
import sys as __sys__
import math as __math__
from enum import IntEnum

class roundmode(IntEnum):
    up=1
    nearest=0
    down=-1

class roundfloat:
    def split(a):
        tmp=a*(2**27+1)
        x=tmp-(tmp-a)
        y=a-x
        return x,y

    def succ(a):
        absa=abs(a)
        if absa >= 2.**(-969):
            return a+absa*(2.**(-53)+2.**(-105))
        if absa< 2.**(-1021):
            return a+absa*2.**(-1074)
        c=2.**(53)*a
        e=(2.**(-53)+2.**(-105))*abs(c)
        return (c+e)*2.**(-53)

    def pred(a):
        absa=abs(a)
        if absa >= 2.**(-969):
            return a-absa*(2.**(-53)+2.**(-105))
        if absa < 2.**(-1021):
            return a-absa*2.**(-1074)
        c=2.**(53)*a
        e=(2.**(-53)+2.**(-105))*abs(c)
        return (c-e)*2.**(-53)

    def twosum(a,b):
        floatArg1=a
        floatArg2=b
        x=floatArg1 + floatArg2
        if abs(floatArg1)>abs(floatArg2):
            tmp=x-floatArg1
            y=floatArg2-tmp
        else:
            tmp=x-floatArg2
            y=floatArg1-tmp
        return x,y

    def twoproduct(a,b):
        floatArg1=a
        floatArg2=b
        x=floatArg1*floatArg2
        if abs(floatArg1) > 2.**996:
            floatArg1fix=floatArg1*2.**(-28)
            floatArg2fix=floatArg2*2.**(28)
        elif abs(floatArg2) > 2.**(996):
            floatArg1fix=floatArg1*2.**(28)
            floatArg2fix=floatArg2*2.**(-28)
        else:
            floatArg1fix=floatArg1
            floatArg2fix=floatArg2
        floatArg1SplitUp,floatArg1SplitDown=roundfloat.split(floatArg1fix)
        floatArg2SplitUp,floatArg2SplitDown=roundfloat.split(floatArg2fix)
        if abs(x) > 2.**1023:
            y=floatArg1SplitDown*floatArg2SplitDown-((((x*0.5)-(floatArg1SplitUp*0.5)*floatArg2SplitUp)*2.-floatArg1SplitDown*floatArg2SplitUp)-floatArg1SplitUp*floatArg2SplitDown)
        else:
            y=floatArg1SplitDown*floatArg2SplitDown-(((x-floatArg1SplitUp*floatArg2SplitUp)-floatArg1SplitDown*floatArg2SplitUp)-floatArg1SplitUp*floatArg2SplitDown)
        return x,y

    def roundadd(a,b,rmode=roundmode.nearest):
        floatArg1=float(a)
        floatArg2=float(b)
        x,y=roundfloat.twosum(floatArg1,floatArg2)
        if rmode==roundmode.up:
            if x == float('inf'):
                return x
            elif x == -float('inf'):
                if floatArg1 == -float('inf') or floatArg2 == -float('inf'):
                    return x
                else:
                    return -__sys__.float_info.max
            if y > 0:
                x=roundfloat.succ(x)
        elif rmode==roundmode.down:
            if x == float('inf'):
                if floatArg1 == float('inf') or floatArg2 == float('inf'):
                    return x
                else:
                    return __sys__.float_info.max
            elif x == -float('inf'):
                return x
            if y < 0:
                x=roundfloat.pred(x)
        return x

    def roundsub(a,b,rmode=roundmode.nearest):
        return roundfloat.roundadd(a,b,rmode)

    def roundmul(a,b,rmode=roundmode.nearest):
        floatArg1=float(a)
        floatArg2=float(b)
        x,y = roundfloat.twoproduct(floatArg1,floatArg2)
        if rmode == roundmode.up:
            if x == float('inf'):
                return x
            elif x == -float('inf'):
                if abs(floatArg1) == float('inf') or abs(floatArg2) == float('inf'):
                    return x
                else:
                    return -sys.float_info.max
            if abs(x) >= 2.**(-969):
                if y > 0:
                    x=roundfloat.succ(x)
        elif rmode==roundmode.down:
            if x == float('inf'):
                if abs(floatArg1) == float ('inf') or abs(floatArg2) == float ('inf') :
                    return x
                else :
                    return __sys__.float_info.max
            elif x == -float('inf'):
                return x

            if abs(x) >= 2.**(-969):
                if y < 0.:
                    return roundfloat.pred(x)
            else:
                s1, s2 = roundfloat.twoproduct(floatArg1*2.**537,floatArg2*2.**537)
                t = (x * 2.**537) * 2.**537
                if t > s1 or (t == s1 and s2 < 0.):
                    return roundfloat.pred(x)
        return x

    def rounddiv(a,b,rmode=roundmode.nearest):
        floatArg1=float(a)
        floatArg2=float(b)
        if rmode==roundmode.up:
            pass
            if floatArg1==0. or floatArg2==0. or abs(floatArg1) == float('inf') or abs(floatArg2) == float('inf') or floatArg1 != floatArg1 or floatArg2 != floatArg2:
                return floatArg1 / floatArg2
            if floatArg2 < 0.:
                floatArg1fix = -floatArg1
                floatArg2fix = -floatArg2
            else:
                floatArg1fix = floatArg1
                floatArg2fix = floatArg2
            if abs(floatArg1fix) < 2.**(-969):
                if abs(floatArg2fix) < 2.**918:
                    floatArg1fix *= 2.**105
                    floatArg2fix *= 2.**105
                else:
                    if floatArg1fix < 0.:
                        return 0.
                    else:
                        return 2.**(-1074)
            d=floatArg1fix / floatArg2fix
            if d==float('inf'):
                return d
            elif d == -float('inf'):
                return -__sys__.float_info.max

            x,y = roundfloat.twoproduct(d,floatArg2fix)
            if x < floatArg1fix or (x==floatArg1fix and y < 0.):
                return roundfloat.succ(d)
            return d
        elif rmode==roundmode.down:
            if floatArg1 == 0. or floatArg2 == 0. or abs(floatArg1) == float('inf') or abs(floatArg2) == float('inf') or floatArg1 != floatArg1 or floatArg2 != floatArg2:
                return floatArg1 / floatArg2
            if floatArg2 < 0.:
                floatArg1fix = -floatArg1
                floatArg2fix = -floatArg2
            else:
                floatArg1fix = floatArg1
                floatArg2fix = floatArg2

            if abs(floatArg1fix) < 2.**(-969):
                if abs(floatArg2fix) < 2.**918:
                    floatArg1fix *= 2.**105
                    floatArg2fix *= 2.**105
                else:
                    if floatArg1fix < 0.:
                        return -2.**(-1074)
                    else:
                        return 0

            d = floatArg1fix / floatArg2fix
            if d == float('inf'):
                return __sys__.float_info.max
            elif d == -float('inf'):
                return d
            x,y = roundfloat.twoproduct(d,floatArg2fix)
            if x > floatArg1fix or (x == floatArg1fix and y > 0.):
                return roundfloat.pred(d)
            return d

    def roundsqrt(x,rmode=roundmode.nearest):
        floatArg=float(x)
        d = __math__.sqrt(floatArg)
        if rmode == roundmode.up:
            if floatArg < 2.**(-969):
                a2 = floatArg * 2.**106
                d2 = d * 2.**53
                x,y=roundfloat.twoproduct(d2,d2)
                if x < a2 or (x == a2 and y < 0.):
                    d = roundfloat.succ(d)
            x,y=roundfloat.twoproduct(d,d)
            if x < floatArg or (x==floatArg and y < 0.):
                d=roundfloat.succ(d)
        if rmode == roundmode.down:
            if floatArg < 2.**(-969):
                a2 = floatArg * 2.**106
                d2 = d * 2.**53
                x,y=roundfloat.twoproduct(d2,d2)
                if x > a2 or (x == a2 and y > 0.):
                    d = roundfloat.pred(d)
            x,y=roundfloat.twoproduct(d,d)
            if x > floatArg or (x==floatArg and y > 0.):
                d=roundfloat.pred(d)
        return d

class interval:
    inf = 0.
    sup = 0.
    def __init__(self,*args):
        length=len(args)
        if length==1:
            self.inf=float(args[0])
            self.sup=float(args[0])
        elif length>=2:
            self.inf=float(args[0])
            self.sup=float(args[1])
        else:
            self.inf=0.
            self.sup=0.

    def __add__(self,arg):
        intervalArg=interval(0.)
        if arg.__class__.__name__=='int' or arg.__class__.__name__=='float':
            #down
            intervalArg.inf=roundfloat.roundadd(self.inf,arg,roundmode.down)
            #up
            intervalArg.sup=roundfloat.roundadd(self.sup,arg,roundmode.up)
        elif arg.__class__.__name__=='interval':
            #down
            intervalArg.inf=roundfloat.roundadd(self.inf,arg.inf,roundmode.down)
            #up
            intervalArg.sup=roundfloat.roundadd(self.sup,arg.sup,roundmode.up)
        return intervalArg

    def __iadd__(self,arg):
        return interval.__add__(self,arg)

    def __radd__(self,arg):
        return interval.__add__(self,arg)

    def __sub__(self,arg):
        intervalArg=interval(0.)
        if arg.__class__.__name__=='int' or arg.__class__.__name__=='float':
            #down
            intervalArg.inf=roundfloat.roundsub(self.inf,arg,roundmode.down)
            #up
            intervalArg.sup=roundfloat.roundsub(self.sup,arg,roundmode.up)
        elif arg.__class__.__name__=='interval':
            #down
            intervalArg.inf=roundfloat.roundsub(self.inf,arg.sup,roundmode.down)
            #intervalArg.inf=self.inf-arg.sup
            #up
            intervalArg.sup=roundfloat.roundsub(self.sup,arg.inf,roundmode.up)
            #intervalArg.sup=self.sup-arg.inf
        return intervalArg

    def __isub__(self,arg):
        return interval.__sub__(self,arg)

    def __rsub__(self,arg):
        return interval.__sub__(self,arg)

    def __mul__(self,arg):
        intervalAnswer = interval(0.)
        if arg.__class__.__name__=='int' or arg.__class__.__name__=='float':
            if arg >= 0.:
                #down
                intervalAnswer.inf = roundfloat.roundmul(self.inf,arg,roundmode.down)
                #up
                intervalAnswer.sup = roundfloat.roundmul(self.sup,arg,roundmode.up)
            else:
                #dowm
                intervalAnswer.inf = roundfloat.roundmul(self.sup,arg,roundmode.down)
                #up
                intervalAnswer.sup = roundfloat.roundmul(self.inf,arg,roundmode.up)
        elif arg.__class__.__name__=='interval':
            if self.inf >= 0.:
                #down
                intervalAnswer.inf = roundfloat.roundmul( self.inf,arg.inf,roundmode.down)
                #up
                intervalAnswer.sup = roundfloat.roundmul(self.sup,arg.sup,roundmode.up)
            elif arg.sup <= 0.:
                #down
                intervalAnswer.inf = roundfloat.roundmul(self.sup,arg.inf,roundmode.down)
                #up
                intervalAnswer.sup = roundfloat.roundmul(self.sup,arg.sup,roundmode.up)
            else:
                #down
                intervalAnswer.inf = roundfloat.roundmul(self.sup,arg.inf,roundmode.down)
                #up
                intervalAnswer.sup = roundfloat.roundmul(self.sup,arg.sup,roundmode.up)
        return intervalAnswer

    def __imul__(self,arg):
        return interval.__mul__(self,arg)

    def __rmul__(self,arg):
        return interval.__mul__(self,arg)

    def __truediv__(self,arg):
        intervalAnswer = interval(0.)
        if arg.__class__.__name__=='int' or arg.__class__.__name__=='float':
            if arg > 0.:
                #down
                intervalAnswer.inf = roundfloat.rounddiv(self.inf,arg,roundmode.down)
                #up
                intervalAnswer.sup = roundfloat.rounddiv(self.sup,arg,roundmode.up)
            elif arg < 0.:
                #down
                intervalAnswer.inf = roundfloat.rounddiv(self.sup,arg,roundmode.down)
                #up
                intervalAnswer.sup = roundfloat.rounddiv(self.inf,arg,roundmode.up)
            else:
                print("error")
        elif arg.__class__.__name__=='interval':
            if arg.inf > 0.:
                if self.inf >= 0.:
                    #down
                    intervalAnswer.inf = roundfloat.rounddiv(self.inf,arg.sup,roundmode.down)
                    #up
                    intervalAnswer.sup = roundfloat.rounddiv(self.sup,arg.inf,roundmode.up)
                elif arg.sup < 0.:
                    #down
                    intervalAnswer.inf = roundfloat.rounddiv(self.inf,arg.inf,roundmode.down)
                    #up
                    intervalAnswer.sup = roundfloat.rounddiv(self.sup,arg.sup,roundmode.up)
                else:
                    #down
                    intervalAnswer.inf = roundfloat.rounddiv(self.inf,arg.inf,roundmode.down)
                    #up
                    intervalAnswer.sup = roundfloat.rounddiv(self.sup,arg.inf,roundmode.up)
            elif arg.sup < 0.:
                if self.inf >= 0.:
                    intervalAnswer.inf = roundfloat.rounddiv(self.sup,arg.sup,roundmode.down)
                    intervalAnswer.sup = roundfloat.rounddiv(self.inf,arg.inf,roundmode.up)
                elif self.sup < 0.:
                    intervalAnswer.inf = roundfloat.rounddiv(self.sup,arg.inf,roundmode.down)
                    intervalAnswer.sup = roundfloat.rounddiv(self.inf,arg.sup,roundmode.up)
                else:
                    intervalAnswer.inf = roundfloat.rounddiv(self.sup,arg.sup,roundmode.down)
                    intervalAnswer.sup = roundfloat.rounddiv(self.inf,arg.sup,roundmode.up)
            else:
                pass
        return intervalAnswer

    def __itruediv__(self,arg):
        return interval.__truediv__(self,arg)

    def __rtruediv__(self,arg):
        return interval.__truediv__(self,arg)

    def __str__(self):
        return '['+str(self.inf)+','+str(self.sup)+']'

    def __repr__(self):
        return '['+repr(self.inf)+','+repr(self.sup)+']'

    def sqrt(self):
        answer = interval(0.)
        answer.inf = roundfloat.roundsqrt(self.inf,roundmode.down)
        answer.sup = roundfloat.roundsqrt(self.sup,roundmode.up)
        return answer


