import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = () => {
    const formData = new FormData();
    formData.append("file", file);

    axios.post("http://localhost:8000/upload/", formData)
      .then((res) => alert(res.data.message))
      .catch((err) => console.error(err));
  };

  const handleQuery = () => {
    axios.post("http://localhost:8000/query/", {query: question })
      .then((res) => setAnswer(res.data.answer))
      .catch((err) => console.error(err));
  };

  return (
    <div>
      <h1>Document Q&A</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <br />
      <input
        type="text"
        placeholder="Ask a question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={handleQuery}>Ask</button>
      <p>Answer: {answer}</p>
    </div>
  );
}

export default App;