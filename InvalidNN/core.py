# DAG 구조 표현
from multipledispatch import dispatch
from abc import *


class MetaNode(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):  # 노드 초기화
        pass

    @abstractmethod
    def __call__(self, k):  # 노드 호출(인자 iterable 이면 입력값 따로 적용)
        pass

    @abstractmethod
    def func(self, k):  # 노드에서 수행하는 연산
        pass


class Node(MetaNode):
    def __init__(self, name=None, upper=None):
        super().__init__()
        self.upper = upper
        self.name = name
        if upper and isinstance(upper, Graph):
            upper.add_node(self)

    def func(self, k):
        return k

    def __call__(self, k):
        if isinstance(k, tuple) or isinstance(k, list):
            result = []
            for i in k:
                result.append(self.func(i))
        else:
            result = self.func(k)

        return result


class CompressNode(Node):
    def __init__(self, name=None, upper=None):
        super().__init__(name, upper)

    def func(self, *args):
        return [*args]

    def __call__(self, *args):
        return self.func(*args)


class Graph(Node):
    def __init__(self, name=None, upper=None):
        super().__init__(name, upper)
        self._nodes = None

    def func(self, k):
        flow = k
        for node in self._nodes:
            flow = node.__call__(flow)
        return flow

    def add_node(self, other):
        self._nodes.append(other)
