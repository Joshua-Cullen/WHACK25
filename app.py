from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

# Folder to store uploaded PDFs
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("upload_html.html")

@app.route("/submit", methods=["POST"])
def submit():
    pdf = request.files.get("file")
    if not pdf:
        return "No file selected", 400

    # Save uploaded file
    save_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
    pdf.save(save_path)

    # Redirect to display page with uploaded PDF
    return render_template(
        "display_noAI.html",
        pdf_filename=pdf.filename
    )

# Route to serve uploaded PDFs
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
