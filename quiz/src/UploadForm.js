import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate hook
import './UploadForm.css'; // Import CSS file for styling

function UploadForm() {
  const [fileName, setFileName] = useState('No file uploaded');
  const [difficultyLevel, setDifficultyLevel] = useState('');
  const [fileSelected, setFileSelected] = useState(false); // State to track if a file is selected
  const navigate = useNavigate(); // Initialize useNavigate hook

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFileName(file.name);
      setFileSelected(true);
    } else {
      setFileName('No file uploaded');
      setFileSelected(false);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file) {
      setFileName(file.name);
      setFileSelected(true);
    } else {
      setFileName('No file uploaded');
      setFileSelected(false);
    }
  };

  const handleDifficultyLevelChange = (event) => {
    setDifficultyLevel(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Create a FormData object to store form data
    const formData = new FormData();
    const fileInput = document.querySelector('input[type="file"]');
    formData.append('file', fileInput.files[0]); // Append the file itself

    // Append other form data
    formData.append('difficulty', difficultyLevel);

    try {
      // Send a POST request to the server
      const response = await fetch('http://localhost:5000/submit', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data); // Log response from the server
        // Reset form fields if needed
        navigate('/quizzes'); // Navigate to QuizzesPage component using useNavigate
      } else {
        console.error('Error:', response.statusText); // Log error message
      }
    } catch (error) {
      console.error('Error:', error); // Log any errors
    }
  };

  return (
    <div className="container">
      <div className="hero">
        <h1 className='Headingg'>PDF to QUIZ Generator</h1>
        <p className="is-size-3 has-text-black has-text-weight-bold has-text-centered">Upload any Document to get an instant Quiz</p>
        <p className="is-size-4 has-text-weight-bold has-text-centered">You Know 📖, You Grow 🚀</p>
        <p className="is-size-5 has-text-black has-text-weight-medium has-text-centered"> Practice More • Learn More </p>
      </div>
      <div className="card-container">
        <div className={`card has-text-centered ${fileSelected ? 'pdf-selected' : ''}`} onDrop={handleDrop} onDragOver={(e) => e.preventDefault()}>
          <img src="https://cdn4.iconfinder.com/data/icons/files-and-folders-thinline-icons-set/144/File_PDF-512.png" alt="upload" />
          <h4 className="file-description"> Choose/Drag & Drop a file </h4>
          <form onSubmit={handleSubmit} encType="multipart/form-data">
            <div className="file has-name is-fullwidth">
              <label className="file-label">
                <input className="file-input" type="file" name="file" accept=".txt, application/pdf" onChange={handleFileChange} />
                <span className="file-cta">
                  <span className="file-icon">
                    <i className="fas fa-upload"></i>
                  </span>
                  Browse
                </span>
                <p className="file-name">{fileName}</p>
              </label>
            </div>
            <div className="difficulty-level">
              <p>Select Difficulty Level:</p>
              <label>
                <input  
                  type="radio"
                  name="difficulty"
                  value="easy"
                  checked={difficultyLevel === 'easy'}
                  onChange={handleDifficultyLevelChange}
                />
                Easy
              </label>
              <label>
                <input
                  type="radio"
                  name="difficulty"
                  value="medium"
                  checked={difficultyLevel === 'medium'}
                  onChange={handleDifficultyLevelChange}
                />
                Medium
              </label>
              <label>
                <input
                  type="radio"
                  name="difficulty"
                  value="hard"
                  checked={difficultyLevel === 'hard'}
                  onChange={handleDifficultyLevelChange}
                />
                Hard
              </label>
            </div>
            <button className="button has-text-centered is-large is-fullwidth is-dark" type="submit" name="upload file">
              <span className="submit has-text-centered">Submit</span>
              <span className="loading"><i className="fa fa-refresh"></i></span>
              <span className="check"><i className="fa fa-check"></i></span>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default UploadForm;
