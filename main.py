import random

grid = {}

for i in range(10):
  grid[i] = ['_' for j in range(10)]

def print_grid():
  print("X", [char for char in "ABCDEFGHIJ"])
  for key, value in grid.items():
    print(key, value)

print_grid()
# The average percentage of mines on the board averages about to 0.12-0.2 %, the percentage increasing as the board gets bigger so probably for 10x10 board 13 would be ok
# Note: For future reference
mines = random.sample(range(1,101),13)
# while len(mines) < 13:
  # x = random.randint(1,100)
  # if x not in mines:
  #   mines.append(x)

print(mines)
print(set(mines))
# for mine in mines:
  
