from .graph import Node, GraphBuidler, Graph
from .components import Components
from .art_points import ArtPoints
from .shortest_way import ShortestWay
from api.rules import Rules


class SolverBuidler:
    @staticmethod
    def build(type: str):
        match type:
            case Rules.COMPONENTS:
                return Components()
            case Rules.ART_POINTS:
                return ArtPoints()
            case Rules.PLANARITY:
                return
            case Rules.SHORTEST_WAY:
                return ShortestWay()
