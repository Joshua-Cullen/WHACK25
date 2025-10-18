from flask import Flask, render_template, request, redirect
from gemini import queryGemini
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("upload_html.html")

@app.route("/submit", methods=["POST"])
def submit():
    pdf = request.files["file"]
    pdf.save(f"uploads/{pdf.filename}")

    response = queryGemini(pdf.filename)
    response = json.loads(response)

    return render_template("display_html.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)


