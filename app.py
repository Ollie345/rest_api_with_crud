from flask import Flask, request, jsonify, g
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

# this block of code allows connects to database
# create a function to get the database connection


def get_db():
 # Get the database connection from the global object
    db = getattr(g, '_database', None)
# If the connection is not available, create a new one
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    # Makes sure that all fetches return a dictionary
    db.row_factory = sqlite3.Row

    # Initial table setup if table does not exist
    cursor = db.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS people (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT)')
    db.commit()

    # Return the database connection
    return db


# This block of code closes the database connection after each request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)

# if the connection exists, close the connection to the database
    if db is not None:
        db.close()


# This block of code implements routes and functions to retrieve information about a list of people.
@app.route('/people', methods=['GET'])
def get_people():
    # Get a connection to the database
    connection = get_db()
    cursor = connection.execute('SELECT * FROM people')

    # Fetch all the rows from the 'people' table
    people = cursor.fetchall()

    # Close the cursor to free up resources
    cursor.close()

    # converting the result to a python dictionary instead of an array
    result = [dict(person) for person in people]

    # Return the people data as a JSON response
    return jsonify(result)


# This block of code Implements routes and functions to retrieves information about a person by their ID


@app.route('/people/<int:person_id>', methods=['GET'])  # mapping the url
# a function that will be called whenever a get request is made to the above url
def get_person(person_id):
    # sending an sql query to the database
    connection = get_db()
    cursor = connection.execute("SELECT * FROM people where id=?",
                                (person_id,))

    # fetch the next row from the 'people' table
    person = cursor.fetchone()
    cursor.close()

    if person is None:
        return jsonify({"message": "Person does not exist"}), 404

    # return jsonify as a dict instead of an array
    return jsonify(dict(person))

# This block of code below implements a route and function to create a new person


@app.route('/people', methods=['POST'])
def create_person():
    # converts the POST request in JSON format of the person's details into a python dictionary
    data = request.json
    connection = get_db()

    # The database is connected and SQL commands are executed to insert the person's details into the database.
    cursor = connection.execute('INSERT INTO people(first_name, last_name, email) VALUES(?,?,?)',
                                (data['first_name'], data['last_name'], data['email']))

    # saves changes made the above line of code
    connection.commit()
    cursor.close()
    return jsonify({'message': 'Person created successfully'}), 201


# Setting up a path for updating an existing person's details
@app.route('/people/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    # Converting the JSON data sent with the PUT request into a Python dictionary, ensuring it contains the updated person's details.
    data = request.json
    connection = get_db()

    # The line connects to the database using the connection function and executes an SQL command to update a row in the 'people' table with the same ID.
    cursor = connection.execute('UPDATE people SET first_name=? ,last_name=?, email=? WHERE id=?',
                                (data['first_name'], data['last_name'], data['email'], person_id))

    # This line tells the database to save the changes made by the previous line.
    connection.commit()
    cursor.close()

    # The line sends a JSON response to the PUT request recipient, indicating successful update and a standard 'OK' status code of '200'.
    return jsonify({'message': 'Person updated successfully!!!'}), 200


# Route to DELETE a person by their ID
@app.route("/people/<int:person_id>", methods=['DELETE'])
def delete_person(person_id):
    connection = get_db()

    # establishing a connection to the database and using an sql query  to delete a person usind their ID
    cursor = connection.execute("DELETE FROM people WHERE id=?", (person_id,))
    # saves changes
    connection.commit()
    cursor.close()

    # returns jsonify as a 200 OK http status code
    return jsonify({'message': 'Person deleted sucessfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
