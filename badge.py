from flask import Flask, render_template, jsonify
from flask_cors import CORS

# Use chatgpt or something to fix this code if it's wrong, and also need some code in html as well, again use ai to do this.

app = Flask(__name__)
CORS(app)

# Keep track of plays for the badge system
plays = 0

@app.route('/')
def index():
    return render_template("game_update_html.html")

@app.route('/play', methods=['POST'])
def play():
    global plays
    plays += 1
    badge = None
    if plays == 5:
        badge = "Bronze"
    elif plays == 10:
        badge = "Silver"
    elif plays == 20:
        badge = "Gold"
    elif plays == 50:
        badge = "Platinum"
    elif plays == 100:
        badge = "Diamond"
    return jsonify({"plays": plays, "badge": badge})

if __name__ == '__main__':
    app.run(debug=True)

