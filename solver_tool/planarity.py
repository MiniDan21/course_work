from itertools import combinations

from .solver import Solver
from .graph import *


# Укладка графа на плоскости (определить способ определения для класса Graph)
class Planarity(Solver):
    def solve(self, graph: Graph, *args, **kwargs):
        planarited = True
        while len(graph.info()) > 4:
            if len(graph.info()) == 6:
                # Основано на авторском алгоритме, где из 6 вершин находится подграф К3,3
                if self.define_K_3_3(graph):
                    planarited = False
                    break
            elif self.define_K_5(graph):
                planarited = False
                break

            # ИСПРАВИТЬ КОСТЫЛЬ ДЛЯ ДВУДОЛЬНЫХ ГРАФОВ
            value, edge = graph.define_minimal_adject()
            if value is inf:
                graph._del_node(edge)
            else:                    
                graph.tight_edge(edge[0], edge[1])

        return planarited

    def define_K_3_3(self, graph: Graph) -> bool:
        if len(graph.info()) != 6:
            return False
        left = set()
        right = set()
        # Если у кого-то 5 вершин, то по сути он со всеми связан, неважно в какую долю его запихивать, пока других не распределим
        five_edges = set()
        switch = False
        # for node in graph.info().keys():
        #     if switch:
        #         choose = right
        #         another = left
        #     else:
        #         choose = left
        #         another = right
        #     if len(node.adjects) < 3:
        #         return False
            
        #     # if node.name in left or node.name in right:
        #     #     continue

        #     if len(node.adjects) == 5:
        #         five_edges.add(node.name)
        #         continue

        #     if node.name not in another and len(choose) != 3:
        #         choose.add(node.name)

        #     for n in node.adjects.keys():
        #         if n.name not in another and n.name not in choose and len(n.adjects) != 5 and len(another) != 3:
        #             another.add(n.name)
        #         elif len(n.adjects) == 5:
        #             five_edges.add(n.name)
        #     switch = not switch
        #     print(choose, another)

        # for five in five_edges:
        #     if five not in right and five not in left:
        #         min(left, right, key=len).add(five)
                
        # print(left, right)
        # if len(left) != 3 or len(right) != 3:
        #     return False
        nodes = set(graph.info().keys())
        for node in nodes:
            if len(node.adjects) < 3:
                    return False
        cases = []
        
        for i in combinations(nodes, 3):
            for j in combinations(nodes - set(i), 3):
                cases.append((i, j,))
        # Проверка на то, что все вершины из противоположной доли являются смежными текущей вершине
        # for node in graph.info().keys():
        #     adjects = set(i.name for i in node.adjects.keys())
        #     result = set()
        #     if node.name in left:
        #         result = right - adjects
        #     if node.name in right:
        #         result = left - adjects
        #     if len(result) > 0:
        #         return False
        found = False
        for case in cases:
            left = set(case[0])
            right = set(case[1])
            for node in nodes:
                adjects = set(i.name for i in node.adjects.keys())
                result = set()
                if node in left:
                    result = right - adjects
                if node in right:
                    result = left - adjects
                if len(result) == 0:
                    found = True
                    break
        return found
    
    def define_K_5(self, graph: Graph) -> bool:
        if len(graph.info()) != 5:
            return False
        added = set()
        for node in graph.info().keys():
            if len(node.adjects) != 4:
                return False
            if node.name in added:
                continue
            added.add(node.name)
            [added.add(n.name) for n in node.adjects.keys() if n.name not in added]
        if len(added) != 5:
            return False
        return True
        