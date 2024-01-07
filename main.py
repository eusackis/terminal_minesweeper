import random

### creating a grid creating function because will use it again maybe
columns = "ABCDEFGHIJ"
rows = range(10)

def create_empty_grid():
  empty_dict = {} # could have made maybe an list of lists, since the keys are pretty much index numbers, but no real reason to change it now
  for i in rows:
    empty_dict[i] = ['O' for j in range(10)]
  return empty_dict
  
original_grid = create_empty_grid()

### self-explanatory print_grid function
def print_grid(grid: dict):
  print("X", [char for char in columns])
  print("----------------------------------------------------")
  for key, value in grid.items():
    print(key, value)
  print("\n")
  

print_grid(original_grid)

### creating mines
mines = random.sample(range(100),13) # The average percentage of mines on the board averages about to 0.12-0.2 %, the percentage increasing as the board gets bigger so probably for 10x10 board 13 would be ok 
# while len(mines) < 13:
  # x = random.randint(1,100)
  # if x not in mines:
  #   mines.append(x)

# checking if everything is on the up-and-up
print(sorted(mines))
print(len(set(mines)))

### placing the mines
for mine in mines:
  row = mine // 10
  idx = mine % 10
  original_grid[row][idx] = 'X'

print_grid(original_grid)

### placing the numbers around the mines and also creating a list of all the numbered fields which need to be uncovered to finish the game
numbers_on_grid = [] # list for all non-zero values on the grid to win the game

for row_num, row_items in original_grid.items():
  for idx in range(len(row_items)):
    # since you can't iterate through a list with invalid grid values (index and key), going to loop through possible 8 cell coordinates and add the only legitimate cells in a list with try .. except
    if row_items[idx] == 'O':
      surrounding_cells = []
      for i, j in [(row_num-1, idx-1), (row_num-1, idx), (row_num-1, idx+1), 
                   (row_num, idx-1),                    (row_num, idx+1), 
                   (row_num+1, idx-1), (row_num+1, idx), (row_num+1, idx+1)]:
        try:
          if j != -1: # so that it doesn't look at the check the [-1] item when the index is 0 
            surrounding_cells.append(original_grid[i][j])
        except (IndexError, KeyError): # IndexError for when idx goes over, KeyError when the key goes outside of 0-9 
          continue
      if surrounding_cells.count('X') == 0:
        row_items[idx] = ' '
      else:
        row_items[idx] = str(surrounding_cells.count('X'))
        numbers_on_grid.append((idx, row_num))
          
print_grid(original_grid)
covered_grid = create_empty_grid()
print_grid(covered_grid)

def uncover_tile():
  # global mistakes
  player_input = input('Enter field coordinates: ').upper()
  tile_data = player_input.split()

  # checking if a valid entry is submitted at all, 
  # the order of conditions matters
  while len(tile_data) != 3 or tile_data[0] not in columns or tile_data[1].isdigit() and int(tile_data[1]) not in rows or tile_data[2] not in ['U', 'F'] or (tile_data[0], int(tile_data[1])) in mistakes:
    print(tile_data)
    if (tile_data[0], int(tile_data[1])) in mistakes: # so that reentering a already detonated mine, does not result in a game over:
      print("Looks like you are trying to step on a detonated mine, one leg per one mine. Company policy.")
    else:
      print("You haven't entered a valid grid coordinate with a valid action")
    player_input = input('Try again: ').upper()
    tile_data = player_input.split()

  char_idx = columns.find(tile_data[0])
  row_key = int(tile_data[1])
  action = tile_data[2]

  checked_zero_tiles = []

  def uncover_safe_tile_remove_num(x, y): #  created this because technically I reuse this sequence twice, the naming sucks, I know
    covered_grid[x][y] = original_grid[x][y]
    if (x, y) in numbers_on_grid:
      numbers_on_grid.remove((x,y))


  def mass_uncover(zero_list: list):
    unchecked_zero_tiles = []
    for item in zero_list:
      x = item[0]
      y = item[1]
      covered_grid[x][y] = original_grid[x][y] # uncover the one you click first
      checked_zero_tiles.append(item)

      for i, j in [(x-1, y-1), (x-1, y), (x-1, y+1), 
                    (x, y-1),               (x, y+1), 
                    (x+1, y-1), (x+1, y), (x+1, y+1)]:
        try:
          if j != -1: # so that it doesn't look at the check the [-1] item when the index is 0
            if original_grid[i][j] == " " and (i, j) not in checked_zero_tiles: # so it remembers all the empty tiles it needs to check and does not check the ones that are
              unchecked_zero_tiles.append((i, j))
            uncover_safe_tile_remove_num(i, j)

        except (IndexError, KeyError): # IndexError for when idx goes over, KeyError when the key goes outside of 0-9 
          continue

    if len(unchecked_zero_tiles) != 0: # if you comment this out the recursion falls under outer for loop - it still works
      mass_uncover(unchecked_zero_tiles)
    

  if original_grid[row_key][char_idx] == 'X' and action == 'U':
    mistakes.append((tile_data[0], row_key)) # changed the char_idx back to tile_data[0], for the sake of consistency, although really weighing the benefits of the letters x numbers aesthetic at this point
    if len(mistakes) == 1:
      print("\nKABLAMO! You are on your last leg. Literally!\n")
    covered_grid[row_key][char_idx] = 'B'
  
  elif original_grid[row_key][char_idx] == ' ':
    zero_cells = [(row_key, char_idx)]
    mass_uncover(zero_cells)
  elif action == 'F':
    covered_grid[row_key][char_idx] = action
  else:
    uncover_safe_tile_remove_num(row_key, char_idx)

  print_grid(covered_grid)

