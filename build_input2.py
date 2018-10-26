import curses, time

############################## 
#                            #
#      Global Variables      #
#                            #
##############################

sendString = ''
sentStrings = ['string1', 'string2', 'string3', 'string4']
inputLine = 0

def assembleLine(char):
  # char is the ascii code for a character
  global sendString
  global sentStrings
  # New Line
  # if char == 10:      
  if char in ('\n', 'Ctrl-J'):      
    sentStrings.append(sendString)
    sendString = ''
    return
  # # Backspace
  if char in ('KEY_BACKSPACE', '\b', '\x7f', '0x7f'):
    sendString = sendString[0:-1] 
    return
  # # Other characters
  else:
    sendString = sendString + char
    return

# Curses helper function from http://devcry.heiho.net/html/2016/20160228-curses-practices.html
def getch():
  KEY_TABLE = {'0x1b': 'ESC'}
  '''Returns keystroke as string''' 

  key = screen.getch()

  if key >= ord(' ') and key <= ord('~'):
    # ascii key
    return chr(key)

  elif key >= 1 and key <= 26:
    # Ctrl-A to Ctrl-Z
    return 'Ctrl-' + chr(ord('@') + key)

  # special key : use a lookup table
  skey = '0x%02x' % key
  if skey in KEY_TABLE:
    return KEY_TABLE[skey]

  # unknown key; just return as a hex string
  return skey


# Reduce the delay time when the escape key is pressed to exit the program  
def set_shorter_esc_delay_in_os():
  os.environ.setdefault('ESCDELAY', '25')
    

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 



# From https://stackoverflow.com/questions/14004835/nodelay-causes-python-curses-program-to-exit
def main(screen):
  screen.nodelay(1)
  screen.clear()

  # Print all the lines that have come before
  for i, line in enumerate(sentStrings):
    screen.addstr(i, 0, line)

  # Print the blue colored cursor where new text input shows up
  screen.addstr(len(sentStrings), 0, '>_ ', curses.color_pair(1))
  # Print the new string we're assembling
  screen.addstr(len(sentStrings), 3, sendString)

  # Get a new 
  charInput = getch()
  # if charInput == 'ESC':
  #   break
  assembleLine(charInput)

  screen.refresh()



if __name__=='__main__':
  screen = curses.initscr()

  curses.noecho()
  curses.cbreak()
  screen.keypad(True)
  screen.nodelay(True)
  curses.start_color()
  curses.use_default_colors()

  # Set the input prompt cursor to blue
  curses.init_pair(1, curses.COLOR_BLUE, -1)

  curses.wrapper(main)
