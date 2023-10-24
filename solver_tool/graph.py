import json
from random import sample
from typing import List, Optional, Tuple, Dict


class Node:
    count = 0
    def __init__(self, name = 'X' + str(count)) -> None:
        self.count = Node.count + 1
        Node.count += 1
        self.name = name
        self.__adjects = dict()
        self._reverse_adjects = []

    def _define_adject(self, adject, weight):
        # Добавление данной вершины в список обратного отображения переданной вершины
        adject._reverse_adjects.append(self)
        self.__adjects.update({adject: weight})

    @property
    def adjects(self):
        return self.__adjects 
    
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
    

        