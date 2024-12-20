import time
import socket
import yaml
import csv
import os

def connect():
    with open('config.yml', 'r') as f:
       yaml_data = yaml.load(f, Loader=yaml.SafeLoader)
    serverMACAddress = yaml_data['mac']
    port = 1
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.connect((serverMACAddress,port))
    return s

"""
def store(name,message):
    try:
        s = connect()
        faxprint(s,name,message)
    except:
        # write into dB
        message_data = [name, message]
        with open('temp_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(message_data)
"""

def print_records(s):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    csv_filename = dir_path + '/temp_data.csv'
    if os.path.exists(csv_filename):
        with open(csv_filename)as file:
            message_csv = csv.reader(file)
            for row in message_csv:
                    name = row[0]
                    message = row[1]
                    print("printing")
                    print(name,message)
                    faxprint(s,name,message)
        os.remove(csv_filename)
    else:
        print('No data to print')

def faxprint(s,name,message):
    print("Serial Open")
    if len(name) < 40:
        s.send(bytearray(("from " +  name + ": "), 'utf-8'))
        s.send(bytearray('\n', 'utf-8'))
        print("Name printed")
    time.sleep(0.1)
    if len(message) < 240:
        s.send(bytearray(message, 'utf-8'))
        s.send(bytearray('\n', 'utf-8'))
        s.send(bytearray('\n', 'utf-8'))
        print("Message Printed")

if __name__ == "__main__":
    while True:
        #check if bluetooth connection works
        try:
            s = connect()
            print('Bluetooth Active')
            print_records(s)
            s.close()
        except:
            print('Bluetooth not active')
        time.sleep(5*60) #try it every 5 minutes
