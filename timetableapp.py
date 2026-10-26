from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Timetable works!"

app.run(debug=True)