# micro_monitor.py

This project is a command line serial monitor utility intended to replace the Arduino IDE serial monitor with a quick and lightweight command line tool.

The project is built with Python 3, it uses the [pySerial library](https://github.com/pyserial/) to identify and communicate with serial ports, and it uses the python [Curses library](https://docs.python.org/3/library/curses.html#module-curses) to render a simple text based user interface in a terminal window.

This script has been tested using Mac OS and Linux but it may work for Windows as well.

## Installation

Python 3 and the pip package manager are required, if you don't have them, learn how to install them [here](https://docs.python-guide.org/starting/installation/).

Before using micro_monitor, use pip install the dependences:

```bash
pip install -r requirements.txt
```

If you like the tool, you may want to make it executable and save an alias for it in your system.

## Using micro_monitor.py

### Opening a connection

micro_monitor first checks for available serial ports. Because printers and other devices often appear in this list, it only searches for devices which include "usb" in their name. If one port exists, it is selected by default, if multiple ports exist you may select the desired one.

Connections are opened at a baudrate of 9600 by default.

```bash
One usb port available:
 -> Port selection: /dev/cu.usbmodem4091371 Teensyduino
 -> Serial port connection opened at 9600 baud
```

### The Monitor Window

Once a connection is available, press `return` to enter the serial monitor window. You may press the `escape` key to exit at any time.

The window is divided in half into send and receive sections.

A prompt in the send section allows you to compose a string to send to the serial port. This prompt is very basic, only ascii characters are allowed but it is possible to type a simple command, use the `backspace` key and press `return` to send the command. 

The receive section displays the most recently received messages from the serial port.

The monitor window may be resized while the script runs. The most recently sent and recieved messages are always displayed.


## Acknowledgments and Resources

* **pySerial**  - *Great documentation* - [pySerial Docs](https://pythonhosted.org/pyserial/)
* **Python Curses Tutorial** - *A big picture introduction to Curses* - [Tutorial Videos](https://www.youtube.com/channel/UCXCA0fPu6uPjWv9p4uUrpEQ)
* **Basics of communicating with serial ports in unix**
  * [Receiving data](https://arduino.stackexchange.com/questions/19002/use-unix-terminal-instead-of-the-monitor-on-arduino-ide)
  * [Sending data](https://stackoverflow.com/questions/32018993/how-can-i-send-a-byte-array-to-a-serial-port-using-python)
* **Handling special characters in Curses** - *A very helpful function* - [The Developer's Cry Blog](http://devcry.heiho.net/html/2016/20160228-curses-practices.html)