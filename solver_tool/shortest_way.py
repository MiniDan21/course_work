from math import inf

from .solver import Solver
from .graph import *


class ShortestWay(Solver):
    '''Возвращает список кратчайших путей и их длину.'''
    def solve(self, graph: Graph, nodeS: Node, nodeT: Node):
        shortest_ways = []
        summary = inf
        if type(nodeS) is str or type(nodeT) is str:
            try:
                nodeS = graph.nodes[nodeS]
                nodeT = graph.nodes[nodeT]
            except KeyError:
                return [[], None]
        if nodeS is nodeT:
            return [[nodeS], 0] 
        routes = self.defind_ways(nodeS, nodeT)
        for route in routes:
            temp = 0
            last = None
            for node in route:
                if last:
                    temp += last.adjects[node]
                last = node
            if summary > temp:
                summary = temp
                shortest_ways = [route]
            elif summary == temp:
                shortest_ways.append(route)
        if summary is inf:
            summary = None
        return [shortest_ways, summary]