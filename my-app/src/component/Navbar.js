import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../Styles/Navbar.css';


const Navbar = ({ handleLogout }) => {
    const location = useLocation();
    
    // Debugging: Check if handleLogout is passed correctly
    console.log("Navbar received handleLogout:", handleLogout);

    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <img src="/Page logo.png" alt="NPKnows Logo" className="navbar-logo" />
            </div>
            <div className="navbar-links">
                <Link to="/dashboard" className={`navbar-link ${location.pathname === '/dashboard' ? 'active' : ''}`}>Dashboard</Link>
                <Link to="/leaf" className={`navbar-link ${location.pathname === '/leaf' ? 'active' : ''}`}>Leaf</Link>
                <Link to="/soil" className={`navbar-link ${location.pathname === '/soil' ? 'active' : ''}`}>Soil</Link>
                {/* <Link to="/analysis" className={`navbar-link ${location.pathname === '/analysis' ? 'active' : ''}`}>Analysis</Link> */}
                <Link to="/recommendation" className={`navbar-link ${location.pathname === '/recommendation' ? 'active' : ''}`}>Recommendation</Link>
            </div>
            <div className="navbar-logout">
    <button className="logout-button" onClick={handleLogout}>Logout</button>
</div>
        </nav>
    );
};

export default Navbar;