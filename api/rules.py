from typing import Dict


class Rules:
    COMPONENTS = 'components'
    ART_POINTS = 'art_points'
    PLANARITY = 'planarity'
    SHORTEST_WAY = 'shortest_way'

    EXPECT = ['nodeS', 'nodeT']
    UNORDINARY = [SHORTEST_WAY]
    @classmethod
    def expect(cls, data: Dict):
        for ex in cls.EXPECT:
            if not data.get(ex):
                return (False, ex)
        return (True, 'success')
