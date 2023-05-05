import React, { useState, useEffect } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import axios from "axios";

import logo from './assets/topicast_logo.png';

const App = () => {
  const [checkbox1, setCheckbox1] = useState(false);
  const [checkbox2, setCheckbox2] = useState(false);
  const [textInput, setTextInput] = useState("");

  const [selectedDate, setSelectedDate] = useState(null);

  const [data, setData] = useState([]);

  const HandleSubmit = (e) => {
    e.preventDefault();
    axios.post("/api/retrieve_topics", {
      checkbox1: checkbox1,
      checkbox2: checkbox2
    })
      .then(response => {
        console.log(response.data);
        setData(response.data);
      })
      .catch(error => {
        console.log(error);
      });
  };

  return (
    <div className="flex flex-col justify-center items-center p-5">
      <div className="flex flex-row justify-center">
        <img className="h-80 w-90" src={logo} alt="" />
      </div>
      <div className="flex flex-col bg-gray-100 mb-5 border-1 border-t-8 border-t-cyan-300 rounded-lg py-12 px-20 mt-5">
        <span className="ml-2 text-lg text-gray-700 font-semibold mb-10 right-5">Tick news sources you want to include.</span>
        <div className="flex flex-col ml-10">
          <label className="inline-flex items-center">
            <input
              type="checkbox"
              className="form-checkbox h-7 w-7 m-4 text-green-500"
              checked={checkbox1}
              onChange={(e) => setCheckbox1(e.target.checked)}
            />
            <span className="ml-2 text-xl text-gray-700 font-semibold">MidlandCourier</span>
          </label>
          <label className="inline-flex items-center">
            <input
              type="checkbox"
              className="form-checkbox h-7 w-7 m-4 text-green-500"
              checked={checkbox2}
              onChange={(e) => setCheckbox2(e.target.checked)}
            />
            <span className="ml-2 text-xl text-gray-700 font-semibold">Baguio News</span>
          </label>
        </div>

      </div>
      <div className="flex items-center mb-5">
        <DatePicker
          className="border border-gray-400 p-2 rounded-md text-gray-600"
          selected={selectedDate}
          onChange={(date) => setSelectedDate(date)}
          placeholderText="Select a date"
        />
      </div>
      <div className="flex flex-row justify-center w-full">
        <button
          className="bg-green-500 hover:bg-green-700 text-white h-22 w-1/6 font-bold py-5 px-4 rounded-lg text-2xl"
          onClick={HandleSubmit}
        >
          Submit
        </button>
        {/* <button className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-full mr-4 h-35 w-40 text-2xl">
          Idk
        </button> */}
      </div>
      <div className="flex flex-col mt-5">
        {(typeof data.message === "undefined") ? (
          <p>Loading...</p>
        ) : (
          <p>{data.message}</p>
        )}
      </div>
    </div>
  );
};

export default App;