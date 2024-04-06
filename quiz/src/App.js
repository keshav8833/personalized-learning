


import React from 'react';
import { BrowserRouter as Router, Routes , Route } from 'react-router-dom';
import UploadForm from './UploadForm';
import QuizzesPage from './QuizzesPage';

function App() {
    return (
        <Router>
            <Routes>
                <Route exact path="/" element={<UploadForm />} />
                <Route path="/quizzes" element={<QuizzesPage />} />
            </Routes>
        </Router>
    );
}

export default App;
