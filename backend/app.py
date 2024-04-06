from flask import Flask, request, jsonify
import mysql.connector
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# Define the MySQL connection details
mydb = mysql.connector.connect(
    host="localhost",
    user="Keshav",
    password="keshav772970",
    database="pdfreader"
)

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    pdf_file = request.files['file'].read()  # Read the file content as binary data
    difficulty_level = request.form['difficulty']

    # Create a MySQL cursor
    mycursor = mydb.cursor()

    # Insert data into the database
    sql = "INSERT INTO quizzes (pdf_file, difficulty_level) VALUES (%s, %s)"
    val = (pdf_file, difficulty_level)
    mycursor.execute(sql, val)
    mydb.commit()

    return jsonify({'message': 'Form submitted successfully'})


@app.route('/quizzes', methods=['GET'])
def get_quizzes():
    # Create a MySQL cursor
    mycursor = mydb.cursor()

    # Retrieve data from the database
    mycursor.execute("SELECT * FROM quizzes")
    quizzes = mycursor.fetchall()

    quiz_data = []
    for quiz in quizzes:
        quiz_data.append({
            'id': quiz[0],
            'pdf_file': 'PDF file (BLOB)',
            'difficulty_level': quiz[2]
        })
    return jsonify({'quizzes': quiz_data})  

if __name__ == '__main__':
    app.run(debug=True)
