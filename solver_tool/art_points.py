from typing import List, Tuple

from .solver import Solver
from .graph import *


# Поиск точек сочленения. Теорема: вершина является точкой сочленения, если существует пара вершин, 
# для которых в любом пути между ними лежит данная вершина
class ArtPoints(Solver):
    '''Поиск множества точек сочленения для 1-связных графов.'''
    def __set_crossing(self, routes: List[Tuple[Node]]):
        void = set()
        for r in routes:
            if void:
                void &= set(r)
            else:
                void = set(r)
        return void

    def solve(self, graph: Graph, *args, **kwargs):
        res = set()
        for nodeS in graph.info():
            for nodeT in graph.info():
                if nodeS is not nodeT:
                    res |= self.__set_crossing(self.defind_ways(nodeS, nodeT)) - {nodeS, nodeT}
        return res or {}
