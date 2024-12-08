import csv
import os

def store(name,message):
    message_data = [[name, message]]
    print(message_data)
    with open('temp_data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(message_data)

if __name__ == "__main__":
    store('n1','m1')
    with open('temp_data.csv')as file:
        message_csv = csv.reader(file)
        for row in message_csv:
            print(row[0])
            print(row[1])
    store('n2','m2')
    with open('temp_data.csv')as file:
        message_csv = csv.reader(file)
        for row in message_csv:
           print(row)
    os.remove('temp_data.csv')
