import React from "react";
import { useState, useEffect } from "react";
import axios from "axios";
import "./passengersByDestination.css";

function PassengersByDestination({ setAdminMenuItem }) {
  const BaseURL = process.env.REACT_APP_BACKEND_API_URL;

  const [airportsList, setAirportsList] = useState([]);
  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");
  const [destination, setDestination] = useState("destination");
  const [passengersCount, setPassengersCount] = useState({});

  useEffect(
    function () {
      async function getAirportsList() {
        try {
          const response = await axios.get(`${BaseURL}/get/airports`);
          console.log(response.data);
          setAirportsList(response.data);
        } catch (error) {
          console.log(error);
        }
      }
      getAirportsList();
    },
    [BaseURL]
  );

  function handleBackClick() {
    setAdminMenuItem("profile-details");
  }

  async function handleViewClick() {
    const token = "<Access-Token>";
    console.log(
      `${BaseURL}/admin/passengers-to-destination?fromDate=${from}&toDate=${to}&toAirport=${destination}`
    );

    try {
      const response = await axios.get(
        `${BaseURL}/admin/passengers-to-destination?fromDate=${from}&toDate=${to}&toAirport=${destination}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      console.log(response.data);
      setPassengersCount(response.data);
    } catch (error) {
      console.error(error);
    }
  }
  
  return (
    <div className="outer-box">
      <span className="view-by-date-dest">
        View Passengers by Date & Destination
      </span>
      <div className="selection-box">
        <div className="date-selection">
          <label className="from" htmlFor="start-date-input">
            From
          </label>
          <input
            id="start-date-input"
            className="model-selection"
            type="date"
            name="start-date"
            min="2023-10-01"
            max="2023-12-31"
            value={from}
            onChange={(e) => setFrom(e.target.value)}
          />
        </div>
        <div className="date-selection">
          <label className="to" htmlFor="end-date-input">
            To
          </label>
          <input
            id="end-date-input"
            className="model-selection"
            type="date"
            name="end-date"
            min="2023-10-01"
            max="2023-12-31"
            value={to}
            onChange={(e) => setTo(e.target.value)}
          />
        </div>

        <select
          value={destination}
          onChange={(e) => setDestination(e.target.value)}
          className="model-selection"
          placeholder="Destination"
        >
          <option className="model-option" value="destination" disabled>
            Destination
          </option>
          {airportsList.map((airport) => (
            <option
              className="model-option"
              value={airport.icaoCode}
              key={airport.icaoCode}
            >
              {airport.city} ({airport.iataCode})
            </option>
          ))}
        </select>
      </div>
      <div className="inner-box">
        {passengersCount ? (
          <div className="no-passengers">
            Select From Date, To Date and Destination Airport and click View
          </div>
        ) : (
          <input disabled type="text" value={passengersCount.passengersCount} />
        )}
      </div>
      <div className="buttons-div">
        <button onClick={handleBackClick} className="buttons">
          Back
        </button>
        <button onClick={handleViewClick} className="buttons">
          View
        </button>
      </div>
    </div>
  );
}

export default PassengersByDestination;
