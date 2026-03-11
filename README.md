# Max-Leave

This repository contains the implementation for the "Implement Maximum Consecutive Leave Limit for Employees" feature, corresponding to Jira issue SCRUM-35.

## Project Overview

The goal of this project is to ensure that employees cannot submit leave requests exceeding a maximum of 10 consecutive working days. The system will validate leave requests, excluding weekends and company-defined public holidays from the consecutive day count. It provides API enforcement of this limit and aims for clear user feedback.

## Architecture

The project follows a layered architecture with a focus on a backend API service.

- **Frontend (Out of Scope for this implementation):** User interface for submitting leave requests.
- **Backend (Leave Management Service):** A Flask application responsible for:
    - Receiving leave requests.
    - Validating the consecutive working days against the 10-day limit.
    - Interacting with a Calendar Service Adapter to get public holidays.
    - Returning appropriate success or error responses.
- **Calendar Service Adapter:** An abstraction layer to provide public holiday data. For this implementation, it's a simple Python module with hardcoded holidays. In a production environment, this would integrate with a database or external calendar API.
- **Data Layer (Out of Scope for this implementation):** Database for storing leave requests and public holidays.

## Getting Started

### Prerequisites

- Python 3.8+
- `pip` (Python package installer)
- `git`

### Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/p67428378-afk/Max-Leave.git
   cd Max-Leave
   ```

2. **Switch to the feature branch:**
   ```bash
   git checkout ISSUE-SCRUM-35
   ```

3. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

To run the Flask application:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development # For development mode, enables debugger and reloader
flask run
```

The application will typically run on `http://127.0.0.1:5000/`.

### API Endpoints

#### `POST /api/leave-requests`

Submits a new leave request and validates it against the consecutive working day limit.

**Request Body (JSON):**

```json
{
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD"
}
```

**Example Request (using `curl`):**

```bash
# Valid request (e.g., 10 working days)
curl -X POST -H "Content-Type: application/json" \
     -d '{"start_date": "2023-10-23", "end_date": "2023-11-03"}' \
     http://127.0.0.1:5000/api/leave-requests

# Invalid request (e.g., 11 working days)
curl -X POST -H "Content-Type: application/json" \
     -d '{"start_date": "2023-10-23", "end_date": "2023-11-06"}' \
     http://127.00.1:5000/api/leave-requests
```

**Example Responses:**

- **Success (HTTP 200 OK):**
  ```json
  {
      "message": "Leave request submitted successfully.",
      "start_date": "2023-10-23",
      "end_date": "2023-11-03",
      "consecutive_working_days": 10
  }
  ```

- **Validation Error (HTTP 400 Bad Request):**
  ```json
  {
      "error": "Your leave request exceeds the maximum allowed 10 consecutive working days. Please adjust your dates."
  }
  ```

- **Invalid Date Format Error (HTTP 400 Bad Request):**
  ```json
  {
      "error": "Invalid date format. Please use YYYY-MM-DD."
  }
  ```

## Technical Details

### Consecutive Working Day Calculation

The `calculate_working_days` function in `app.py` determines the number of consecutive working days by:
1. Iterating through each day from `start_date` to `end_date`.
2. Checking if the day is a weekend (Saturday or Sunday).
3. Checking if the day is present in the list of public holidays provided by `calendar_adapter.py`.
4. Incrementing the count only for non-weekend and non-holiday days.

### Public Holidays

The `calendar_adapter.py` module currently provides a hardcoded list of public holidays. For a real-world application, this would be replaced by a more dynamic solution, such as:
- Fetching from a dedicated public holiday database.
- Integrating with an external calendar API (e.g., Google Calendar API).
- Reading from a configurable source (e.g., YAML file, environment variable).

## Docker

A `Dockerfile` is provided to containerize the application.

### Build the Docker image

```bash
docker build -t max-leave-app .
```

### Run the Docker container

```bash
docker run -p 5000:5000 max-leave-app
```

The application will then be accessible via `http://localhost:5000`.
