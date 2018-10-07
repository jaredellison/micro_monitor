# Python Serial

This directory encludes python tools to send and receive serial data for developing and debugging code on teensy microcontrollers. It is intended to help replace the arduino IDE.

The general idea is to open two terminal windows to work in: one for sending information, the other for receiving it. 

At some point it might be interesting to combine both these functions into a single window command line GUI type application.

## How to use:

Open two terminal windows. In the one for sending data, run the attached 



## Dependencies:

Python 3.7.0

https://github.com/pyserial/pyserial

## Basis:

### Figuring Out Which Serial Port To Use:

Run the terminal command

```bash
ls /dev/tty.usb*
```

For example the serial port for a teensy 3.2 was: `/dev/cu.usbmodem4091371`

The port `/dev/cu.usbmodem4091371` is used for sending data while the port `/dev/tty.usbmodem4091371`  is used for receiving data.

### Receiving Data:

Open miniterm.py by running the command:

```bash
python -m serial.tools.miniterm <serial port>
```

### Sending Data:

Open a serial port 

```python
import serial
ser = serial.Serial('/dev/cu.usbmodem4091371', 9600)

def serialout(string):
    string = string+'\n'
    ser.write(string.encode())
```



## Helpful links:

The Python Serial Library: 
https://media.readthedocs.org/pdf/pyserial/latest/pyserial.pdf



Receiving Data from a serial port:

https://arduino.stackexchange.com/questions/19002/use-unix-terminal-instead-of-the-monitor-on-arduino-ide



Sending data to a serial port: 
https://stackoverflow.com/questions/32018993/how-can-i-send-a-byte-array-to-a-serial-port-using-python