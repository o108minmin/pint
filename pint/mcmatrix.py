from .core import roundmode, roundfloat
from .interval import interval


class mcmatrix(list):
    #size=mcmatrix.
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
