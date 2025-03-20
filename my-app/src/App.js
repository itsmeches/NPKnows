import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import axios from 'axios';
import Login from './component/Login';
import Register from './component/Register';
import Leaf from './component/Leaf';
import LandingPage from './component/LandingPage';
import Soil from './component/Soil';
import Dashboard from './component/Dashboard';
import Analysis from './component/Analysis';
import PrivateRoute from './component/PrivateRoute';
import Recommendation from './component/Recommendation';

const App = () => {
    const [user, setUser] = useState(() => {
        const savedUser = localStorage.getItem('user');
        return savedUser ? JSON.parse(savedUser) : null;
    });

    useEffect(() => {
        const validateToken = async () => {
            const token = localStorage.getItem('authToken');
            if (token) {
                try {
                    const response = await axios.get('http://localhost:8000/api/validate-token/', {
                        headers: {
                            'Authorization': `Token ${token}`,
                        },
                    });
                    if (response.data.valid) {
                        setUser(response.data.user);
                    } else {
                        setUser(null);
                        localStorage.removeItem('authToken');
                        localStorage.removeItem('user');
                    }
                } catch (error) {
                    setUser(null);
                    localStorage.removeItem('authToken');
                    localStorage.removeItem('user');
                }
            }
        };

        validateToken();
    }, []);

    useEffect(() => {
        if (user) {
            localStorage.setItem('user', JSON.stringify(user));
        } else {
            localStorage.removeItem('user');
        }
    }, [user]);

    const handleLogout = () => {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        setUser(null);
    };

    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login onLogin={setUser} />} />
                <Route path="/register" element={<Register onRegister={setUser} />} />
                <Route path="/landing" element={<LandingPage onLogin={setUser} />} />
                <Route path="/leaf" element={<PrivateRoute element={<Leaf />} isAuthenticated={!!user} handleLogout={handleLogout} />} />
                <Route path="/soil" element={<PrivateRoute element={<Soil />} isAuthenticated={!!user} handleLogout={handleLogout} />} />
                <Route path="/dashboard" element={<PrivateRoute element={<Dashboard />} isAuthenticated={!!user} handleLogout={handleLogout} />} />
                {/* <Route path="/analysis" element={<PrivateRoute element={<Analysis />} isAuthenticated={!!user} handleLogout={handleLogout} />} /> */}
                <Route path="/recommendation" element={<PrivateRoute element={<Recommendation />} isAuthenticated={!!user} handleLogout={handleLogout} />} />
                <Route path="/" element={<Navigate to="/landing" />} />
            </Routes>
        </Router>
    );
};

export default App;