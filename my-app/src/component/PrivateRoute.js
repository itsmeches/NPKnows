import React from 'react';
import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ element, isAuthenticated, handleLogout }) => {
    if (!isAuthenticated) {
        return <Navigate to="/login" />;
    }
    return React.cloneElement(element, { handleLogout });
};

export default PrivateRoute;
