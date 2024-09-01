import random, json, os
from mdp import STATE
class AGENT:
  def __init__(self, save_file, count_save_file, symbol, mdp, ep=0.1):
    self.count_save_file = count_save_file
    self.mdp = mdp
    self.save_file = save_file
    self.symbol = symbol
    self.policy = None
    self.state_action_update_count = None
    self.ep = ep

  def get_state_visit_count(self):
    if not os.path.exists(self.count_save_file):
      return -1
    with open(self.count_save_file,'r') as c:
      j = json.load(c)
      d = {tuple(int(x) for x in k.strip('()').split(',')): {int(kk):vv for kk,vv in v.items()} for k,v in j.items()}
      self.state_action_update_count = d
      return


  def save_state_visit_count(self):
    state_action_update_count = self.state_action_update_count
    f = open(self.count_save_file, 'w')
    json.dump({str(k):v for k,v in state_action_update_count.items()},f)
    f.close()
    return



  def get_policy(self):
    if not os.path.exists(self.save_file):
      return -1
    with open(self.save_file,'r') as p:
      j = json.load(p)
      # print(j)
      d = {tuple(int(x) for x in k.strip('()').split(',')): {int(kk):vv for kk,vv in v.items()} for k,v in j.items()}
      self.policy = d
      return d

  def save_updated_policy(self):
    print("Saving Policy")
    policy = self.policy
    p = open(self.save_file,'w')
    json.dump({str(k):v for k,v in policy.items()},p)
    p.close()

  def init_policy_state_action_count(self):
    if os.path.exists(self.save_file):
      return -1
    p = open(self.save_file,'w')
    c = open(self.count_save_file,'w')
    policy = {}
    state_action_update_count = {}

    print(f"total states = {len(self.mdp.states)}")
    for state in self.mdp.states:
      if not state.t_status:
        actions = state.actions
        num_actions = state.num_actions
        prob = 0      # 1/num_actions
        policy[state.state] = {}
        state_action_update_count[state.state] = {}
        for a in actions:
          policy[state.state][a] = prob
          state_action_update_count[state.state][a] = prob
    self.policy = policy
    print(f"Total policy lenght = {len(list(self.policy.keys()))}")
    self.state_action_update_count = state_action_update_count


    # print(policy)
    json.dump({str(k):v for k,v in policy.items()},p)
    p.close()
    json.dump({str(k):v for k,v in state_action_update_count.items()},c)
    c.close()
    return

  def take_action(self):
    policy = self.policy
    state = self.mdp.current_state
    if state.t_status:
      print("problem - game is finished")
      return -1
    actions = policy[state.state]

    def weighted_random_by_dct(dct,ep):
      greedy_action = max(zip(actions.values(), actions.keys()))[1]
      rest_actions = list(actions.keys())
      rest_actions.remove(greedy_action)
      if len(rest_actions) == 0:
        return greedy_action
      r = random.random()
      if r>=0.2:
        return greedy_action
      else:
        return random.choice(rest_actions)

    action = weighted_random_by_dct(actions,self.ep)
    new_state = STATE(state.take_action(action, self.symbol))
    self.mdp.update_state(new_state)
    return action
  


  #===================================================

class M_AGENT(AGENT):
    def __init__(self, save_file, count_save_file, symbol, mdp, ep=0.1, discount=1):
        super().__init__(save_file, count_save_file, symbol, mdp, ep=0.1)
        self.discount = discount



    def update_policy(self, episode):  # episode is a list of tuples of the form [(state, action, reward), (next_state, next_action, next_reward)] last tuple will be (final_state,0,0)
        G = 0
        for i in range(len(episode)-1,-1,-1):
            state = episode[i][0]
            action = episode[i][1]
            reward = episode[i][2]
            G = self.discount*G + reward
            # print(self.policy)
            # print(self.policy[state.state])
            # print(self.state_action_update_count)
            self.policy[state.state][action] = (1/(self.state_action_update_count[state.state][action]+1))*(self.state_action_update_count[state.state][action]*self.policy[state.state][action] + G)
            self.state_action_update_count[state.state][action] += 1


# Code cells for your implementation
class Q_AGENT(AGENT):
    def __init__(self, save_file, count_save_file, symbol, mdp, ep=0.1, discount=1, alpha = 0.2):
        super().__init__(save_file, count_save_file, symbol, mdp, ep=0.1)
        self.discount = discount
        self.alpha = alpha



    def update_policy(self, episode):
        for i in range(len(episode)):
            state = episode[i][0]
            action = episode[i][1]
            reward = episode[i][2]
            if i == len(episode) - 1:
                next_greedy_action_value = 0
            else:
                actions = self.policy[episode[i+1][0].state]
                greedy_action = max(zip(actions.values(), actions.keys()))[1]
                next_greedy_action_value = actions[greedy_action]


            self.policy[state.state][action] += self.alpha*(reward + (self.discount*next_greedy_action_value) - self.policy[state.state][action])


