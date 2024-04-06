import React, { useState, useEffect } from 'react';
import axios from 'axios';

function QuizzesPage() {
    const [quizzes, setQuizzes] = useState([]);

    useEffect(() => {
        fetchQuizzes();
    }, []);
    const fetchQuizzes = async () => {
        try {
            const response = await axios.get('http://localhost:5000/quizzes');
            setQuizzes(response.data.quizzes);
        } catch (error) {
            console.error('Error fetching quizzes:', error);
        }
    };

    return (
        <div>
            <h1>Quizzes</h1>
            <ul>
                {quizzes.map(quiz => (
                    <li key={quiz.id}>
                        PDF File: {quiz.pdf_file}<br />
                        Difficulty: {quiz.difficulty_level}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default QuizzesPage;
