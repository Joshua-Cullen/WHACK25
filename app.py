import datetime
import json
import sqlite3

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

from gemini import queryGemini
from pdfHighlighting import highlight_pdf

app = Flask(__name__)
app.secret_key = "replace-this-with-a-secure-random-key"


@app.context_processor
def inject_request():
    return dict(request=request)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
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
            session["user_id"] = userId
            return redirect(url_for("home", username=userId))
        else:
            return render_template("login.html", error="Invalid credentials")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
            cursor.execute(query, (username, email, password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template(
                "signup.html", error="An account with that email already exists"
            )
        conn.close()

        return redirect(url_for("login"))


@app.route("/submit", methods=["POST"])
def submit():
    pdf = request.files["file"]
    filename = secure_filename(pdf.filename)
    save_path = f"uploads/{filename}"
    pdf.save(save_path)

    try:
        response = queryGemini(filename)
        response = json.loads(response)
    except Exception as e:
        print("Contract analysis failed:", e)
        return render_template(
            "upload.html",
            error="Something went wrong analysing that file. Please check the server's Gemini API key and try again.",
        )

    highlighted_filename = None
    try:
        phrases = response.get("part_5") or response.get("part_4") or []
        if isinstance(phrases, list) and phrases:
            highlighted_filename = f"highlighted_{filename}"
            highlighted_path = f"uploads/{highlighted_filename}"
            highlight_pdf(save_path, highlighted_path, phrases)
    except Exception as e:
        print("Highlighting failed:", e)

    pdf_to_show = highlighted_filename or filename
    return render_template("upload.html", response=response, pdf_filename=pdf_to_show)


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)


@app.route("/quiz")
def quiz():
    return render_template("quiz.html")


@app.route("/game")
def game():
    return render_template("game.html")


@app.route("/cashflow")
def cashflow():
    return render_template("cash-flow-tracker.html")


@app.route("/contractconsultant")
def contractconsultant():
    return render_template("upload.html")


@app.route("/home/")
@app.route("/home/<username>")
def home(username=None):
    return render_template("index.html", username=username)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/api/entries/<username>", methods=["GET"])
def get_entries(username):
    user_id = session.get("user_id")
    if not user_id:
        today_iso = datetime.date.today().isoformat()
        return json.dumps(
            [
                {
                    "id": "demo1",
                    "date": today_iso,
                    "description": "Salary",
                    "amount": 2000.0,
                    "type": "income",
                },
                {
                    "id": "demo2",
                    "date": today_iso,
                    "description": "Coffee",
                    "amount": 3.50,
                    "type": "expense",
                },
            ]
        )
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT money_id, date, description, amount, type FROM money WHERE user_id = ?",
        (user_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    entries = []
    for row in rows:
        entries.append(
            {
                "id": row[0],
                "date": row[1],
                "description": row[2],
                "amount": row[3],
                "type": row[4],
            }
        )
    return json.dumps(entries)


@app.route("/api/entries", methods=["POST"])
def add_entry():
    user_id = session.get("user_id")
    if not user_id:
        return json.dumps({"status": "unauthorized"}), 401
    data = request.json
    date = data.get("date")
    description = data.get("description")
    amount = float(data.get("amount", 0))
    entry_type = data.get("type")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO money (user_id, date, description, amount, type) VALUES (?, ?, ?, ?, ?)",
        (user_id, date, description, amount, entry_type),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return json.dumps({"status": "success", "id": new_id})


@app.route("/api/entries/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    user_id = session.get("user_id")
    if not user_id:
        return json.dumps({"status": "unauthorized"}), 401
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM money WHERE money_id = ? AND user_id = ?", (entry_id, user_id)
    )
    conn.commit()
    conn.close()
    return json.dumps({"status": "success"})


@app.route("/api/quiz", methods=["POST"])
def save_quiz_score():
    user_id = session.get("user_id")
    if not user_id:
        return json.dumps({"status": "unauthorized"}), 401
    data = request.json
    score = int(data.get("score", 700))
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO quiz_scores (user_id, score) VALUES (?, ?)", (user_id, score)
    )
    conn.commit()
    conn.close()
    return json.dumps({"status": "success"})


@app.route("/api/quiz/high", methods=["GET"])
def get_quiz_high_score():
    user_id = session.get("user_id")
    if not user_id:
        return json.dumps({"high_score": 0})
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(score) FROM quiz_scores WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    high_score = result[0] if result[0] is not None else 0
    return json.dumps({"high_score": high_score})


if __name__ == "__main__":
    app.run(debug=True)
