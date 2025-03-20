import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Modal from 'react-modal';
import Login from './Login';
import '../Styles/LandingPage.css';

Modal.setAppElement('#root'); // Set the root element for accessibility

const LandingPage = ({ onLogin }) => {
    const [modalIsOpen, setModalIsOpen] = useState(false);

    const openModal = () => {
        setModalIsOpen(true);
    };

    const closeModal = () => {
        setModalIsOpen(false);
    };

    return (
        <div className="landing-page">
            <nav className="navbar">
                <div className="navbar-brand">
                    <img src="/Page logo.png" alt="NPKnows Logo" className="navbar-logo" />
                </div>
                <div className="navbar-links">
                    <Link to="#" className="navbar-link" onClick={openModal}>Dashboard</Link>
                    <Link to="#" className="navbar-link" onClick={openModal}>Leaf</Link>
                    <Link to="#" className="navbar-link" onClick={openModal}>Soil</Link>
                    <Link to="#" className="navbar-link" onClick={openModal}>Analysis</Link>
                    <Link to="#" className="navbar-link" onClick={openModal}>Recommendation</Link>
                </div>
            </nav>
            <div className="landing-content">
                <h1>Welcome to the Bitter Gourd Leaf Analyzer</h1>
                <p>Analyze the health of your bitter gourd leaves and get recommendations for better growth.</p>
                <button onClick={openModal} className="login-button">Login</button>
            </div>
            <Modal
                isOpen={modalIsOpen}
                onRequestClose={closeModal}
                contentLabel="Login Modal"
                className="modal"
                overlayClassName="overlay"
            >
                <button onClick={closeModal} className="close-button">X</button>
                <Login onLogin={onLogin} />
            </Modal>
        </div>
    );
};

export default LandingPage;