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
print("Serial Open")

# end command: \n
term_input = "hi abbi"
term_bytes = bytes((term_input + '\n'), 'utf-8')
ser.write(term_bytes)
out = ''
time.sleep(0.5)
while ser.inWaiting() > 0:
    out += ser.read(1)
if out != '':
    print(">>") + out
ser.close()
exit()