from .kuhn import KuhnPoker
from .nodes import Node
import random

class CFR_agent:

    def __init__(self, iterations, plot_strategy_sum):

        self.game = KuhnPoker()
        self.iterations = iterations
        self.plot_strategy_sum = plot_strategy_sum
        self.infostate_map = dict()
        self.cards = []

    def train(self):

        for _ in range(self.iterations):
        
            self.cards = random.sample(self.game.cards, 2)
            
            self.CFR("", 1, 1)

    def CFR(self, history, pi_i, pi_i_c):

        if self.game.isGameFinished(history):
            
            return self.game.getPayouts(history, self.cards)
        
        player_to_act = self.game.getPlayerToAct

        infostate = str(player_to_act) + self.cards[player_to_act] + history
        # example, player 1 with a king to act after checking and player 2 betting:
        # 02pb

        if infostate not in self.infostate_map.keys:

            self.infostate_map[infostate] = Node()


        actions = self.game.getActions()


        regret_sum_sum = 0
        #strategy normalization constant

        #Calculate strategy normalization constant
        for action in actions:

            #Calculate the normalization constant 
            #sum of R+(I,a)
            
            R_I_a = self.infostate_map[infostate].regret_sum[action]

            regret_sum_sum += max(R_I_a, 0)
             
        if regret_sum_sum > 0:

            #Calculate probability of taking action a
            for action in actions:
                
                #calculate sig(I,a):
                R_I_a = self.infostate_map[infostate].regret_sum[action]

                R_plus_I_a = max(R_I_a, 0)

                self.infostate_map[infostate].strategy[action] = R_plus_I_a / regret_sum_sum

        else:

            for action in actions:

                self.infostate_map[infostate].strategy[action] = 1 / len(actions)

        #calculate node value: essentially current expected value with current strategy
        #v_sig_I
        node_expected_value = 0

        for action in self.game.getActions():
            
            strategy_a = self.infostate_map[infostate].strategy(action)

            if player_to_act == 0: 

                value_a = self.CFR(history + action, pi_i * strategy_a, pi_i_c)

            else:

                value_a = self.CFR(history + action, pi_i, pi_i_c * strategy_a)


            self.infostate_map[infostate].value[action] = value_a

            node_expected_value += strategy_a * value_a 

        #now reassign the regrets
        for action in self.game.getActions():

            #compare v(I,a) against v_sig_i

            value_a = self.infostate_map[infostate].value[action]
            strategy_a = self.infostate_map[infostate].strategy[action]


            #r(I,a) = v(I,a) - v_sig_i
            regret_a = value_a - node_expected_value

            regret_a = max(regret_a, 0)

            #if v(I,a) > v_sig_i, we have positive regret and we regret not chosing a more often

            #update cumulative regret (regretsum)
            #R(a) = R(a) + (pi_i_c * r(I,a))

            pi_c = pi_i_c if player_to_act == 0 else pi_i

            self.infostate_map[infostate].regret[action] += pi_c * regret_a

            #update strategy sum
            #sig(a) = sig(a) + (pi_i * sig(a))

            pi = pi_i if player_to_act == 0 else pi_i_c

            self.infostate_map[infostate].strategy_sum[action] += strategy_a * pi

        return node_expected_value

    def calculate_final_strategy(self):

        for infostate in self.infostate_map.keys:
            
            actions = self.infostate_map[infostate].actions

            #normalization constnat for final strategies
            final_strategy_sum = 0

            for action in actions:

                final_strategy_sum += self.infostate_map[infostate].strategy_sum[action] 

            if final_strategy_sum > 0:

                for action in actions:

                    strategy_sum_a = self.infostate_map[infostate].strategy_sum[action] 

                    self.infostate_map[infostate].final_strategy[action] = strategy_sum_a / final_strategy_sum
            
            else:

                for action in actions:

                    self.infostate_map[infostate].final_strategy[action] = 1 / len(actions)

        
                    