#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    File name: micro_monitor.py
    Author: Jared Ellison
    Date created: Oct 2018
    Python Version: 3.7
'''

import curses
import math
import serial
from serial.tools import list_ports
from getch import getch

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

#                     Helper functions

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~



##############################
#                            #
#       Serial Helpers       #
#                            #
##############################


# Text is input to the script as a string, here we add a new line character
# and encode it to binary and send it to the open serial port.
def serial_out(serial_port, string):
    string = string + '\n'
    serial_port.write(string.encode())


def receive_message(serial_port):
    # ser.in_waiting shows the number of bytes waiting to be read.
    # We only want to read them if they exist, otherwise the program will hang.
    if serial_port.in_waiting:
        line = serial_port.readline()
        if line:
            received_buffer.append(line.decode('utf-8').strip())
    return


def assemble_to_send(serial_port, char, send_message, sent_buffer):
    # char is the ascii code for a character
    # New Line
    if char in ('\n', 'Ctrl-J'):
        serial_out(serial_port, send_message)
        sent_buffer.append(send_message)
        send_message = ''

    # Backspace
    if char in ('KEY_BACKSPACE', '\b', '\x7f', '0x7f', '0x107'):
        send_message = send_message[0:-1]

    # Other characters
    elif is_ascii(char):
        send_message = send_message + char

    return (send_message, sent_buffer)


##############################
#                            #
#          Drawing           #
#                            #
##############################


def draw_section_dividers(division_point, dimensions):
    # Create section dividers to separate the screen
    send_label = '◦ send:      '
    receive_label = '◦ receive:   '
    send_divider = send_label + '─' * (dimensions['x'] - len(send_label))
    receive_divider = receive_label + '─' * (dimensions['x'] - len(receive_label))
    screen.addstr(0, 0, send_divider, curses.color_pair(1))
    screen.addstr(division_point, 0, receive_divider, curses.color_pair(1))


def draw_sent(division_point, dimensions, sent_buffer):
    send_area_lines = division_point - 2

    # Slice total buffer down to the number
    # of messages that can be displayed
    printable_messages = sent_buffer[-send_area_lines:]
    for i, message in enumerate(printable_messages):
        # if messages are too long to fit on screen, trim them
        message = message[:dimensions['x']]
        screen.addstr(1 + i, 0, message)

    prompt_position = len(printable_messages) + 1
    return prompt_position


def draw_received(division_point, dimensions, received_buffer):
    receive_area_lines = dimensions['y'] - division_point - 1

    # Slice total buffer down to the number
    # of messages that can be displayed
    printable_messages = received_buffer[-receive_area_lines:]
    for i, message in enumerate(printable_messages):
        # if messages are too long to fit on screen, trim them
        message = message[:dimensions['x']]
        screen.addstr(division_point + 1 + i, 0, message)


def draw_prompt(prompt_position, send_message):
    prompt_str = '>_ '
    prompt_length = len(prompt_str)
    # Print the blue colored cursor where new text input shows up
    screen.addstr(prompt_position, 0, prompt_str, curses.color_pair(1))
    # Print the new string we're assembling
    screen.addstr(prompt_position, prompt_length, send_message)
    return prompt_length


def draw_cursor(prompt_position, prompt_length, send_message):
    # Set cursor position to end of message being typed
    screen.move(prompt_position, prompt_length + len(send_message))

##############################
#                            #
#          Tests             #
#                            #
##############################


# Test a single character to see if it is ascii
def is_ascii(c):
    return len(c) == 1 and 31 < ord(c) < 128


# Test if input strings are valid as integers
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

#                     Core Functions

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


def serial_monitor(serial_port, screen, sent_buffer,
                   received_buffer, send_message):
    # If any errors occur, curses leaves a mess in the terminal.
    # If any exeptions happen, exit gracefully.
    try:
        while True:
            screen.clear()

            # Get termianl dimensions
            # Note that coordinates appear in the order y,x not x,y
            dims = {'x': screen.getmaxyx()[1], 'y': screen.getmaxyx()[0]}
            mid_y = math.floor(int(dims['y']/2))

            if dims['y'] < 4 or dims['y'] < 8:
                raise RuntimeError('Window too small for micro_monitor')

            draw_section_dividers(mid_y, dims)

            receive_message(serial_port)

            draw_received(mid_y, dims, received_buffer)

            prompt_position = draw_sent(mid_y, dims, sent_buffer)

            prompt_length = draw_prompt(prompt_position, send_message)

            draw_cursor(prompt_position, prompt_length, send_message)

            # Check for input characters
            char_in = getch_curses()
            if char_in == 'ESC':
                break
            elif char_in:
                send_message, sent_buffer = assemble_to_send(serial_port,
                                                             char_in,
                                                             send_message,
                                                             sent_buffer)

            # Draw all changes to the screen
            screen.refresh()

    except Exception as e:
        message = 'Exiting with error: ' + str(e)
        exit_gracefully(screen, curses, message=message)



# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

#                     Main Class

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

class App():

    ##############################
    #                            #
    #         Core Methods       #
    #                            #
    ##############################

    def __init__(self):
        self.send_message = ''
        self.sent_buffer = []
        self.received_buffer = []

        self.welcome()
        self.serial_port = open_serial_connection()
        self.screen = initilize_curses()

    def run(self):
        self.serial_monitor(serial_port, screen, sent_buffer,
                       received_buffer, send_message)
        self.exit_gracefully(screen, curses)

    def exit(self, message=''):
        # Clear screen and exit, possibly printing message
        self.screen.clear()
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

        if message:
            print(message)

        exit()

    ##############################
    #                            #
    #     Initialize Methods     #
    #                            #
    ##############################

    def welcome():
         print("""
 .       __   __   __            __         ___  __   __
 |\\/| | /  ` |__) /  \\     |\\/| /  \\ |\\ | |  |  /  \\ |__)
 |  | | \\__, |  \\ \\__/ ___ |  | \\__/ | \\| |  |  \\__/ |  \\\n""")


    def open_serial_connection():
        # search for available usb serial ports
        available_ports = [e for e in list_ports.grep('usb')]

        if len(available_ports) == 0:
            print('No usb serial ports available, '
                  + 'please check that devices are connected.')
            exit()
        elif len(available_ports) == 1:
            print('One usb port available:')
            selected_port = available_ports[0]
            ser_send_path = selected_port.device
            ser = serial.Serial(ser_send_path, 9600)
            print(' -> Port selection: ' + selected_port.device
                  + ' ' + selected_port.manufacturer)
            print(' -> Serial port connection opened at 9600 baud')
        else:
            print('Please select a serial device:')
            # Print a list of available devices
            for i, port in enumerate(available_ports):
                print('   {}. {} {}'.format(i + 1, port.device, port.manufacturer))
            # Listen for a selection
            while True:
                selection = input('Port number: ')
                # If it's a valid selection, open that port for communication
                if is_int(selection) \
                   and int(selection) in range(1, len(available_ports) + 1):
                    print(' -> Port selection: ' + port.device
                          + ' ' + port.manufacturer)
                    selected_port = available_ports[int(selection) - 1]
                    ser_send_path = selected_port.device
                    ser = serial.Serial(ser_send_path, 9600, timeout=.1)
                    print(' -> Serial port connection opened at 9600 baud')
                    break
                else:
                    print('Please enter a valid port number')

        # Let users know how to quit
        print('\nPress escape key to exit at any time.'
              + '\nPress return to enter serial monitor.')

        while True:
            key_input = getch()
            # Check if escape key is pressed
            if ord(key_input) == 27:
                exit()
            else:
                break
        return ser


    def initilize_curses():
        screen = curses.initscr()

        # Don't show characters on the screen as they're typed. Characters are
        # shown using the assemble_to_send() function.
        curses.noecho()

        # The function curses_getch() blocks the cpu waiting for input so it's
        # important to set a timeout value for the screen. 250 Milliseconds is the
        # default. If the value is set too low, the script REALLY uses the CPU and
        # the screen may flicker but setting it lower does mean that incoming bytes
        # are displayed quicker.
        screen.timeout(250)

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

        return screen

    ##############################
    #                            #
    #       Curses Methods       #
    #                            #
    ##############################

    # Curses helper function from:
    # http://devcry.heiho.net/html/2016/20160228-curses-practices.html
    # This helps identify when escape key is pressed to exit the program
    def getch_curses(self):
        KEY_TABLE = {'0x1b': 'ESC'}
        # Returns keystroke as string

        key = self.screen.getch()

        if key == curses.KEY_RESIZE:
            resize_event()

        elif ord(' ') <= key <= ord('~'):
            # ascii key
            return chr(key)

        elif 1 <= key <= 26:
            # Ctrl-A to Ctrl-Z
            return 'Ctrl-' + chr(ord('@') + key)

        # special key : use a lookup table
        skey = '0x%02x' % key
        if skey in KEY_TABLE:
            return KEY_TABLE[skey]

        # unknown key; just return as a hex string
        return skey


    def resize_event(self):
        y, x = self.screen.getmaxyx()
        self.screen.clear()
        curses.resizeterm(y, x)
        self.screen.refresh()



if __name__ == '__main__':
    app = App()

    app.run()

