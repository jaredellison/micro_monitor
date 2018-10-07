# import serial
import serial
from serial.tools import list_ports

# A simple function to test if input strings are valid as integers
def representsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

# search for available usb serial ports
available_ports = [e for e in list_ports.grep('usb')]

# Print a list of available devices
print('Please select a serial device:')
for i, port in enumerate(available_ports):
  print('   {}. {} {}'.format(i + 1, port.device, port.manufacturer))

# Listen for a selection
while True:
  selection = input('Port number: ')
  # If it's a valid selection, open that port for communication
  if representsInt(selection) and int(selection) in range(1, len(available_ports) + 1):
    print('Port selection: ' + port.device + ' ' + port.manufacturer)
    selected_port = available_ports[int(selection) - 1]
    serSend_path = selected_port.device
    ser = serial.Serial(serSend_path, 9600)
    # serReturn_path = 'tty'.join(serSend_path.split('cu'))
    # print('return path: ' + serReturn_path)
    # serReturn = serial.Serial(serReturn_path, 9600)
    print('Serial port connection opened at 9600 baud')
    break
  else:
    print('Please enter a valid port number')

# Text is input to the script as a string, here we add a new line character
# and endode it to binary and send it to the open serial port.
def serialout(string):
    string = string+'\n'
    ser.write(string.encode())

while True:
  # while ser.in_waiting:  # Or: while ser.inWaiting():
  #     print(ser.readline().decode('utf-8').strip())
  #     print(ser.in_waiting)
  command_in = input('> ')
  if command_in[0] == '!':
    exec(command_in[1:])
  else:
    serialout(command_in)