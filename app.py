from flask import Flask, request, jsonify
from datetime import date, timedelta
from dateutil import rrule
from calendar_adapter import get_public_holidays

app = Flask(__name__)

MAX_CONSECUTIVE_WORKING_DAYS = 10

def calculate_working_days(start_date: date, end_date: date) -> int:
    """
    Calculates the number of consecutive working days between two dates,
    excluding weekends and public holidays.
    """
    if start_date > end_date:
        return 0

    public_holidays = get_public_holidays(start_date, end_date)
    working_days_count = 0

    # Iterate through each day in the range
    for dt in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):
        current_date = dt.date()
        # Check if it's a weekend (Saturday = 5, Sunday = 6)
        if current_date.weekday() >= 5:
            continue
        # Check if it's a public holiday
        if current_date in public_holidays:
            continue
        working_days_count += 1
    return working_days_count

@app.route('/api/leave-requests', methods=['POST'])
def submit_leave_request():
    # Handle cases where JSON is missing or malformed (e.g., wrong Content-Type)
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    
    # Handle empty JSON or missing data
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON payload"}), 400

    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')

    if not start_date_str or not end_date_str:
        return jsonify({"error": "Missing start_date or end_date in JSON payload"}), 400

    try:
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."}), 400

    if start_date > end_date:
        return jsonify({"error": "Start date cannot be after end date."}), 400

    consecutive_working_days = calculate_working_days(start_date, end_date)

    if consecutive_working_days > MAX_CONSECUTIVE_WORKING_DAYS:
        return jsonify({
            "error": f"Your leave request exceeds the maximum allowed {MAX_CONSECUTIVE_WORKING_DAYS} consecutive working days. Please adjust your dates."
        }), 400
    else:
        # In a real application, you would save the leave request to a database here.
        # For this exercise, we just return a success message.
        return jsonify({
            "message": "Leave request submitted successfully.",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "consecutive_working_days": consecutive_working_days
        }), 200

if __name__ == '__main__':
    app.run(debug=True)
