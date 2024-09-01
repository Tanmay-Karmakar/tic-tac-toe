def show_episode(episode):
  for e in episode:
    print(f"{e[0].state}:{e[1]}:{e[2]}",end=' -> ')

  print()

def display_state(state):
    dis = []
    for i in state:
        if i == 0:
            dis.append('#')
        elif i == 1:
            dis.append('O')
        else:
            dis.append('X')

    print("----------------------")
    print(f"{dis[0]} {dis[1]} {dis[2]}")
    print(f"{dis[3]} {dis[4]} {dis[5]}")
    print(f"{dis[6]} {dis[7]} {dis[8]}")
    print("----------------------")