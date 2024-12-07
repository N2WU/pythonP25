from flask import Flask, render_template, request
import time
import socket
import yaml

app = Flask(__name__)

def faxprint(name,message):
    with open('config.yml', 'r') as f:
       yaml_data = yaml.load(f, Loader=yaml.SafeLoader)
    serverMACAddress = yaml_data['mac']
    port = 1
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.connect((serverMACAddress,port))
    print("Serial Open")
    if len(name) < 40:
        s.send(bytearray(("from " +  name + ": "), 'utf-8'))
        s.send(bytearray('\n', 'utf-8'))
        print("Name printed")
    time.sleep(0.1)
    if len(message) < 140:
        s.send(bytearray(message, 'utf-8'))
        s.send(bytearray('\n', 'utf-8'))
        s.send(bytearray('\n', 'utf-8'))
        print("Message Printed")
    s.close()

# Route to display the form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]
        if len(message) > 140:
            return f"Your message was too long. Please retry."
        else:
            faxprint(name,message)
            return f"Thank you {name}! Your message: '{message}' has been received."
    return render_template("form.html")
# there needs to be some form of hook here or in the serial thing

if __name__ == "__main__":
    app.run(debug=True)

