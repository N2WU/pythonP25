from flask import Flask, render_template, request
import time
import serial

app = Flask(__name__)

def faxprint(name,message):
    ser = serial.Serial(
    port='COM4',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS,
    )
    ser.isOpen()
    print("Serial Open")
    #ret_byte = bytearray('\n', 'utf-8')
    #ser.reset_output_buffer
    if len(name) < 40:
        ser.write(bytearray(("from " +  name + ": "), 'utf-8'))
        ser.write(bytearray('\n', 'utf-8'))
        print("Name printed")
    time.sleep(0.1)
    if len(message) < 140:
        ser.write(bytearray(message, 'utf-8'))
        ser.write(bytearray('\n', 'utf-8'))
        ser.write(bytearray('\n', 'utf-8'))
        print("Message Printed")
    out = ''
    time.sleep(0.5)
    while ser.inWaiting() > 0:
        out += ser.read(1)
    if out != '':
        print(">>") + out
        ser.close()

# Route to display the form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]
        faxprint(name,message)
        return f"Thank you {name}! Your message: '{message}' has been received."
    return render_template("form.html")
# there needs to be some form of hook here or in the serial thing

if __name__ == "__main__":
    # would running code here work?
    #ser = serial.Serial(
    #port='COM4',
    #baudrate=115200,
    #parity=serial.PARITY_NONE,
    #stopbits=serial.STOPBITS_TWO,
    #bytesize=serial.EIGHTBITS,
    #)
    #ser.isOpen()
    #print("Serial Open")
    #ser.close()
    app.run(debug=True)

