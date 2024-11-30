from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
from datetime import timedelta, datetime

app = Flask(__name__)
CORS(app)

# Paths to the data files
hr_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/HR-data-2021-12-08 20_37_23.csv')
notes_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/notes.csv')

# Load and preprocess datasets
hr_data = pd.read_csv(hr_data_path)
notes_data = pd.read_csv(notes_data_path)

hr_data.dropna(inplace=True)
hr_data['Date'] = pd.to_datetime(hr_data['Time']).dt.date
hr_data['Time'] = pd.to_datetime(hr_data['Time']).dt.time

notes_data['mood'] = notes_data['mood'].str.strip()
notes_data['emojis'] = notes_data['mood'].map({
    'happy': '😃', 'content': '🙂', 'neutral': '😐', 'sad': '☹️',
    'angry': '😡', 'bored': '😒', 'tired': '😫', 'grateful': '😇',
    'stressed': '😓', 'motivated': '🧐', 'relieved': '😌', 'focused': '🤔',
    'irritated': '😩', 'relaxed': '😎', 'hopeful': '😏', 'anxious': '😰',
    'frustrated': '😖', 'inspired': '🤩', 'guilt': '🤥', 'ashamed': '😬',
    'depressed': '😥', 'indifferent': '😕'
})

# Endpoint for chart and notes data
@app.route('/data', methods=['GET'])

def get_data():
    date_value = request.args.get('date')
    if not date_value:
        return jsonify({"error": "Date parameter is required"}), 400

    # Filter HR data
    hr_data['Date'] = hr_data['Date'].astype(str)
    hr_data['Time'] = hr_data['Time'].astype(str)
    hr_filtered = hr_data[hr_data['Date'] == date_value]

    # Filter notes data
    notes_data['full_date'] = pd.to_datetime(notes_data['full_date'])
    notes_data['time'] = notes_data['full_date'].dt.time
    notes_data['date'] = notes_data['full_date'].dt.date.astype(str)
    notes_filtered = notes_data[notes_data['date'] == date_value]

    # Prepare chart data
    chart_data = {
        "x": (hr_filtered['Date'] + " " + hr_filtered['Time']).tolist(),
        "y": hr_filtered['Empatica.mean'].tolist(),
        "annotations": [
            {"time": row.time.strftime('%H:%M:%S'), "emoji": row.emojis}
            for _, row in notes_filtered.iterrows()
        ]
    }

    # Prepare notes data
    notes_list = [
        {
            "time": row.time.strftime('%H:%M:%S'),
            "text": row.note,
            "emoji": row.emojis,
        }
        for _, row in notes_filtered.iterrows()
    ]

    return jsonify({"chart": chart_data, "notes": notes_list})

if __name__ == '__main__':
    app.run(debug=True)
