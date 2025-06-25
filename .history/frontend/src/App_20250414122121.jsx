import { useState } from "react";
import React from "react";
import axios from "axios";

function App() {
  const [inputData, setInputData] = useState("");
  const [prediction, setPrediction] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", {
        input: inputData,
      });
      setPrediction(response.data.prediction);
    } catch (error) {
      console.error("Error fetching prediction:", error);
    }
  };

  return (
    <div>
      <h1>Product Recommendation</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputData}
          onChange={(e) => setInputData(e.target.value)}
          placeholder="Enter product details"
        />
        <button type="submit">Get Recommendation</button>
      </form>

      {prediction && (
        <div>
          <h2>Recommendation:</h2>
          <p>{prediction}</p>
        </div>
      )}
    </div>
  );
}

export default App;
