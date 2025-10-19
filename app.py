from flask import Flask, render_template, request, redirect, url_for
from gemini import queryGemini
import json
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
<<<<<<< HEAD
    return render_template("home_index.html")
=======
<<<<<<< HEAD
    return render_template("login_index.html")
=======
    return render_template("game_html.html")
>>>>>>> origin/main
>>>>>>> e58b28d05f1ff259d8c06996110de5e2c4e0f59d

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
<<<<<<< HEAD
        return render_template("login_index.html")
=======
<<<<<<< HEAD
        return render_template("login_index.html")
=======
        return render_template("login_html.html")
>>>>>>> origin/main
>>>>>>> e58b28d05f1ff259d8c06996110de5e2c4e0f59d
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        query = "SELECT password, user_id FROM users WHERE email = ?"
        result = cursor.execute(query, (email,)).fetchall()
        if result:
            checkPassword, userId = result[0]
        else:
            checkPassword, userId = None, None
        conn.commit()
        conn.close()

        if checkPassword == password:
            return redirect(f"/dashboard_html.html/{userId}")
        else:
            return redirect(url_for('login'))

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
        cursor.execute(query, (username, email, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

@app.route("/dashboard_html.html/<username>")
def dashboard(username):
    return render_template("dashboard_html.html", username=username)



@app.route("/submit", methods=["POST"])
def submit():
    pdf = request.files["file"]
    pdf.save(f"uploads/{pdf.filename}")

    response = queryGemini(pdf.filename)
    response = json.loads(response)

    return render_template("display_html.html", response=response)

@app.route("/game")
def game():
    return render_template("game_html.html")


@app.route("/cashflow")
def cashflow():
    return render_template("cash-flow-tracker.html")


@app.route("/contractconsultant")
def contractconsultant():
    return render_template("upload_html.html")

@app.route("/home")
def home():
    return render_template("home_index.html")





if __name__ == "__main__":
    app.run(debug=True)

