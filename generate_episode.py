from mdp import STATE
from utils import *
def generate_episode(player1,player2,mdp): # episode is a list of tuples of the form [(state, action, reward), (next_state, next_action, next_reward)] last tuple will be (final_state,0,0)
  episode1 = []
  episode2 = []
  check_p2 = 0  
  while True:
    state = mdp.current_state
    
    action1 = player1.take_action()
    next_state = mdp.current_state
    
    status1 = next_state.check_winning_status(player1.symbol)
    if status1 == 1:
      print("1st player wins")
      # wp1 +=1
      episode1.append((state, action1, 10))
      if check_p2 == 1:
        episode2.append((prev_state, action2, -10))
      break
    elif status1 == 0:
      episode1.append((state, action1, 0))
      print("It's a draw")
      # dr +=1
      if check_p2 == 1:
        episode2.append((prev_state, action2, 0))
        
        break
      break
    elif status1 == 2:
      if check_p2 == 1:
        episode2.append((prev_state, action2, -1))

    prev_state = mdp.current_state
    action2 = player2.take_action()
    new_state = mdp.current_state
    
    check_p2 = 1
    status2 = new_state.check_winning_status(player2.symbol)
    if status2 == 1:
      print("2nd player wins")
      # wp2 += 1
      episode1.append((state , action1, -10))
      episode2.append((prev_state, action2, 10))
      break
    elif status2 == 2:
      episode1.append((state, action1, -1))
    elif status2 == 0:
      print("It's a draw")
      # dr +=1
      episode1.append((state, action1, 0))
      episode2.append((prev_state, action2, 0))
      break


  check_p2 = 0
  mdp.init_mdp()

  
  return episode1 , episode2

def play(player1,player2,mdp,epoch):
  for i in range(epoch):
    print(f"epoch = {i}")
    episode1, episode2 = generate_episode(player1, player2, mdp)
    show_episode(episode1)
    show_episode(episode2)

    player1.update_policy(episode1)
    player2.update_policy(episode2)

  player1.save_updated_policy()
  player2.save_updated_policy()
  player1.save_state_visit_count()
  player2.save_state_visit_count()




def generate_episode_against_Tanmay(player , mdp):
  episode = []

  t_symbol = mdp.current_state.rev(player.symbol)
  if t_symbol == 2:
    print(f"Your symbol is 2:X")
  else:
    print("Your symbol is 1:O")
  display_state(mdp.current_state.state)
  print("0 1 2\n3 4 5\n6 7 8")

  first_who = input("Who will take the first move? Write Tanmay or Computer : ")
  
  if first_who.lower() == 'tanmay':
      t_action = int(input("What is your move? 0 to 8 : "))
      new_state = mdp.current_state.take_action(t_action,t_symbol)
      mdp.current_state = STATE(new_state)
      mdp.t_status = mdp.current_state.t_status
      display_state(mdp.current_state.state)


  while True:
    
    state = mdp.current_state
    action = player.take_action()
    next_state = mdp.current_state
    
    display_state(next_state.state)
    
    status = next_state.check_winning_status(player.symbol)
    if status == 1:
      episode.append((state, action, 10))
      print('game is finished ! You lose')
      break
    elif status == 0:
      episode.append((state, action, 0))
      print('game is finished ! Draw ')
      break
    print('Your Turn')
    t_action = int(input("What is your move? 0 to 8 : "))
    while t_action not in mdp.current_state.actions:
      t_action = int(input("Take a valid move !!\n"))

    new_state = mdp.current_state.take_action(t_action,t_symbol)
    display_state(new_state)
    new_state = STATE(new_state)
    mdp.current_state = new_state
    mdp.t_status = mdp.current_state.t_status
    status2 = new_state.check_winning_status(new_state.rev(player.symbol))
    if status2 == 1:
      episode.append((state , action, -10))
      print("Game is finished ! You win" )
      break
    elif status2 == 0:
      episode.append((state, action, 0))
      print('Game is finished ! Draw')
      break

    elif status2 == 2:
      episode.append((state, action, -1))
    
  return episode
    

def play_against_Tanmay(player, mdp):
  mdp.init_mdp()
  episode = generate_episode_against_Tanmay(player,mdp)
  show_episode(episode)
  player.update_policy(episode)

  player.save_updated_policy()
  player.save_updated_policy()
  player.save_state_visit_count()
  player.save_state_visit_count()
