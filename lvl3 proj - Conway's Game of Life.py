from tkinter import *
from tkinter import ttk
import math

GRID_SIZE = 30  # Tile amount on x and y axis (recommended 14)
GRID_SIZE_MAX = GRID_SIZE * GRID_SIZE  # Just to save on line length
auto = False #  Used for automation functions

# Basics
root = Tk()
root.title("Conway's Game of Life Demo")
grid = Frame(root)


class Tile:
    def __init__(self, num):
        self.num = num  # Main identifier of tiles
        # Using color as an indicator of the status of a tile saves on lines and a status variable
        # and also saves any possible issue getting a hypothetical status variable to match.
        self.color = 'white'
        self.neighbouring = []  # Used to keep track of the amount of live tiles are neighbouring
        self.tile_text = StringVar()
        # Setting tile_text to those spaces creates spacing so height and width match
        self.tile_text.set("     ")  # Varied on different computers (test computer ran linux)
        # Tiles are buttons tkinter-wise. 
        # Pretty basic. The main stuff is in the command/function, click
        self.button = Button(grid, textvariable=self.tile_text,
                             bg=self.color, activebackground='gray',
                             command=self.click)
         # Grids the button. Done on seperate line to prevent error in changing properties of the button.
        self.button.grid(row=num % GRID_SIZE, column=math.floor(num/GRID_SIZE),
                         columnspan=1, sticky="NESW")

    def click(self):
        if self.color == 'white':  # Inverts color/status
            self.color = 'black'
        else:
            self.color = 'white'
        self.button.configure(bg=self.color)  # Changes the button's visuals on screen
        neighbours = [  # Neighbour coord combinations
            [self.num+GRID_SIZE-1, -1, +1],   # 0 Right-Up
            [self.num+GRID_SIZE+1, +1, +1],   # 1 Right-Down
            [self.num-GRID_SIZE-1, -1, -1],   # 2 Left-Up
            [self.num-GRID_SIZE+1, +1, -1],   # 3 Left-Down
            [self.num-GRID_SIZE, 0, -1],      # 4 Left
            [self.num+GRID_SIZE, 0, +1],      # 5 Right
            [self.num-1, -1, 0],              # 6 Up
            [self.num+1, +1, 0]               # 7 Down
        ]
        for i in range(len(neighbours)):
            # Stops out of list error when far right column is tested
            if(neighbours[i][0]) >= 0 and (neighbours[i][0]) < GRID_SIZE_MAX:
                # This line checks the neighbour coord getting trialed.
                if((tile[neighbours[i][0]].num % GRID_SIZE) == ((self.num % GRID_SIZE)+neighbours[i][1]))and((math.floor(tile[neighbours[i][0]].num/GRID_SIZE)) == ((math.floor(self.num/GRID_SIZE))+neighbours[i][2])):
                    # Since this is just taking itself out or putting itself into neighbouring
                    # tiles' neighbouring list it's just a .remove or .append
                    if self.num not in tile[neighbours[i][0]].neighbouring:
                        tile[neighbours[i][0]].neighbouring.append(self.num)
                    else:
                        tile[neighbours[i][0]].neighbouring.remove(self.num)


# Resets the grid by going through every cell.
# Could be improved by just testing neighbouring and live cells
# because every other cell has no chance of life.
def grid_reset():
  for i in range(GRID_SIZE_MAX):
    tile[i].color = 'white'
    tile[i].button.configure(bg=tile[i].color)
    tile[i].neighbouring = []


