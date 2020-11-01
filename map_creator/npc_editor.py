class NpcEditor:
    def __init__(self):
        self.pos = None
        self.npc = None
        self.cnpc = None

    def set_npc(self, pos, npc):
        self.pos = pos
        self.npc = npc
        self.cnpc = npc.copy()
