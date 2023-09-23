# REST API CAPABLE OF CRUD OPERATIONS
This is a simple Flask application that allows you to perform CRUD operations on a "people" resource using SQLite as the database.

## Getting Started
### Prerequisites
* Python 311
* Flask
* SQLite

### Installing dependencies
1. Create a virtual enviroment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

2. Install dependencies:
```bash
pip install Flask
```

### Running the Application
```bash
python app.py
```
The application will be running at http://localhost:5000.

## Usage
### API Endpoints
* GET /people: Get a list of all people.
* GET /people/<person_id>: Get details of a specific person.
* POST /people: Create a new person.
* PUT /people/<person_id>: Update an existing person.
* DELETE /people/<person_id>: Delete a person.

### Request Format
All data must be sent in JSON format. Here's an example of a JSON request body for creating a new person:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```

### Response Format
Responses will be in JSON format. For example, a successful response for creating a person will look like:
```json
{
  "message": "Person created successfully"
}
```

## Database
The application uses SQLite as the database. The database file is database.db.

## Additional Notes
* Make sure to handle database connections properly to prevent potential resource leaks.
* This is a simple example and might require additional features and error handling for production use.