# step function (named after step event) puts the grid into it's next generation/iteration
def step():
  live_tiles = []  # explained below
  for i in range(GRID_SIZE_MAX):  # tests every tile in grid
    # conway's rules for a tile being alive in the next iteration.
    if(tile[i].color == 'black' and len(tile[i].neighbouring) == 2) or (len(tile[i].neighbouring) == 3):
      live_tiles.append(tile[i].num)  # adds tile to be alive next iteration
    tile[i].neighbouring = []
  print(live_tiles)
  for i in range(GRID_SIZE_MAX):  # Putting the game into it's next iteration.
    if i in live_tiles:  # Living ones
      print("{} PASS".format(i))
      tile[i].color = 'black'
      tile[i].button.configure(bg=tile[i].color)
    else:
      tile[i].color = 'white'  # Dead ones
      tile[i].button.configure(bg=tile[i].color)
  print(live_tiles)
  for j in range(len(live_tiles)):
    print(j)
    neighbours = [  # List of adaptable coords of neighbouring tiles.
      [tile[live_tiles[j]].num+GRID_SIZE-1, -1, +1],  # 0 Right-Up
      [tile[live_tiles[j]].num+GRID_SIZE+1, +1, +1],  # 1 Right-Down
      [tile[live_tiles[j]].num-GRID_SIZE-1, -1, -1],  # 2 Left-Up
      [tile[live_tiles[j]].num-GRID_SIZE+1, +1, -1],  # 3 Left-Down
      [tile[live_tiles[j]].num-GRID_SIZE, 0, -1],     # 4 Left
      [tile[live_tiles[j]].num+GRID_SIZE, 0, +1],     # 5 Right
      [tile[live_tiles[j]].num-1, -1, 0],             # 6 Up
      [tile[live_tiles[j]].num+1, +1, 0]              # 7 Down
    ]
    for i in range(len(neighbours)):  # Should be 8 because there's only 8 neighbours
      if(neighbours[i][0]) >= 0 and (neighbours[i][0]) < GRID_SIZE_MAX:  # Stops out of list error when far right column is tested
        if((tile[neighbours[i][0]].num % GRID_SIZE) == ((tile[live_tiles[j]].num % GRID_SIZE) + neighbours[i][1])) and ((math.floor(tile[neighbours[i][0]].num / GRID_SIZE)) == ((math.floor(tile[live_tiles[j]].num / GRID_SIZE)) + neighbours[i][2])):
          if tile[live_tiles[j]].num not in tile[neighbours[i][0]].neighbouring:
            tile[neighbours[i][0]].neighbouring.append(tile[live_tiles[j]].num)
          else:
            tile[neighbours[i][0]].neighbouring.remove(tile[live_tiles[j]].num)


# This is to change auto variable. It's a boolean so it's a pretty
# basic line with two possibilities.
def automate():
  global auto
  auto = not auto
  automation()  # Starts the loop 

# Automation is done like this so when the button is pressed it's
# toggling a variable, and not directly controlling the next step
# and causing possible problems, plus it's just nicer.
def automation():
  global auto
  if auto: # Breaks the loop if auto is set to False
    step() # Goes through another step/iteration of the grid
    root.after(500, automation) # Stays in the loop

# tile is used to store all the objects of the Tile class. Better
# than creating possibly hundreds of variables, depending on grid size.
tile = []
# live_tiles is used to store all tiles that should be alive in the
# next step. It's stored for later to stop possible reactions that
# could be caused by newly placed live tiles in the middle of a step
live_tiles = []



# Menu -----------------------------------------------------------------------------------------------------------------------------------------
menu = Frame(root)
ttk.Button(menu, text="Start Game", command=lambda : step()).pack(side=LEFT)                    # Start Game button
ttk.Button(menu, text="Reset Grid", command=lambda : grid_reset()).pack(side=LEFT)              # Reset Grid button
ttk.Button(menu, text="Exit Game", command=lambda : root.destroy()).pack(side=LEFT, pady=10)    # Exit Game button
ttk.Button(menu, text="Automate", command=lambda : automate()).pack(side=LEFT)                  # Automate button

# Creating grid --------------------------------------------------------------------------------------------------------------------------------
for i in range(GRID_SIZE_MAX):
  tile.append(Tile(i))

# Packing --------------------------------------------------------------------------------------------------------------------------------------
# Seperated the menu and grid frame because it would be safer to
# grid all the tiles in the grid, to ensure they're all correctly
# positioned.
# Menu just needed to be packed together, placement of the buttons
# should automatically be perfectly as intended, but if not, the
# application doesn't implode.
menu.pack()
grid.pack()

# Creating window ------------------------------------------------------------------------------------------------------------------------------
# The application should be resized to perfectly fit all the widgets
# with no margins to the left, right, and bottom which is intended.
# The only margin/padding should be up and down the buttons, pushing
# the top of the window up and grid below by 10 pixels
root.resizable(False,False)
# Final line to start application
root.mainloop()

# Please give me excellence
