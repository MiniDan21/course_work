import pprint 

from solver_tool import GraphBuidler, ShortestWay
from solver_tool.parser import Parser


data, directed, weighted, task = Parser.json_to_obj(open('api/test.json', 'rb').read())
print(data, directed, weighted, task)
graph = GraphBuidler.build(nodes=data, directed_graph=directed, weighted_graph=weighted)

# solver = Components()
# for i in solver.solve(graph):
#     print(i)
# r_n_c = graph.random_node_cuple()
# for nodeS in graph.info():
#     for nodeT in graph.info():
#         print('NodeS and NodeT')
#         pprint.pprint((nodeS, nodeT))
#         print('\/ RESULT \/')
#         print(solver.defind_ways(nodeS, nodeT))

# solver = ArtPoints()

# print(solver.solve(graph))

solver = ShortestWay()
print(solver.solve(graph, graph.nodes["X1"], graph.nodes["X1"]))