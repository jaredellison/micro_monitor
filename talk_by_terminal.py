#! /usr/bin/python
'''
    File name: talk_by_terminal.py
    Author: Jared Ellison
    Date created: Oct 2018
    Python Version: 3.7
'''

import curses
import math
import time

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

#                     Helper functions

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# Curses helper function from http://devcry.heiho.net/html/2016/20160228-curses-practices.html
# This helps identify when escape key is pressed to exit the program
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

def resize_event():
    y, x = screen.getmaxyx()
    screen.clear()
    curses.resizeterm(y, x)
    screen.refresh()

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

screen = curses.initscr()

receivedBuffer = ['message 1', 'message 2', 'message 3', 'message 4', 'message 5', 'message 6']


# Press escape key to exit
q = ''


##############################
#                            #
#         Main Loop          #
#                            #
##############################

while q != 'ESC':
  screen.clear()

  # Note that coordinates appear in the order y,x not x,y
  dims = {'x': screen.getmaxyx()[1], 'y': screen.getmaxyx()[0]}

  # Create a divider string to separate the screen
  divider = '~' * dims['x']
  divider_position = int(dims['y']/2)

  screen.addstr(divider_position, 0, divider)

  # Draw messages received from serial port
  receiveArea = {'start': int(dims['y']/2 + 1), 'lines': dims['y'] - int(dims['y']/2 + 1)}

  for i,line in enumerate(range(receiveArea['lines'])):
    screen.addstr(receiveArea['start'] + i, 0, receivedBuffer[-(receiveArea['lines']):][0])

  q = getch()
  screen.refresh()


##############################
#                            #
#      Exit and Clean Up     #
#                            #
##############################


# Clear screen and exit
screen.clear()
curses.endwin()