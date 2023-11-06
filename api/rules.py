from typing import Dict


class Rules:
    EXPECT = ['nodeS', 'nodeT']
    UNORDINARY = ['shortest_way']
    @classmethod
    def expect(cls, data: Dict):
        for ex in cls.EXPECT:
            if not data.get(ex):
                return (False, ex)
        return (True, 'success')
