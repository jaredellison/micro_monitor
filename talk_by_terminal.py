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

def draw_section_dividers():
  # Create section dividers to separate the screen
  send_divider = '◦ send:      ' + '─' * (dims['x'] - 13)
  receive_divider = '◦ receive:   ' + '─' * (dims['x'] - 13)
  screen.addstr(0, 0, send_divider, curses.color_pair(1))
  screen.addstr(mid_y, 0, receive_divider, curses.color_pair(1))

def draw_received():
  # Draw messages received from serial port
  receive_area = {'start': int(dims['y']/2 + 1),
                  'lines': dims['y'] - int(dims['y']/2 + 1)}

  # Slice total received buffer down to the number of messages that can be displayed
  printable_messages = received_buffer[-receive_area['lines']:]
  for i, message in enumerate(printable_messages):
    screen.addstr(mid_y + 1 + i, 0, message)


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

##############################
#                            #
#      Global Variables      #
#                            #
##############################

sendString = ''
sentStrings = ['sent msg 1', 'sent msg 2', 'sent msg 3', 'sent msg 4']
inputLine = 0

##############################
#                            #
#         Initialize         #
#                            #
##############################

screen = curses.initscr()

curses.noecho()
curses.cbreak()
screen.keypad(True)

# Color Handling
curses.start_color()
curses.use_default_colors()

# Set the input prompt cursor to blue
# Init color pair is set with the arguments:
#   id # starting at 1 (0 is the default)
#   foreground color (-1 is the default color)
#   background color (-1 is the default color)
curses.init_pair(1, curses.COLOR_BLUE, -1)

received_buffer = ['received msg 1', 'received msg 2', 'received msg 3', 'received msg 4', 'received msg 5', 'received msg 6']

# Press escape key to exit
q = ''


##############################
#                            #
#         Main Loop          #
#                            #
##############################

while True:
  screen.clear()

  # Get termianl dimensions
  # Note that coordinates appear in the order y,x not x,y
  dims = {'x': screen.getmaxyx()[1], 'y': screen.getmaxyx()[0]}
  mid_y = math.floor(int(dims['y']/2))

  draw_section_dividers()

  draw_received()

  # Check for input characters
  charInput = getch()
  if charInput == 'ESC':
    break

  # Draw all changes to the screen
  screen.refresh()


##############################
#                            #
#      Exit and Clean Up     #
#                            #
##############################

# Clear screen and exit
screen.clear()

curses.nocbreak()
screen.keypad(0)
curses.echo()

screen.clear()
curses.endwin()