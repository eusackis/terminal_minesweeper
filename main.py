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

for row_num, row_items in original_grid.items():
  for idx in range(len(row_items)):
    # since you can't iterate through a list with invalid grid values (index and key), going to loop through possible 8 cell coordinates and add the only legitimate cells in a list with try .. except
    if row_items[idx] == '_':
      surrounding_cells = []
      for i, j in [(row_num-1, idx-1), (row_num-1, idx), (row_num-1, idx+1), 
                   (row_num, idx-1),                    (row_num, idx+1), 
                   (row_num+1, idx-1), (row_num+1, idx), (row_num+1, idx+1)]:
        try:
          if j != -1: # so that it doesn't look at the check the [-1] item when the index is 0 
            surrounding_cells.append(original_grid[i][j])
        except (IndexError, KeyError): # IndexError for when idx goes over, KeyError when the key goes outside of 0-9 
          continue
      row_items[idx] = str(surrounding_cells.count('X'))
      
          
print_grid(original_grid)

covered_grid = create_empty_grid()

print_grid(covered_grid)


def uncover_tile():
  global mistakes
  player_input = input('Enter field coordinates: ').upper()
  tile_data = player_input.split()

  # checking if a valid entry is submitted at all, 
  # also note-to-self - the order of conditions matters: first if there is the right amount of split variables, then each element (with the second being checked whether it's a digit to begin with before being made into an int, and lastly whether it's been added to 1 mistake list)
  while len(tile_data) != 3 or tile_data[0] not in columns or tile_data[1].isdigit() and int(tile_data[1]) not in rows or tile_data[2] not in ['U', 'F'] or (tile_data[0], int(tile_data[1])) in mistakes:
    print(tile_data)
    if (tile_data[0], int(tile_data[1])) in mistakes:
      print("Looks like you are trying to step on a detonated mine, one leg per one mine. Company policy.")
    else:
      print("You haven't entered a valid grid coordinate with a valid action")
    player_input = input('Try again: ').upper()
    tile_data = player_input.split()

  # so that reentering a already detonated mine, does not result in a game over:

  char_idx = columns.find(tile_data[0])
  row_key = int(tile_data[1])
  action = tile_data[2]

  if original_grid[row_key][char_idx] == 'X' and action == 'U':
    mistakes.append((tile_data[0], row_key)) # changed the char_idx back to tile_data[0], for the sake of consistency, although really weighing the benefits of the letters x numbers aesthetic at this point
    if len(mistakes) == 1:
      print("\nKABLAMO! You are on your last leg. Literally!\n")
    covered_grid[row_key][char_idx] = 'B'
  
  elif original_grid[row_key][char_idx] == '0':
    zero_cells = []
    for i, j in [(row_key-1, char_idx-1), (row_key-1, char_idx), (row_key-1, char_idx+1), 
                  (row_key, char_idx-1),    (row_key, char_idx),  (row_key, char_idx+1), # included row_key, char_idx
                  (row_key+1, char_idx-1), (row_key+1, char_idx), (row_key+1, char_idx+1)]:
      try:
        if j != -1: # so that it doesn't look at the check the [-1] item when the index is 0
          if original_grid[i][j] == "0":
            zero_cells.append((i, j))
          covered_grid[i][j] = original_grid[i][j]

      except (IndexError, KeyError): # IndexError for when idx goes over, KeyError when the key goes outside of 0-9 
        continue
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
  
    