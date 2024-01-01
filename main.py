import random

# creating a grid creating functoinm because will use it again maybe

columns = "ABCDEFGHIJ"
rows = range(10)

def create_empty_grid():
  empty_dict = {} # could have made maybe an list of lists, since the keys are pretty much index numbers, but no real reason to change it now
  for i in rows:
    empty_dict[i] = ['_' for j in range(10)]
  return empty_dict
  
original_grid = create_empty_grid()

def print_grid(grid: dict):
  print("X", [char for char in columns])
  print("----------------------------------------------------")
  for key, value in grid.items():
    print(key, value)
  print("\n")
  

print_grid(original_grid)
# The average percentage of mines on the board averages about to 0.12-0.2 %, the percentage increasing as the board gets bigger so probably for 10x10 board 13 would be ok

mines = random.sample(range(100),13) # 
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

covered_grid = create_empty_grid()

print_grid(covered_grid)


def uncover_tile():
  global mistakes
  player_input = input('Enter field coordinates: ').upper()
  tile_data = player_input.split()

  # checking if a valid entry is submitted at all: tile_data should have 3 items, 1st a letter A - J, 2nd an int and 0-9, 3rd either U or F
  while len(tile_data) != 3 or tile_data[0] not in columns or tile_data[1].isdigit() and int(tile_data[1]) not in rows or tile_data[2] not in ['U', 'F']:
    print(tile_data)
    print("You haven't entered a valid grid coordinate with a valid action")
    player_input = input('try again: ').upper()
    tile_data = player_input.split()

  # so that reentering a already detonated mine, does not result in a game over:

  char_idx = columns.find(tile_data[0])
  row_key = int(tile_data[1])
  action = tile_data[2]

  if original_grid[row_key][char_idx] == 'X' and action == 'U':
    mistakes.append((row_key, char_idx))
    if len(mistakes) == 1:
      print(":(\nWhoops! Seems like you made a mistake, I'll let this one slide, but one more and you are out!\n")
    covered_grid[row_key][char_idx] = 'B'
  
  elif original_grid[row_key][char_idx] == '_':
    pass
  elif action == 'F':
    covered_grid[row_key][char_idx] = action
  else:
    covered_grid[row_key][char_idx] = original_grid[row_key][char_idx]

  print_grid(covered_grid)

mistakes = []

print('To play enter the tile coordinates with the column + row combo in that order, for example - B 7 U')

while len(mistakes) < 2:
  uncover_tile()
  print(f"the amount of mistakes: {mistakes}")
  
    