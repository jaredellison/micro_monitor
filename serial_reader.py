#! /usr/bin/python
'''
    File name: talk_by_terminal.py
    Author: Jared Ellison
    Date created: Oct 2018
    Python Version: 3.7
'''

# import serial
import serial
from serial.tools import list_ports


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

#                     Helper functions

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# A simple function to test if input strings are valid as integers
def is_int(s):
  try:
      int(s)
      return True
  except ValueError:
      return False

def receive_message():
  # global ser
  line = ser.readline()
  if line:
    # received_buffer.append(str(line))
    print(line.decode('utf-8').strip())
  return


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

##############################
#                            #
#      Global Variables      #
#                            #
##############################

send_message = ''
sent_buffer = ['sent msg 1', 'sent msg 2', 'sent msg 3', 'sent msg 4', 'sent msg 5', 'sent msg 6', 'sent msg 7', 'sent msg 8']
inputLine = 0
received_buffer = ['received msg 1', 'received msg 2', 'received msg 3', 'received msg 4', 'received msg 5', 'received msg 6']


##############################
#                            #
#      Select Serial Port    #
#                            #
##############################

# search for available usb serial ports
available_ports = [e for e in list_ports.grep('usb')]

# Print a list of available devices
print('Please select a serial device:')
for i, port in enumerate(available_ports):
  print('   {}. {} {}'.format(i + 1, port.device, port.manufacturer))

if len(available_ports) == 1:
  print('Only one usb port available:')
  selected_port = available_ports[0]
  serSend_path = selected_port.device
  ser = serial.Serial(serSend_path, 9600)
  print(' -> Port selection: ' + selected_port.device + ' ' + selected_port.manufacturer)
  print(' -> Serial port connection opened at 9600 baud')
else:
  # Listen for a selection
  while True:
    selection = input('Port number: ')
    # If it's a valid selection, open that port for communication
    if is_int(selection) and int(selection) in range(1, len(available_ports) + 1):
      print(' -> Port selection: ' + port.device + ' ' + port.manufacturer)
      selected_port = available_ports[int(selection) - 1]
      serSend_path = selected_port.device
      ser = serial.Serial(serSend_path, 9600, timeout=1)
      # serReturn_path = 'tty'.join(serSend_path.split('cu'))
      # print('return path: ' + serReturn_path)
      # serReturn = serial.Serial(serReturn_path, 9600)
      print(' -> Serial port connection opened at 9600 baud')
      break
    else:
      print('Please enter a valid port number')

while True:
  receive_message()
