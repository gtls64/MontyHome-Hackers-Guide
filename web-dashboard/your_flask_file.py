from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)

# API endpoint to fetch the last 10 JSON data entries
@app.route('/api/data', methods=['GET'])
def get_data():
    if os.path.exists('ble_responses.json'):
        with open('ble_responses.json', 'r') as f:
            all_data = json.load(f)
        # Get the last 10 entries only
        last_10_data = all_data[-10:] if all_data else []
    else:
        last_10_data = []
    return jsonify(last_10_data)

# Webpage route
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
