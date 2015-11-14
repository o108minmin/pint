from .core import roundmode, roundfloat
from .interval import interval


class mcmatrix(list):

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
        return answer

    def __iadd__(self, arg):
        return mcmatrix.__add__(self, arg)

    def __radd__(self, arg):
        return mcmatrix.__add__(self, arg)

    def __sub__(self, arg):
        pass

    def __isub__(self, arg):
        pass

    def __rsub__(self, arg):
        pass

    def __mul__(self, arg):
        pass

    def __imul__(self, arg):
        pass
