# https://stackoverflow.com/questions/676172/full-examples-of-using-pyserial-package#7654527

import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM4',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()

print('Enter your commands below.\r\nInsert "exit" to leave the application.')

term_input=1
while 1 :
    # get keyboard input
        #input = raw_input(">> ")
        # Python 3 users
    term_input = input(">> ")
    if term_input == 'exit':
        ser.close()
        exit()
    else:
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        term_bytes = bytearray((term_input), 'utf-8')
        #term_bytes += b'\x0d\x0a'
        ser.write(term_bytes)
        ser.write(bytearray(("\n"), 'utf-8')) #it probably prints after an enter, but needs \n to get it visible
        ser.write(bytearray(("\n"), 'utf-8'))
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read(1)
            
        if out != '':
            print(">>") + out