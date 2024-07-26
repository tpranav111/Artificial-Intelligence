class Node:
    def __init__(self, name):
        self.name = name
        self.rew = 0
        self.value = 0
        self.isTerminal = False
        self.isChance = False
        self.isDecision = False
        self.edges = []
        self.prob = []
        self.cur_policy = name

    def assign_node_type(self):
        prob_check = 0
        if len(self.edges) == len(self.prob) and len(self.edges) > 0:
            self.isChance = True
        elif len(self.prob) == 1:
            self.isDecision = True
        elif len(self.prob) == 0 and len(self.edges) > 0:
            self.isDecision = True
            self.prob.append(1)
        elif len(self.prob) == 1:
            self.isDecision = True
        elif len(self.edges) == 0:
            self.isTerminal = True