class Node:

    def __init__(self, actions):
        
        self.actions = actions
        self.regret_sum = dict()
        self.strategy = dict()
        self.strategy_sum = dict()
        self.value = dict()
        self.final_strategy = dict()
    
