import random
import game_strings
import string

print(game_strings.intro_text,"\n-----------------------------------------------------------------------------")
print(game_strings.description_text)

column_count = None
row_count = None

while row_count not in range(8,21):
    row_count = input("Enter a row count: ")
    if row_count == "":
        row_count = 8
    else:
        row_count = int(row_count)


while column_count not in range(8,27):
    column_count = input("Enter a column count: ")
    if column_count == "":
        column_count = 8
    else:
        column_count = int(column_count)


columns = string.ascii_uppercase[:column_count]
rows = range(row_count)

### creating a grid creating function because will use it again maybe
def create_empty_grid(rows, columns):
    empty_dict = {} # could have made maybe an list of lists, since the keys are pretty much index numbers, but no real reason to change it now
    for i in range(rows):
        empty_dict[i] = ['O' for j in range(columns)]
    return empty_dict
  
original_grid = create_empty_grid(row_count, column_count)

### self-explanatory print_grid function
def print_grid(grid: dict):
    
    print("XX", [char for char in columns])
    hyphen_line = "-----"
    hyphen_line += hyphen_line * column_count # have a separating line of hyphens that more or less adapts to the amount of columns
    print(hyphen_line)
    for key, value in grid.items():
        if key < 10:
            print("0" + str(key), value)
        else:
            print(key, value)
    print("\n")


### placing the numbers around the mines and also creating a list of all the numbered fields which need to be uncovered to finish the game
### creating mines
tile_count = row_count * column_count
mine_count = 9
if tile_count > 64:
    mine_count += (tile_count - 64) * 0.21
    mine_count = int(mine_count)

mines = random.sample(range(tile_count),mine_count) 
### placing the mines
for mine in mines:
    row = mine // column_count
    idx = mine % column_count

    original_grid[row][idx] = 'X'

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
                except (IndexError, KeyError): # IndexError for when idx goes over, KeyError when the key goes outside of the key range 
                    continue
            if surrounding_cells.count('X') == 0:
                row_items[idx] = ' '
            else:
                row_items[idx] = str(surrounding_cells.count('X'))
                numbers_on_grid.append((idx, row_num)) # adding the numbered tile to a list
 
# print_grid(original_grid)
covered_grid = create_empty_grid(row_count, column_count)
# print_grid(covered_grid)

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
print_grid(covered_grid)
while len(mistakes) < 2 and len(numbers_on_grid) != 0:
    # print_grid(original_grid)
    uncover_tile()
    print(f"the amount of mistakes: {len(mistakes)}")
    # print_grid(original_grid)

if len(mistakes) == 2:
    print(game_strings.losing_text)
  
if len(numbers_on_grid) == 0: 
    print(game_strings.winning_text)
  
    