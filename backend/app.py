# from flask import Flask, request, jsonify
# # import mysql.connector
# from flask_cors import CORS
# import os
# import tempfile
# import openai 
# import random   
# import tempfile
# from pdfminer.high_level import extract_text


# openai.api_key = os.getenv("OPENAI_API_KEY")
# app = Flask(__name__)
# CORS(app)
# # Define the MySQL connection details
# # mydb = mysql.connector.connect(
# #     host="localhost",
# #     user="Keshav",
# #     password="keshav772970",
# #     database="pdfreader"
# # )

# # Route to handle form submission


# def generate_question(text, difficulty, q_type):
#     """
#     Generates a question based on the text, difficulty, and question type (MCQ/Descriptive).
#     """
#     # This is a placeholder. In practice, you would use a model to generate a question
#     # based on the text and difficulty level, then format it according to q_type.
    
#     if q_type == "mcq":
#         question = "What is the main topic discussed?"
#         options = ['Option A: Topic A', 'Option B: Topic B', 'Option C: Topic C', 'Option D: Topic D']
#         correct_option = random.choice(options)
#         return f"{question}\n" + "\n".join(options) + f"\nCorrect Answer: {correct_option}"
#     elif q_type == "descriptive":
#         questions = [
#             "Easy Question: Describe the importance of the main topic.",
#             "Medium Question: Explain how the main topic affects related topics.",
#             "Hard Question: Analyze the implications of the main topic on future developments."
#         ]
#         if difficulty == "easy":
#             return questions[0]
#         elif difficulty == "medium":
#             return questions[1]
#         elif difficulty == "hard":
#             return questions[2]
#     return "Unable to generate question."

# def query_text_with_question(extracted_text, question):
#     """
#     Use the extracted text and the generated question to query for an answer.
#     This function simplifies the call to an NLP model. You might need to adjust
#     the prompt or use a specific API endpoint depending on your model.
#     """
#     response = openai.Completion.create(
#         engine="davinci",  # Choose an appropriate engine for your task
#         prompt=f"{extracted_text}\n\nQuestion: {question}\nAnswer:",
#         temperature=0.5,
#         max_tokens=150,
#         stop=["\n"],
#     )
#     return response.choices[0].text.strip()





# @app.route('/submit', methods=['POST'])
# def submit_form():
#     pdf_file = request.files['file']
#     difficulty_level = request.form['difficulty']
#     question_type = "descriptive"
    
#     temp_dir = tempfile.mkdtemp()
#     pdf_path = os.path.join(temp_dir, pdf_file.filename)
#     pdf_file.save(pdf_path)
#     extracted_text = extract_text(pdf_path)
#     # answer = query_text_with_question(extracted_text, generated_question)


#     # Create a MySQL cursor
#     # mycursor = mydb.cursor()

#     # Insert data into the database
#     # sql = "INSERT INTO quizzes (pdf_file, difficulty_level) VALUES (%s, %s)"
#     # val = (pdf_file, difficulty_level)
#     # mycursor.execute(sql, val)
#     # mydb.commit()


#     generated_question = generate_question(extracted_text, difficulty_level, question_type)

#     os.remove(pdf_path)
#     os.rmdir(temp_dir)


#     print(jsonify({'generated_question': generated_question}))

#     return jsonify({'message': 'Form submitted successfully'})


# # @app.route('/quizzes', methods=['GET'])
# # def get_quizzes():
# #     # Create a MySQL cursor
# #     mycursor = mydb.cursor()

# #     # Retrieve data from the database
# #     mycursor.execute("SELECT * FROM quizzes")
# #     quizzes = mycursor.fetchall()

# #     quiz_data = []
# #     for quiz in quizzes:
# #         quiz_data.append({
# #             'id': quiz[0],
# #             'pdf_file': 'PDF file (BLOB)',
# #             'difficulty_level': quiz[2]
# #         })
# #     return jsonify({'quizzes': quiz_data})  

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request, jsonify
# import mysql.connector
from flask_cors import CORS
import os
import tempfile
import openai 
import random   
import json  # Add this import statement
from pdfminer.high_level import extract_text
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator

openai.api_key = os.getenv("")
app = Flask(__name__)
CORS(app)

def generate_question(text, difficulty, q_type):
    if q_type == "mcq":
        question = "What is the main topic discussed?"
        options = ['Option A: Topic A', 'Option B: Topic B', 'Option C: Topic C', 'Option D: Topic D']
        correct_option = random.choice(options)
        return f"{question}\n" + "\n".join(options) + f"\nCorrect Answer: {correct_option}"
    elif q_type == "descriptive":
        questions = [
            "Easy Question: Describe the importance of the main topic.",
            "Medium Question: Explain how the main topic affects related topics.",
            "Hard Question: Analyze the implications of the main topic on future developments."
        ]
        if difficulty == "easy":
            return questions[0]
        elif difficulty == "medium":
            return questions[1]
        elif difficulty == "hard":
            return questions[2]
    return "Unable to generate question."

# def query_text_with_question(extracted_text, question):
#     response = openai.Completion.create(
#         engine="davinci",  
#         prompt=f"{extracted_text}\n\nQuestion: {question}\nAnswer:",
#         temperature=0.5,
#         max_tokens=150,
#         stop=["\n"],
#     )
#     return response.choices[0].text.strip()

@app.route('/submit', methods=['POST'])
def submit_form():
    pdf_file = request.files['file']
    difficulty_level = request.form['difficulty']
    question_type = "descriptive"
    
    temp_dir = tempfile.mkdtemp()
    pdf_path = os.path.join(temp_dir, pdf_file.filename)
    pdf_file.save(pdf_path)
    # extracted_text = extract_text(pdf_path)
    loader = UnstructuredPDFLoader(pdf_path)
    index = VectorstoreIndexCreator().from_loaders([loader])
    query = "generate some descriptive questions with a proper thought process needed to solve it and also give the answer"
    response = index.query(query)
    # generated_question = generate_question(extracted_text, difficulty_level, question_type)

    # answer = query_text_with_question(extracted_text, generated_question)  # Corrected this line

    os.remove(pdf_path)
    os.rmdir(temp_dir)

    # Return generated question and answer
    print({'query': query})
    print({'response': response})
    return jsonify({'generated_question': generated_question})

if __name__ == '__main__':
    app.run(debug=True)

