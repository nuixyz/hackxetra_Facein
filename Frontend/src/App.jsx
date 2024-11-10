import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [users, setUsers] = useState([]);

  // Fetch data from backend
  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/api/users") // Update the URL to match the API endpoint
      .then((response) => {
        setUsers(response.data); // Set the data in state
      })
      .catch((error) => {
        console.error("There was an error fetching the data!", error);
      });
  }, []);

  return (
    <div>
      <h1>Facein</h1>
      <table>
        <thead>
          <tr>
            <th>Username</th>
            <th>Days Present</th>
            <th>Total Days</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user, index) => (
            <tr key={index}>
              <td>{user.username}</td>
              <td>{user.daysPresent}</td>
              <td>{user.totalClasses}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
