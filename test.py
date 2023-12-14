import pprint 

from solver_tool import GraphBuidler, ShortestWay, Planarity
from solver_tool.parser import Parser


data, directed, weighted, task = Parser.json_to_obj(open('api/test.json', 'rb').read())
graph = GraphBuidler.build(nodes=data, directed_graph=directed, weighted_graph=weighted)
node1, node2 = graph.random_node_cuple()

solver = ShortestWay()
# print(solver.solve(graph, graph.nodes["X1"], graph.nodes["X1"]))


# print(graph.info())
print(f"{node1=}")
print(f"{node2=}")
print(solver.solve(graph, node1, node2))