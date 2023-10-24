from copy import copy
from abc import ABC, abstractmethod
from typing import Set, Optional

from .graph import Graph, Node


class Solver(ABC):
    @abstractmethod
    def solve(self, graph: Graph, *args, **kwargs):
        return graph
    
    def defind_ways(self, nodeS: Node, nodeT: Node, given_route=None):
        first = False
        route = copy(given_route)
        if not route:
            route = (nodeS,)
            first = True
            routes = []
        else:
            route = route + (nodeS,)
        # print(nodeS, nodeS.adjects, nodeT, route)
        if nodeS is nodeT:
            # print('Конец')
            return route
        
        if not nodeS.adjects:
            # print('Пук пук')
            return []
        temp_routes = []
        for adject in nodeS.adjects:
            if not adject in route:
                if res := self.defind_ways(adject, nodeT, route):
                    if type(res) is list:
                        temp_routes += res
                    else:
                        temp_routes.append(res)
            if first and temp_routes:
                # print('Добавлен')
                for r in temp_routes:
                    routes.append(r)
                temp_routes = []

        if first:
            # print('Возвращен итог')
            return routes
        # print('Возвращен промежуток')
        return temp_routes

    def direct_transitive_closure(self, node: Node, t=None) -> Optional[Set[Node] | None]:
        '''Определяет прямое транзитивное замыкание указанного узла'''
        if not t:
            t = set()
        if node in t:
            return t
        t.add(node)
        # print(node, t)
        res = t
        for n in node.adjects:
            res |= self.direct_transitive_closure(n, t)
        # print(node, res)
        return res or None
    
    def reverse_transitive_closure(self, node: Node, t=None) -> Optional[Set[Node] | None]:
        '''Определяет обратное транзитивное замыкание указанного узла'''
        if not t:
            t = set()
        if node in t:
            return t
        t.add(node)
        res = t
        for n in node._reverse_adjects:
            res |= self.reverse_transitive_closure(n, t)
        return res or None
