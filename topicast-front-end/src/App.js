import React, { useState, useEffect } from "react";

const App = () => {
  const [checkbox1, setCheckbox1] = useState(false);
  const [checkbox2, setCheckbox2] = useState(false);
  const [checkbox3, setCheckbox3] = useState(false);
  const [textInput, setTextInput] = useState("");

  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('/api/hello').then(response =>
      response.json().then(data => {
        setData(data)
      })
  )}, []);

  const HandleSubmit = () => {
    console.log(checkbox1, checkbox2, checkbox3);

    
  };



  return (
    <div className="flex flex-col justify-center items-center">
      {/* <h1 className="text-3xl font-bold mb-5">News Sources</h1>
      <textarea
        className="border-2 border-gray-400 rounded-md w-80 h-48 p-2 mb-5"
        placeholder="Enter your text here"
        value={textInput}
      //onChange={(e) => setTextInput(e.target.value)}
      /> */}

      {(typeof data.message === "undefined") ? (
        <p>Loading...</p>
      ) : (
        data.message.map((message, i) => (
          <p key={i}>{message}</p>
        ))
      )}

      {/* <div className="flex flex-col items-start mb-5">
        <label className="inline-flex items-center">
          <input
            type="checkbox"
            className="form-checkbox h-5 w-5 text-green-500"
            checked={checkbox1}
            onChange={(e) => setCheckbox1(e.target.checked)}
          />
          <span className="ml-2 text-gray-700 font-semibold">MidlandCourier</span>
        </label>
        <label className="inline-flex items-center">
          <input
            type="checkbox"
            className="form-checkbox h-5 w-5 text-green-500"
            checked={checkbox2}
            onChange={(e) => setCheckbox2(e.target.checked)}
          />
          <span className="ml-2 text-gray-700 font-semibold">Philstar</span>
        </label>
        <label className="inline-flex items-center">
          <input
            type="checkbox"
            className="form-checkbox h-5 w-5 text-green-500"
            checked={checkbox3}
            onChange={(e) => setCheckbox3(e.target.checked)}
          />
          <span className="ml-2 text-gray-700 font-semibold">Baguio News</span>
        </label>
      </div> */}
      <div className="flex flex-row justify-center">
        <button
          className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-full mr-4"
          onClick={HandleSubmit}
        >
          Submit
        </button>
        <button className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-full">
          Close
        </button>
      </div>
    </div>
  );
};

export default App;