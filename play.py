import os, sys
from agent import *
from agent import M_AGENT, Q_AGENT
from generate_episode import *
from mdp import MDP

save_dir = 'data2'
if not os.path.exists(save_dir):
    os.mkdir(save_dir)

# Create the MDP
mdp = MDP()

# Load/Initialize the agents
M_player1 = M_AGENT(f'./{save_dir}/pol1', f'./{save_dir}/count1',1,mdp)
M_player1.init_policy_state_action_count()
M_player1.get_policy()
M_player1.get_state_visit_count()
M_player2 = M_AGENT(f'./{save_dir}/pol2',f'./{save_dir}/count2',2,mdp)
M_player2.init_policy_state_action_count()
M_player2.get_policy()
M_player2.get_state_visit_count()

Q_player1 = Q_AGENT(f'./{save_dir}/qpol1', f'./{save_dir}/count1',1,mdp)
Q_player1.init_policy_state_action_count()
Q_player1.get_policy()
Q_player1.get_state_visit_count()
Q_player2 = Q_AGENT(f'./{save_dir}/qpol2', f'./{save_dir}/count2',2,mdp)
Q_player2.init_policy_state_action_count()
Q_player2.get_policy()
Q_player2.get_state_visit_count()

if sys.argv[1] != 'train':
    # Learn while playing against Human
    play_against_Tanmay(M_player1 , mdp)
else:
    # Learn by playing gainst other agent
    play(M_player1, Q_player2, mdp, epoch= 100000)  # Make sure that they have dirrerent symbols


