import time
import socket
# configure the serial connections (the parameters differs on the device you are connecting to)

if __name__ == "__main__":

    serverMACAddress = '00:08:1b:95:5c:3d'
    port = 1
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.connect((serverMACAddress,port))

    print("Serial Open")

    # end command: \n
    term_input = "hi abbi"
    term_bytes = bytes((term_input + '\n'), 'utf-8')
    s.send(term_bytes)
    time.sleep(0.5)
    s.close()
    exit()
