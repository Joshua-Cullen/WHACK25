from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def compute(limit, balance, apr_percent, extras):
    try:
        limit = float(limit)
        balance = float(balance)
        apr = float(apr_percent) / 100.0  # use this for calculations
        apr_float = float(apr_percent)    # use this for display/rounding
    except Exception:
        raise ValueError("Invalid numeric input")

    monthly_rate = apr / 12.0
    monthly_interest = balance * monthly_rate
    utilization = None
    if limit > 0:
        utilization = balance / limit

    hacks = []
    for e in extras:
        try:
            extra = max(0.0, float(e))
        except Exception:
            extra = 0.0
        new_balance = max(0.0, balance - extra)
        new_month_interest = new_balance * monthly_rate
        saved_month = monthly_interest - new_month_interest
        saved_year = saved_month * 12
        hacks.append({
            'extra': round(extra, 2),
            'new_balance': round(new_balance, 2),
            'saved_month': round(saved_month, 2),
            'saved_year': round(saved_year, 2)
        })

    return {
        'monthly_interest': round(monthly_interest, 2),
        'utilization': round(utilization, 3) if utilization is not None else None,
        'apr': round(apr_float, 2),  # convert string to float first
        'hacks': hacks
    }

@app.route('/')
def index():
    return render_template("index_3.html")

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json() or {}
    limit = data.get('limit', 0)
    balance = data.get('balance', 0)
    apr = data.get('apr', 0)
    extras = data.get('extras', [])

    try:
        result = compute(limit, balance, apr, extras)
    except ValueError:
        return jsonify({'error': 'Invalid input'}), 400

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)



