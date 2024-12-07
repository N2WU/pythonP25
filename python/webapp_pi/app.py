from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def store(name,message):
    message_data = [[name, message]]
    with open('temp_data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(message_data)

# Route to display the form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]
        if len(message) > 140:
            return f"Your message was too long. Please retry."
        else:
            store(name,message)
            return f"Thank you {name}! Your message: '{message}' has been received."
    return render_template("form.html")
# there needs to be some form of hook here or in the serial thing

if __name__ == "__main__":
    app.run(debug=True)

