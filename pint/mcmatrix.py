# -*- coding: utf-8 -*-
from pint import roundmode, roundfloat
from .interval import interval


class mcmatrix(list):
    size = 0
    shape = 0
    def __init__(self, arg):
        list.__init__(self)
        if arg.__class__.__name__ == "list":
            for i in range(0, arg.__len__(), 1):
                if arg[i].__class__.__name__ == "list":
                    self.append(mcmatrix(arg[i]))
                else:
                    self.append(arg[i])
        else:
            self.append(arg[i])
        self.size = self.calcsize()
        self.shape = self.calcshape()

    def __add__(self, arg):
        answer = list()
        if arg.__class__.__name__ == "mcmatrix":
            for i in range(0, self.__len__(), 1):
                answer.append(self[i] + arg[i])
        else:
            for i in range(0, self.__len__(), 1):
                answer.append(self[i] + arg)
        return mcmatrix(answer)

    def __iadd__(self, arg):
        return mcmatrix.__add__(self, arg)

    def __radd__(self, arg):
        return mcmatrix.__add__(self, arg)

    def __sub__(self, arg):
        return mcmatrix.__add__(self, -arg)

    def __isub__(self, arg):
        return mcmatrix.__sub__(self, arg)

    def __rsub__(self, arg):
        return mcmatrix.__sub__(self, arg)

    def __mul__(self, arg):
        answer = list()
        for i in range(0, self.__len__(), 1):
            answer.append(self[i] * arg)
        return mcmatrix(answer)

    def __imul__(self, arg):
        return mcmatrix.__mul__(self, arg)

    def __rmul__(self, arg):
        return mcmatrix.__mul__(self, arg)

    def __truediv__(self, arg):
        return mcmatrix.__mul__(self, 1. / arg)

    def __itruediv__(self, arg):
        return mcmatrix.__truediv__(self, arg)

    def __rtruediv__(self, arg):
        answer = list()
        for i in range(0, self.__len__(), 1):
            answer.append(arg / self[i])
        return mcmatrix(answer)

    def __neg__(self):
        return mcmatrix.__mul__(self, -1.)

    #matrix methods
    def transpose(self):
        if self[0].__class__.__name__ == "mcmatrix":
            vertical = self.__len__()
            horiontal = self[0].__len__()
            answer = mcmatrix.zeros([horiontal,vertical])
            for i in range(0,horiontal,1):
                for j in range(0,vertical,1):
                    answer[i][j] = self[j][i]
        return answer

    def T(self):
        return mcmatrix.transpose(self)

    def numbers(shape, arg):
        answer = list()
        column = list()
        for j in range(0,shape[1],1):
            column.append(arg)
        for i in range(0,shape[0],1):
            answer.append(column)
        return mcmatrix(answer)

    def ones(shape):
        return mcmatrix.numbers(shape, 1.)

    def zeros(shape):
        return mcmatrix.numbers(shape, 0.)

    def calcsize(self):
        answer = 0
        for i in range(0,self.__len__(),1):
            if self[i].__class__.__name__ == "mcmatrix":
                answer += self[i].calcsize()
            else :
                answer += 1
        return answer

    def calcshape(self):
        if self[0].__class__.__name__ == "mcmatrix":
            return tuple(list([self.__len__(),self[0].__len__()]))
        else :
            return tuple(list([self.__len__()]))

    def dot(a, b):
        mata=a
        matb=b
        if (mata.__class__.__name__ != "mcmatrix" or
            matb.__class__.__name__ != "mcmatrix"):
            return mata*matb
        elif (mata[0].__class__.__name__ != "mcmatrix" and
            matb[0].__class__.__name__ != "mcmatrix"):
            answer = 0.
            for i in range(0,mata.__len__(),1):
                answer += mata[i] * matb[i]
            return answer
        vertical = mata.__len__()
        if mata[0].__class__.__name__ == "mcmatrix":
            lengthTemp = mata[0].__len__()
        else :
            lengthTemp = mata.__len__()
        lengthTemp = matb.__len__()
        if matb[0].__class__.__name__ == "mcmatrix":
            horiontal = matb[0].__len__()
        else :
            horiontal = matb.__len__()
        answer = mcmatrix.zeros([vertical,horiontal])
        #TODO: Change more fast algorithm e.g. loop unrolling
        for i in range(0,vertical,1):
            for j in range(0,horiontal,1):
                for k in range(0,lengthTemp,1):
                    answer[i][j] += mata[i][k] * matb[k][j]
        return answer

    #default list methods
    def append(self, object):
        answer = list.append(self,object)
        self.size = self.calcsize()
        self.shape = self.calcshape()
        return answer

    def extend(self, iterable):
        answer = list.append(self,iterable)
        self.size = self.calcsize()
        self.shape = self.calcshape()
        return answer

    def insert(self, index, object):
        answer = list.insert(self, index, object)
        self.size = self.calcsize()
        self.shape = self.calcshape()
        return answer

    def remove(self, value):
        answer = list.remove(self, value)
        self.size = self.calcsize()
        self.shape = self.calcshape()
        return answer

    def pop(self, *index):
        answer = list.pop(self, *index)
        self.size = self.calcsize()
        self.shape = self.calcshape()
        return answer

    def clear(self):
        answer = list.clear(self)
        self.size = self.calcsize()
        self.shape = self.calcshape()
        return answer
