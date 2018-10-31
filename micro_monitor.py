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
        self.serial_port = self.open_serial_connection()
        self.initilize_curses()

    def run(self):
        self.serial_monitor()
        self.exit()

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
    #       Serial Monitor       #
    #                            #
    ##############################

    def serial_monitor(self):
        # If any errors occur, curses leaves a mess in the terminal.
        # If any exeptions happen, exit gracefully.
        # try:
            while True:
                self.screen.clear()

                # Get termianl dimensions
                # Note that coordinates appear in the order y,x not x,y
                self.dimensions = {'x': self.screen.getmaxyx()[1], 'y': self.screen.getmaxyx()[0]}
                self.division_point = math.floor(int(self.dimensions['y']/2))

                if self.dimensions['y'] < 4 or self.dimensions['y'] < 8:
                    raise RuntimeError('Window too small for micro_monitor')

                self.draw_section_dividers()

                self.receive_message()

                self.draw_received()

                self.draw_sent()

                self.draw_prompt()

                self.draw_cursor()

                # Check for input characters
                char_in = self.getch()
                if char_in == 'ESC':
                    break
                elif char_in:
                    self.assemble_to_send(char_in)

                # Draw all changes to the screen
                self.screen.refresh()

        # except Exception as e:
        #     message = 'Exiting with error: ' + str(e)
        #     self.exit(message)



    ##############################
    #                            #
    #     Initialize Methods     #
    #                            #
    ##############################

    def welcome(self):
         print("""
 .       __   __   __            __         ___  __   __
 |\\/| | /  ` |__) /  \\     |\\/| /  \\ |\\ | |  |  /  \\ |__)
 |  | | \\__, |  \\ \\__/ ___ |  | \\__/ | \\| |  |  \\__/ |  \\\n""")


    def open_serial_connection(self):
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


    def initilize_curses(self):
        self.screen = curses.initscr()

        # Don't show characters on the screen as they're typed. Characters are
        # shown using the assemble_to_send() function.
        curses.noecho()

        # The function curses_getch() blocks the cpu waiting for input so it's
        # important to set a timeout value for the screen. 250 Milliseconds is the
        # default. If the value is set too low, the script REALLY uses the CPU and
        # the screen may flicker but setting it lower does mean that incoming bytes
        # are displayed quicker.
        self.screen.timeout(250)

        curses.cbreak()
        self.screen.keypad(True)

        # Color Handling
        curses.start_color()
        curses.use_default_colors()

        # Set the input prompt cursor to blue
        # Init color pair is set with the arguments:
        #   id # starting at 1 (0 is the default)
        #   foreground color (-1 is the default color)
        #   background color (-1 is the default color)
        curses.init_pair(1, curses.COLOR_BLUE, -1)

        self.blue_text = curses.color_pair(1)

    ##############################
    #                            #
    #       Curses Methods       #
    #                            #
    ##############################

    # Curses helper function from:
    # http://devcry.heiho.net/html/2016/20160228-curses-practices.html
    # This helps identify when escape key is pressed to exit the program
    def getch(self):
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


    ##############################
    #                            #
    #       Serial Helpers       #
    #                            #
    ##############################


    # Text is input to the script as a string, here we add a new line character
    # and encode it to binary and send it to the open serial port.
    def serial_out(self, string):
        string = string + '\n'
        self.serial_port.write(string.encode())


    def receive_message(self):
        # ser.in_waiting shows the number of bytes waiting to be read.
        # We only want to read them if they exist, otherwise the program will hang.
        if self.serial_port.in_waiting:
            line = self.serial_port.readline()
            if line:
                self.received_buffer.append(line.decode('utf-8').strip())
        return


    def assemble_to_send(self, char):
        # char is the ascii code for a character
        # New Line
        if char in ('\n', 'Ctrl-J'):
            self.serial_out(self.send_message)
            self.sent_buffer.append(self.send_message)
            self.send_message = ''

        # Backspace
        if char in ('KEY_BACKSPACE', '\b', '\x7f', '0x7f', '0x107'):
            self.send_message = self.send_message[0:-1]

        # Other characters
        elif is_ascii(char):
            self.send_message = self.send_message + char

        return

    ##############################
    #                            #
    #       Drawing Methods      #
    #                            #
    ##############################

    def draw_section_dividers(self):
        # Create section dividers to separate the screen
        send_label = '◦ send:      '
        receive_label = '◦ receive:   '
        send_divider = send_label + '─' * (self.dimensions['x'] - len(send_label))
        receive_divider = receive_label + '─' * (self.dimensions['x'] - len(receive_label))
        self.screen.addstr(0, 0, send_divider, self.blue_text)
        self.screen.addstr(self.division_point, 0, receive_divider, self.blue_text)


    def draw_sent(self):
        send_area_lines = self.division_point - 2

        # Slice total buffer down to the number
        # of messages that can be displayed
        printable_messages = self.sent_buffer[-send_area_lines:]
        for i, message in enumerate(printable_messages):
            # if messages are too long to fit on screen, trim them
            message = message[:self.dimensions['x']]
            self.screen.addstr(1 + i, 0, message)

        self.prompt_position = len(printable_messages) + 1


    def draw_received(self):
        receive_area_lines = self.dimensions['y'] - self.division_point - 1

        # Slice total buffer down to the number
        # of messages that can be displayed
        printable_messages = self.received_buffer[-receive_area_lines:]
        for i, message in enumerate(printable_messages):
            # if messages are too long to fit on screen, trim them
            message = message[:self.dimensions['x']]
            self.screen.addstr(self.division_point + 1 + i, 0, message)


    def draw_prompt(self):
        prompt_str = '>_ '
        self.prompt_length = len(prompt_str)
        # Print the blue colored cursor where new text input shows up
        self.screen.addstr(self.prompt_position, 0, prompt_str, self.blue_text)
        # Print the new string we're assembling
        self.screen.addstr(self.prompt_position, self.prompt_length, self.send_message)


    def draw_cursor(self):
        # Set cursor position to end of message being typed
        self.screen.move(self.prompt_position, self.prompt_length + len(self.send_message))


if __name__ == '__main__':
    app = App()

    app.run()

