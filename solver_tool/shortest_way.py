from copy import deepcopy, copy
from math import inf

from .solver import Solver
from .graph import *


class ShortestWay(Solver):
    '''Возвращает список кратчайших путей и их длину.'''
    # def solve(self, graph: Graph, nodeS: Node, nodeT: Node):
    #     shortest_ways = []
    #     summary = inf
    #     if type(nodeS) is str or type(nodeT) is str:
    #         try:
    #             nodeS = graph.nodes[nodeS]
    #             nodeT = graph.nodes[nodeT]
    #         except KeyError:
    #             return [[], None]
    #     if nodeS is nodeT:
    #         return [[nodeS], 0] 
    #     routes = self.defind_ways(nodeS, nodeT)
    #     for route in routes:
    #         temp = 0
    #         last = None
    #         for node in route:
    #             if last:
    #                 temp += last.adjects[node]
    #             last = node
    #         if summary > temp:
    #             summary = temp
    #             shortest_ways = [route]
    #         elif summary == temp:
    #             shortest_ways.append(route)
    #     if summary is inf:
    #         summary = None
    #     return [shortest_ways, summary]
    
    def solve(self, graph: Graph, nodeS: Node, nodeT: Node):
        if type(nodeS) is str or type(nodeT) is str:
            try:
                nodeS = graph.nodes[nodeS]
                nodeT = graph.nodes[nodeT]
            except KeyError:
                return [[], None]
        if nodeS is nodeT:
            return [[nodeS], 0] 
        result = list(self.BellmanFord(graph=graph, nodeS=nodeS)[nodeT.name])
        if result[0] is inf:
            result[0] = None
        # Фронтенд в другом порядке принимает значения
        result[0], result[1] = result[1], result[0]
        return result
    
    def BellmanFord(self, graph: Graph, nodeS: Node) -> any:
        '''Метод на основе алгоритма Беллмана-Форда'''
        edges = self._read_edges(graph=graph)
        dist = {node: inf for node in graph.nodes}
        freeze_dist = deepcopy(dist) 
        predecessors = {node: set() for node in graph.nodes}
        dist[nodeS.name] = 0
        result = {}
        if not edges:
            return {i: ("Error: Некорректно указан вес", False) for i in predecessors}
        for _ in range(len(graph.nodes) - 1):
            for u, v, w in edges:
                if dist[u] != inf and dist[u] + w <= dist[v]:
                    if dist[u] + w in list(dist.values()):
                        predecessors[v].add(u)
                    else:
                        predecessors[v] = {u}

                    dist[v] = dist[u] + w

        for u, v, w in edges:
              if dist[u] != inf and dist[u] + w < dist[v]:
                return {i: ("Error: Отрицательная петля", False) for i in dist}
        
        
        # print(predecessors)
        for node, distance in dist.items():
            if predecessors[node] is not None:
                paths = self.spec_defind_ways(predecessors, node)
                result[node] = (distance, paths)
            else:
                result[node] = distance
        print(result)
        return result
    
    def _read_edges(self, graph: Graph) -> List[int]:
        '''Возвращает массив с ребрами типа [S, T, W]'''
        result = []
        data = graph.info()
        for v in data:
            for u, w in data[v].items():
                if type(w) is int or type(w) is float:
                    result.append([v.name, u.name, data[v][u]])
        
        return result
    
    # def spec_defind_ways(self, predecessors, nodeS, nodeT):
    #     paths = []
    #     base = []
    #     paths.append(base)
    #     # В будущем может быть множеством вершин, если есть разветвления
    #     current_node = nodeT
    #     last = set(nodeT)
    #     while current_node is not None:
    #         if type(current_node) is set:
    #             for node in current_node:
    #                 temp = deepcopy(base)

    #         # Добавляем в начало пути текущую вершину
    #         base.insert(0, current_node)
    #         last = set(nodeT)
    #         predecessors[nodeT]

    def spec_defind_ways(self, predecessors, nodeT):
        base = [nodeT]
        paths = [base]
        # for branches in predecessors.values():
        #     exludes |= branches
        # while exludes:
        #     temp_path = []
        #     self._dfs_help(predecessors, exludes, nodeS, nodeT, base)
        #     paths.append(copy(temp_path))
        preds = predecessors[nodeT]
        self._dfs_help(predecessors, preds, base, paths)

        return paths



    def _dfs_help(self, predecessors, preds, base, paths):
        if not preds:
            return
        temp_base = base
        copy_base = copy(base)
        # Счетчик, чтобы base сразу не заменили
        counter = 0
        for pred in preds:
            if len(preds) > 1 and counter:
                temp_base = copy(copy_base)
                paths.append(temp_base)
            temp_base.insert(0, pred)
            next_preds = predecessors[pred]
            self._dfs_help(predecessors, next_preds, temp_base, paths)
            counter += 1
