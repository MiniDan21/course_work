from math import inf
import json
from random import sample
from typing import List, Optional, Tuple, Dict


class Node:
    count = 0
    def __init__(self, name = 'X' + str(count)) -> None:
        self.count = Node.count + 1
        Node.count += 1
        self.name = name
        self._adjects = dict()
        self._reverse_adjects = []

    def _define_adject(self, adject, weight):
        # Добавление данной вершины в список обратного отображения переданной вершины
        adject._reverse_adjects.append(self)
        self._adjects.update({adject: weight})

    def _random_adject(self):
        if self._adjects:
            for key, val in self._adjects.items():
                return key
        return False

    @property
    def adjects(self):
        return self._adjects 
    
    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name
        
    def __lt__(self, other):
        return str(self) < str(other)
    
    def __iter__(self):
        return self.name
    
    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, o)

class Graph:
    def __init__(self, nodes: Tuple[Node], directed_graph: bool = False, weighted_graph: bool = False):
        self.__directed = directed_graph
        self.__weighted = weighted_graph
        self.nodes = {node.name: node for node in nodes}

    def meta_info(self):
        return {"directed": self.__directed, "wighted": self.__weighted}
    
    def info(self):
        return {n: n.adjects for n in self.nodes.values()}
    
    def random_node_cuple(self):
        return sample(sorted(self.nodes.values()), k=2)

    def _del_node(self, node: Node) -> bool:
        if self.nodes.get(node.name):
            del self.nodes[node.name]
            return True
        return False
    
    def define_minimal_adjects_count(self) -> List[Node | None]:
        min_nodes = []
        minimum = inf
        for node, adjects in self.info().items():
            l = len(adjects)
            if l == minimum:
                min_nodes.append(node)
            elif l < minimum:
                min_nodes = [node]
                minimum = l
        return min_nodes

    def tight_edge(self, first: Node, second: Node) -> bool:
        '''Удаляется first, стягиваясь с second'''
        if not first in second.adjects.keys() or not second in first.adjects.keys():
            return False
        for adject in first.adjects:
            # Принебрегаем весом, определяем лишь планарость
            if not second is adject:
                second._define_adject(adject=adject, weight=1)
                adject._define_adject(adject=second, weight=1)
            del adject._adjects[first]
        self._del_node(first)
        return True
    

class GraphBuidler:
    WEIGHTED_GRAPH = False
    DIRECTED_GRAPH = False

    @classmethod
    def _connect(cls, nodeS: Node, nodeT: Node, directed: bool = False, weight: int = 1) -> None:
        nodeS._define_adject(adject=nodeT, weight=weight)
        if not directed:
            nodeT._define_adject(adject=nodeS, weight=weight)

    @classmethod
    def build(cls, nodes: Dict, directed_graph: bool = False, weighted_graph: bool = False) -> Graph:
        '''Принимая на вход словарь из объектов, проводит связку вершин и добавляет в класс Graph в виде множества из Node. 
        Все задействованные в графе вершины должны быть указаны в JSON в качестве ключей nodes, иначе не будут добавлены.'''
        cls.WEIGHTED_GRAPH = weighted_graph
        cls.DIRECTED_GRAPH = directed_graph
        temp_graph = set()
        for node, adjects in nodes.items():
            for adject_node, weight in adjects.items():
                if not cls.WEIGHTED_GRAPH:
                    weight = 1
                cls._connect(node, adject_node, weight=weight, directed=cls.DIRECTED_GRAPH)
            temp_graph.add(node)
        return Graph(nodes=tuple(temp_graph), directed_graph=cls.DIRECTED_GRAPH, weighted_graph=cls.WEIGHTED_GRAPH)
    

        