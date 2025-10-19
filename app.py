from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from gemini import queryGemini
from werkzeug.utils import secure_filename
import json
import sqlite3
from pdfHighlighting import highlight_pdf

app = Flask(__name__)
app.secret_key = "replace-this-with-a-secure-random-key"

# Context processor to make request available in templates
@app.context_processor
def inject_request():
    return dict(request=request)


@app.route('/')
def index():
    return render_template("home_index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login_index.html")
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
            # Set session so templates can detect logged-in user
            session['user_id'] = userId
            return redirect(url_for('home', username=userId))
        else:
            # On failure, re-render the login page with a message instead of silent redirect.
            return render_template('login_index.html', error='Invalid credentials')

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
    # sanitize filename and save to uploads directory
    filename = secure_filename(pdf.filename)
    save_path = f"uploads/{filename}"
    pdf.save(save_path)

    # call the analyzer and parse response
    response = queryGemini(filename)
    response = json.loads(response)

    # If the LLM returned part_5 (quotes to highlight), run the highlighter
    highlighted_filename = None
    try:
        phrases = response.get("part_5") or response.get("part_4") or []
        # part_5 should be a list of exact quotes to highlight
        if isinstance(phrases, list) and phrases:
            highlighted_filename = f"highlighted_{filename}"
            highlighted_path = f"uploads/{highlighted_filename}"
            # call the reusable highlighting function
            highlight_pdf(save_path, highlighted_path, phrases)
    except Exception as e:
        # don't break the user flow if highlighting fails; log to console
        print("Highlighting failed:", e)

    # pass the filename to the template so url_for('uploaded_file', filename=...) works
    # prefer to show the highlighted file when available
    pdf_to_show = highlighted_filename or filename
    return render_template("display_html.html", response=response, pdf_filename=pdf_to_show)


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    # serve files from the uploads directory
    return send_from_directory('uploads', filename)

@app.route("/game")
def game():
    return render_template("game_html.html")


@app.route("/cashflow")
def cashflow():
    return render_template("cash-flow-tracker.html")


@app.route("/contractconsultant")
def contractconsultant():
    return render_template("upload_html.html")
@app.route('/home/')
@app.route('/home/<username>')
def home(username=None):
    # username may be None when url_for('home') is used without values
    return render_template("home_index.html", username=username)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))




if __name__ == "__main__":
    app.run(debug=True)

