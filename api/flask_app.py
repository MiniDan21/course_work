from flask import Flask, request, render_template

from solver_tool import GraphBuidler, SolverBuidler
from .parser import Parser
from .rules import Rules


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    nodes, directed, weighted, task = Parser.json_to_obj(request.json)
    graph = GraphBuidler.build(nodes=nodes, directed_graph=directed, weighted_graph=weighted)
    solver = SolverBuidler.build(task['type'])
    extra = dict()
    if not (check := Rules.expect(task))[0] and task['type'] in Rules.UNORDINARY:
        return {'Expected': check[1]}
    if task['type'] in Rules.UNORDINARY:
        del task['type']
        extra = task
    return Parser.obj_to_json(solver.solve(graph, **extra))


app.run()