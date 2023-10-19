import React from "react";
import { UserGlobalState } from "../Layout/UserGlobalState";
import { useState, useEffect } from "react";
import axios from "axios";
import "../Profile/RegisteredUser/userProfile.css";

function GuestBookedTickets({ guestID }) {
  const BaseURL = process.env.REACT_APP_BACKEND_API_URL;

  const { setCurrentUserData } = UserGlobalState();
  const [bookedTickets, setBookedTickets] = useState([]);

  useEffect(
    function () {
      async function getBookedTickets() {
        try {
          const response = await axios.get(
            `${BaseURL}/tickets/guest/search?guestID=${guestID}`
          );
          console.log(response.data);
          setBookedTickets(response.data);
        } catch (error) {
          console.log(error);
          if (error.response && error.response.status === 401) {
            setCurrentUserData({
              username: null,
              firstName: null,
              lastName: null,
              isAdmin: null,
              isDataEntryOperator: null,
              bookingsCount: null,
              category: null,
            });
          }
        }
      }
      getBookedTickets();
    },
    [BaseURL, guestID, setCurrentUserData]
  );

  return (
    <div className="profileDetailsWrapper">
      <h1 className="user-header">Booked Tickets</h1>
      <div style={{ height: "375px", overflow: "auto", width: "100%" }}>
        {bookedTickets.length ? (
          <table className="user-table">
            <thead className="user-thead">
              <tr className="user-tr">
                <th className="user-th">Ticket Number</th>
                <th className="user-th">Passenger</th>
                <th className="user-th">Passport ID</th>
                <th className="user-th">From</th>
                <th className="user-th">To</th>
                <th className="user-th">Seat</th>
                <th className="user-th">Class</th>
                <th className="user-th">Depature Date</th>
                <th className="user-th">Depature Time</th>
              </tr>
            </thead>
            <tbody className="user-tbody">
              {bookedTickets.map((ticket) => (
                <tr className="user-tr" key={ticket.ticketNumber}>
                  <td className="user-td">{ticket.ticketNumber}</td>
                  <td className="user-td">{ticket.passenger}</td>
                  <td className="user-td">{ticket.passportID}</td>
                  <td className="user-td">{ticket.from.city}</td>
                  <td className="user-td">{ticket.to.city}</td>
                  <td className="user-td">{ticket.seat}</td>
                  <td className="user-td">{ticket.class}</td>
                  <td className="user-td">{ticket.departureDate}</td>
                  <td className="user-td">{ticket.departureTime}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <h4 className="loading-text">Loading Details Please Wait....</h4>
        )}
      </div>
    </div>
  );
}

export default GuestBookedTickets;