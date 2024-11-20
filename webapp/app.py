from flask import Flask, render_template, request
import time
import serial

app = Flask(__name__)

def faxprint(name,message):
    ret_byte = bytearray('\n', 'utf-8')
    ser.isOpen()
    print("Serial Open")
    ser.reset_output_buffer
    ser.write(bytearray(("from: " +  name + ": "), 'utf-8'))
    time.sleep(0.1)
    ser.write(bytearray(message, 'utf-8'))
    out = ''
    time.sleep(0.5)
    while ser.inWaiting() > 0:
        out += ser.read(1)
    if out != '':
        print(">>") + out
        ser.close()
    exit()

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
    # setup serial
    ser = serial.Serial(
        port='COM4',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS
    )
    app.run(debug=True)
    # would running code here work?
