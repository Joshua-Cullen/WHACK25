from flask import Flask, render_template, request, redirect
from gemini import queryGemini
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index_pdf_analyser.html")

@app.route("/submit", methods=["POST"])
def submit():
    pdf = request.files["file"]
    pdf.save(f"uploads/{pdf.filename}")

    response = queryGemini(pdf.filename)
    response = json.loads(response)

    return render_template("response.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)


