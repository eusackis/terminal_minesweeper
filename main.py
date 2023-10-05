import random

# creating a grid creating functoinm because will use it again maybe
def create_grid():
  empty_dict = {}
  for i in range(10):
    empty_dict[i] = ['_' for j in range(10)]
  return empty_dict
  
original_grid = create_grid()

def print_grid(grid):
  print("X", [char for char in "ABCDEFGHIJ"])
  print("----------------------------------------------------")
  for key, value in grid.items():
    print(key, value)
  print("\n")
  

print_grid(original_grid)
# The average percentage of mines on the board averages about to 0.12-0.2 %, the percentage increasing as the board gets bigger so probably for 10x10 board 13 would be ok

mines = random.sample(range(100),13)
# while len(mines) < 13:
  # x = random.randint(1,100)
  # if x not in mines:
  #   mines.append(x)

print(sorted(mines))
print(len(set(mines)))

for mine in mines:
  row = mine // 10
  idx = mine % 10
  original_grid[row][idx] = 'X'

print_grid(original_grid)

for key, value in original_grid.items():
  for idx in range(len(value)):
    # since you can't iterate through a list with invalid grid values (index and key), going to loop through possible 8 cell coordinates and add the only legitimate cells in a list with try .. except
    if value[idx] == '_':
      surrounding_cells = []
      for i, j in [(key-1, idx-1), (key-1, idx), (key-1, idx+1), 
                   (key, idx-1),                    (key, idx+1), 
                   (key+1, idx-1), (key+1, idx), (key+1, idx+1)]:
        try:
          if j != -1: # so that it doesn't look at the check the [-1] item when the index is 0 
            surrounding_cells.append(original_grid[i][j])
        except (IndexError, KeyError):
          continue
      value[idx] = str(surrounding_cells.count('X'))
      
          
print_grid(original_grid)

covered_grid = create_grid()

print_grid(covered_grid)