mistakes = []

print('To play enter the tile coordinates with the column + row combo in that order, for example - B 7 U')

while len(mistakes) < 2 and len(numbers_on_grid) != 0:
  # print_grid(original_grid)
  uncover_tile()
  print(f"the amount of mistakes: {mistakes}")
  print_grid(original_grid)

if len(mistakes) == 2:
  print("""
██╗░░██╗░█████╗░██████╗░░█████╗░░█████╗░███╗░░░███╗██╗  ██╗░░░██╗░█████╗░██╗░░░██╗  ░█████╗░██████╗░███████╗
██║░██╔╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗████╗░████║██║  ╚██╗░██╔╝██╔══██╗██║░░░██║  ██╔══██╗██╔══██╗██╔════╝
█████═╝░███████║██████╦╝██║░░██║██║░░██║██╔████╔██║██║  ░╚████╔╝░██║░░██║██║░░░██║  ███████║██████╔╝█████╗░░
██╔═██╗░██╔══██║██╔══██╗██║░░██║██║░░██║██║╚██╔╝██║╚═╝  ░░╚██╔╝░░██║░░██║██║░░░██║  ██╔══██║██╔══██╗██╔══╝░░
██║░╚██╗██║░░██║██████╦╝╚█████╔╝╚█████╔╝██║░╚═╝░██║██╗  ░░░██║░░░╚█████╔╝╚██████╔╝  ██║░░██║██║░░██║███████╗
╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝  ░░░╚═╝░░░░╚════╝░░╚═════╝░  ╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝

██████╗░███████╗░█████╗░██████╗░
██╔══██╗██╔════╝██╔══██╗██╔══██╗
██║░░██║█████╗░░███████║██║░░██║
██║░░██║██╔══╝░░██╔══██║██║░░██║
██████╔╝███████╗██║░░██║██████╔╝
╚═════╝░╚══════╝╚═╝░░╚═╝╚═════╝░""")
  
if len(numbers_on_grid) == 0: 
  print("""
█▄█ ▄▀█ ▄▀█ ▄▀█ ▄▀█ ▄▀█ █▄█ █   █▀▀ █▀█ █▄░█ █▀▀ █▀█ ▄▀█ ▀█▀ █░█ █░░ ▄▀█ ▀█▀ █ █▀█ █▄░█ █▀
░█░ █▀█ █▀█ █▀█ █▀█ █▀█ ░█░ ▄   █▄▄ █▄█ █░▀█ █▄█ █▀▄ █▀█ ░█░ █▄█ █▄▄ █▀█ ░█░ █ █▄█ █░▀█ ▄█""")
  
    