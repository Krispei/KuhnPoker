import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from leduc.leduc import leduc

#Compute the expected utilities of each players strategies
def test_payouts():

    agent = leduc()

    # Histories (given player 1 wins):
    # Round 1 / 2:
    # pp - 1
    # prf 
    # prc
    # prrf
    # prrc
    # rf
    # rc
    # rrf
    # rrc
    
    cards = [2,1,0] # P1 has king, p2 has queen, community board is jack, p1 will always win
    history_map = {'pp:pp': 1,
                   'prc:pp': 2,
                   'rc:pp': 2, 
                   'pp:rc': 3,
                   'rrc:pp': 3,
                   'prrc:pp': 3,
                   'rc:rc': 4,
                   'prc:rc': 4,
                   'rc:prc': 4,
                   'prc:prc': 4,
                   'pp:rrc': 5,
                   'pp:prrc': 5,
                   'rrc:rrc': 7,
                   'rrc:prrc': 7,
                   'prrc:rrc': 7,
                   'prrc:prrc': 7,     
                   }
    for history in history_map.keys:
        
        assert agent.payout(history, cards) == history_map[history]

