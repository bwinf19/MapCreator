class NpcEditor:
    def __init__(self):
        self.pos = None
        self.npc = None
        self.cnpc = None

    def set_npc(self, pos, npc):
        self.pos = pos
        self.npc = {'i': npc['i'], 'dialog': [x for x in npc['dialog']]}
        self.cnpc = {'i': npc['i'], 'dialog': [x for x in npc['dialog']]}
