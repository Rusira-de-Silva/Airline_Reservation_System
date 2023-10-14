import React, { useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import "./passengersByType.css";
import { UserMenuGlobalState } from "../../Layout/UserMenuGlobalState";


function PassengersByType() {
  const BaseURL = process.env.REACT_APP_BACKEND_API_URL;

  const { setUserMenuItem } = UserMenuGlobalState();
  const [to, setTo] = useState("");
  const [from, setFrom] = useState("");

  const [response, setResponse] = useState([]);

  function handleBackClick() {
    setUserMenuItem("profile-details");
  }

  async function handleViewClick() {
    const token = Cookies.get("access-token");

    console.log(
      `${BaseURL}/admin/bookings-by-ptype?fromDate=${from}&toDate=${to}`
    );

    try {
      const response = await axios.get(
        `${BaseURL}/admin/bookings-by-ptype?fromDate=${from}&toDate=${to}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      console.log(response.data);
      setResponse(response.data);
    } catch (error) {
      console.error(error);
    }
  }
  return (
    <div className="outer-box">
      <span className="view-by-date-dest">View Passenger By Date & Type</span>
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
      </div>
      <div className="inner-box">
        {response.length ? (
          <div style={{ overflow: "auto", width: "100%" }}>
            <table>
              <thead>
                <tr>
                  <th>Passenger Type</th>
                  <th>Bookings Count</th>
                </tr>
              </thead>
              <tbody>
                {response.map((item) => (
                  <tr key={item.passengerType}>
                    <td>{item.passengerType}</td>
                    <td>{item.bookingsCount}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="no-passengers">
            Select From and To dates and click View
          </div>
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

export default PassengersByType;