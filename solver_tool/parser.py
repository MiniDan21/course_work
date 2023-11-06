# Переводит JSON в словарь Dict с объектами из solver
import json
from typing import Dict, Optional, List, Generator

from .graph import Node, Graph


class NodeEncoder(json.JSONEncoder):
    def default(self, o: Node):
        return o.name

class Parser:
    @staticmethod
    def json_to_obj(json_data: Optional[bytes| None]) -> (bool, bool, Optional[Dict | None], Dict):
        '''Парсит словарь из строк в словарь из объектов'''
        if type(json_data) is bytes:
            json_data = json.loads(json_data)
        obj_data = dict()
        created = dict()
        directed = bool(json_data.get('directed'))
        weighted = bool(json_data.get('weighted'))
        # словарь с ключом nodes и значением словаря с вершинами
        if json_data.get('nodes'):
            for node, adjects in json_data.get('nodes').items():
                if not node in created.keys():
                    node = Node(name=node)
                    created.update({node.name: node})
                else:
                    node = created[node]
                obj_data.update({node: dict()})
                try:
                    for adject_node, weight in adjects.items() or {}:
                        if not adject_node in created.keys():
                            adject_node = Node(name=adject_node)
                            created.update({adject_node.name: adject_node})
                        else:
                            adject_node = created[adject_node]
                        obj_data[node].update({adject_node: weight} or {})        
                except AttributeError:
                    pass
        return obj_data, directed, weighted, json_data.get('task')
    

    @staticmethod
    def obj_to_json(obj) -> bytes:
        res = list(obj)
        # if isinstance(obj, Generator):
        #     res = list(obj)
        return json.dumps(res, cls=NodeEncoder)
