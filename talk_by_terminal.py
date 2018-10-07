import curses
import math
import time

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

#                     Helper functions

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# Curses helper function from http://devcry.heiho.net/html/2016/20160228-curses-practices.html
def getch():
  KEY_TABLE = {'0x1b': 'ESC'}
  '''Returns keystroke as string''' 
  
  key = screen.getch()

  if key == curses.KEY_RESIZE:
    resize_event()

  elif key >= ord(' ') and key <= ord('~'):
    # ascii key
    return chr(key)

  elif key >= 1 and key <= 26:
    # Ctrl-A to Ctrl-Z
    return 'Ctrl-' + ch(ord('@') + key)

  # special key : use a lookup table
  skey = '0x%02x' % key
  if skey in KEY_TABLE:
    return KEY_TABLE[skey]

  # unknown key; just return as a hex string
  return skey

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

screen = curses.initscr()

# Press escape key to exit
q = ''

while q != 'ESC':
  screen.clear()

  # Note that coordinates appear in the order y,x not x,y
  dims = {'x': screen.getmaxyx()[1], 'y': screen.getmaxyx()[0]}

  # Create a divider string to separate the screen
  divider = '~' * dims['x']
  divider_position = int(dims['y']/2)

  screen.addstr(divider_position, 0, divider)
  q = getch()
  screen.refresh()

# Clear screen and exit
screen.clear()
curses.endwin()