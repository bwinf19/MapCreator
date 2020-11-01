class NpcEditor:
    def __init__(self):
        self.pos = None
        self.npc = None
        self.cnpc = None

    @staticmethod
    def clone(npc):
        return {'i': npc['i'], 'dialog': [x for x in npc['dialog']],
                'pokemon': [{'name': x['name'], 'lvl': x['lvl']} for x in npc['pokemon']]}

    def set_npc(self, pos, npc):
        self.pos = pos
        self.npc = self.clone(npc)
        self.cnpc = self.clone(npc)
