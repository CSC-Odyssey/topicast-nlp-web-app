import React, { useState, useEffect } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import axios from "axios";
import Card from "./components/Card";

import logo from './assets/topicast_logo.png';

const App = () => {
  const [checkbox1, setCheckbox1] = useState(false);
  const [checkbox2, setCheckbox2] = useState(false);
  const [textInput, setTextInput] = useState("");

  const [processing, setProcessing] = useState(false);

  const [selectedDate, setSelectedDate] = useState(null);

  const [data, setData] = useState(null);

  const HandleSubmit = (e) => {
    e.preventDefault();
    setProcessing(true);
    axios.post("/api/retrieve_topics", {
      checkbox1: checkbox1,
      checkbox2: checkbox2,
      selectedDate: selectedDate.toLocaleDateString()
    })
      .then(response => {
        console.log(response.data);
        setData(response.data);
        setProcessing(false);
        console.log(data)
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
          dateFormat='yyyy-MM-dd'
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

      {data && (
        <div className="flex flex-col mt-5">
          <div className="flex flex-wrap justify-center">
            {Object.keys(data).map((topic, index) => (
              <Card key={index} title={topic} words={data[topic]} />
            ))}
          </div>
        </div>
      )}

      {/* Modal to display "processing data" message */}
      {processing && (
        <div className="fixed z-10 inset-0 overflow-y-auto pt-8">
          <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity">
              <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>

            <div
              className="inline-block align-middle bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:align-middle sm:max-w-lg sm:w-full"
            >
              <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <p className="text-sm leading-5 font-medium text-gray-900">
                  Processing data...
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};

export default App;