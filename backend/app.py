from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'  # SQLite database file path
db = SQLAlchemy(app)

# Define the Quiz model
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pdf_file = db.Column(db.LargeBinary)  # Store PDF file as BLOB
    difficulty_level = db.Column(db.String(10))

# Create the database tables within the application context
with app.app_context():
    db.create_all()

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    pdf_file = request.files['file'].read()  # Read the file content as binary data
    difficulty_level = request.form['difficulty']

    # Create a new Quiz object
    quiz = Quiz(pdf_file=pdf_file, difficulty_level=difficulty_level)

    # Add the object to the database
    db.session.add(quiz)
    db.session.commit()

    return jsonify({'message': 'Form submitted successfully'})


@app.route('/quizzes', methods=['GET'])
def get_quizzes():
    quizzes = Quiz.query.all()
    quiz_data = []
    for quiz in quizzes:
        quiz_data.append({
            'id': quiz.id,
            'pdf_file': 'PDF file (BLOB)',
            'difficulty_level': quiz.difficulty_level
        })
    return jsonify({'quizzes': quiz_data})  

if __name__ == '__main__':
    app.run(debug=True)
