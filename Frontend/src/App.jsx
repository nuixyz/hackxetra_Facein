import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [data, setData] = useState([]);

  // Fetch data from Flask API
  useEffect(() => {
    axios.get('http://127.0.0.1:5000/chayan')
      .then(response => {
        setData(response.data);  // Set the list received from the backend
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  return (
    <div>
      <h1>Data from Flask Backend</h1>
      <ul>
        {data.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
