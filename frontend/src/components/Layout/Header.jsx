import NavBar from "./NavBar";
import "./header.css";
import { Link } from "react-router-dom";
import { UserGlobalState } from '../Layout/UserGlobalState';

export default function Header () {
    const { currentUserData, setCurrentUserData} = UserGlobalState();

    const logout = () => {
        setCurrentUserData({
            'username': null,
            'firstName': null,
            'lastName': null,
            'isAdmin': null,
            'isDataEntryOperator': null,
            'bookingsCount': null,
            'category': null
        });
    }

    return (
        <div>
            <div className="logo">
                <Link to="/" style={{ textDecoration: 'none' }}>
                    <img src={require('../../images/Logo.png')} alt="logo" className="logoImg"/>
                </Link>
            </div>
            <div className="navBarContainer">
                <NavBar />
            </div>
            <div className="profile-btns">
                <Link to="/profile" style={{ textDecoration: 'none' }}>
                    <button className="profile-btn">{ currentUserData.username ? 'Profile' : 'Log in'}</button>
                </Link>
                { currentUserData.username &&
                    <button className="profile-btn" onClick={logout}>Log Out</button>}
            </div>
        </div>
    );
};
