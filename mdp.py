# MDP generation
from itertools import product
import os , json
data = 'data2'
if not os.path.exists(f'./{data}'):
  os.mkdir(f'./{data}')

# each state is denoted by a 9-tuple(list) representing 9 boxes on the tic-tac-toe board
# where each entry is 0, 1 or 2 (0:= Empty box, 1:= Box with o and 2: Box with x )
class STATE:
  def __init__(self,state):
    self.state = state
    self.t_status = self.check_termination()
    self.actions = self.get_possible_actions()
    self.num_actions = len(self.actions)


  def a0(self,symbol):
    state = list(self.state)
    state[0] = symbol
    return tuple(state)

  def a1(self,symbol):
    state = list(self.state)
    state[1] = symbol
    return tuple(state)

  def a2(self,symbol):
    state = list(self.state)
    state[2] = symbol
    return tuple(state)

  def a3(self,symbol):
    state = list(self.state)
    state[3] = symbol
    return tuple(state)

  def a4(self,symbol):
    state = list(self.state)
    state[4] = symbol
    return tuple(state)

  def a5(self,symbol):
    state = list(self.state)
    state[5] = symbol
    return tuple(state)

  def a6(self,symbol):
    state = list(self.state)
    state[6] = symbol
    return tuple(state)

  def a7(self,symbol):
    state = list(self.state)
    state[7] = symbol
    return tuple(state)

  def a8(self,symbol):
    state = list(self.state)
    state[8] = symbol
    return tuple(state)

  def take_action(self,which,symbol):
    match which:
      case 0:
        s = self.a0(symbol)
      case 1:
        s = self.a1(symbol)
      case 2:
        s = self.a2(symbol)
      case 3:
        s = self.a3(symbol)
      case 4:
        s = self.a4(symbol)
      case 5:
        s = self.a5(symbol)
      case 6:
        s = self.a6(symbol)
      case 7:
        s = self.a7(symbol)
      case 8:
        s = self.a8(symbol)
    return s


  def get_possible_actions(self):
    possible_actions = []
    for pos in range(9):
      if self.state[pos] == 0:
        possible_actions.append(pos)
    return possible_actions

  def check_termination(self):
    s = self.state

    if s[0] == s[1] == s[2] != 0 or s[3] == s[4] == s[5]!=0 or s[6] == s[7] == s[8]!=0:
      # print('hello')  # Rows
      return True
    elif s[0] == s[3] == s[6]!=0 or s[7] == s[4] == s[1]!=0 or s[8] == s[5] == s[2]!=0: # Columns
      return True
    elif s[0] == s[4] == s[8]!=0 or s[6] == s[4] == s[2]!=0:                         # Diagonal
      return True
    elif self.state.count(0) == 0:
      return True
    return False



  def check_winning_status(self,symbol):    # returns 1 if agent wins -1 if looses 0 if draw and 2 otherwise
    s = self.state
    if self.t_status == False:
      return 2
    if s[0] == s[1] == s[2] == symbol or s[3] == s[4] == s[5] == symbol or s[6] == s[7] == s[8] == symbol:   # Rows
      return 1
    elif s[0] == s[3] == s[6] == symbol or s[7] == s[4] == s[1] == symbol or s[8] == s[5] == s[2] == symbol: # Columns
      return 1
    elif s[0] == s[4] == s[8] == symbol or s[6] == s[4] == s[2] == symbol:                         # Diagonal
      return 1
    elif self.check_loosing_status(symbol):
      return -1
    return 0

  def check_loosing_status(self,symbol):
    s = self.state
    r = self.rev(symbol)
    if s[0] == s[1] == s[2] == r or s[3] == s[4] == s[5] == r or s[6] == s[7] == s[8] == r:   # Rows
      return True
    elif s[0] == s[3] == s[6] == r or s[7] == s[4] == s[1] == r or s[8] == s[5] == s[2] == r: # Columns
      return True
    elif s[0] == s[4] == s[8] == r or s[6] == s[4] == s[2] == r:                         # Diagonal
      return True
    else:
      return False

  def rev(self, num):
    if num == 1:
      return 2
    else:
      return 1

#=================================================================


class MDP:
  def __init__(self):
    self.current_state = STATE((0,0,0,0,0,0,0,0,0))
    self.t_status = self.current_state.t_status
    self.states = self.generate_states()

  def init_mdp(self):
    self.current_state = STATE((0,0,0,0,0,0,0,0,0))
    self.t_status = self.current_state.t_status


  def get_possible_actions(self):
    return 1

  def generate_states(self):
    a = [0,1,2]
    state_tuples = product(a,repeat=9)
    state_tuples = list(state_tuples)
    states = []
    for s in state_tuples:
      state = STATE(s)
      states.append(state)
    return states

  def update_state(self, state):
    self.current_state = state
    self.t_status = self.current_state.t_status
    return
# =========================================
