import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "../Styles/Login.css";

const Login = ({ onLogin }) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!username || !password) {
            setError("Username and password are required.");
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const response = await axios.post(
                "http://localhost:8000/api/login/", 
                { username, password },
                { headers: { 'Content-Type': 'application/json' } }
            );

            if (response.data.token) {
                localStorage.setItem("authToken", response.data.token);
                onLogin({ username });
                navigate("/dashboard");
            } else {
                setError("Invalid response from server.");
            }
        } catch (error) {
            setError(error.response?.data?.error || "Network error. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <div className="login-header">
                    <img src="/rb_661 copy.png" alt="NPKnows Logo" className="login-logo" />
                    <h1 className="login-title">NPKnows</h1>
                </div>
                <hr className="divider" />
                <h2>Welcome Back</h2>
                <p className="login-subtext">Log in to continue</p>
                <form onSubmit={handleSubmit}>
                    <div className="input-container">
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Username"
                            required
                        />
                    </div>
                    <div className="input-container">
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Password"
                            required
                        />
                    </div>
                    <div className="remember-forgot">
                        <label>
                            <input type="checkbox" /> Remember me
                        </label>
                        <Link to="/forgot-password" className="forgot-password">Forgot Password?</Link>
                    </div>
                    <button type="submit" disabled={loading} className="btn-login">
                        {loading ? "Logging in..." : "Log in"}
                    </button>
                    {error && <p className="error-message">{error}</p>}
                </form>
                <div className="register-link">
                    Don't have an account? <Link to="/register">Sign up</Link>
                </div>
            </div>
        </div>
    );
};

export default Login;
















// import React, { useState } from "react";
// import { Link, useNavigate } from "react-router-dom";
// import axios from "axios";
// import "../Styles/Login.css";

// const Login = ({ onLogin }) => {
//     const [username, setUsername] = useState("");
//     const [password, setPassword] = useState("");
//     const [error, setError] = useState(null);
//     const [loading, setLoading] = useState(false);
//     const navigate = useNavigate();

//     const handleSubmit = async (event) => {
//         event.preventDefault();
    
//         if (!username || !password) {
//             setError("Username and password are required.");
//             return;
//         }
    
//         setLoading(true);
//         setError(null); // Clear previous errors
    
//         try {
//             const response = await axios.post(
//                 "http://localhost:8000/api/login/", 
//                 { username, password },
//                 { headers: { 'Content-Type': 'application/json' } }
//             );
    
//             // Check for token in response
//             if (response.data.token) {
//                 localStorage.setItem("authToken", response.data.token); // Store token properly
//                 console.log("Token stored:", localStorage.getItem("authToken"));
//                 onLogin({ username });
//                 navigate("/dashboard");
//             } else {
//                 setError("Invalid response from server.");
//             }
//         } catch (error) {
//             console.error("Login error:", error);
    
//             // Check if error.response exists and has a proper error message
//             if (error.response) {
//                 // Log the full error response
//                 console.log("Full error response:", error.response);
    
//                 setError(error.response.data ? error.response.data.error : "Invalid username or password.");
//             } else {
//                 setError("Network error. Please try again.");
//             }
//         } finally {
//             setLoading(false);
//         }
//     };

//     return (
//         <div className="login-container">
//             <div className="login-box">
//                 <div className="login-logo-container">
//                     <img src="/rb_661 copy.png" alt="NPKnows Logo" className="login-logo" />
//                     <span className="login-logo-text">NPKnows</span>
//                 </div>
//                 <hr className="divider" />
//                 <h2>Log in to your account</h2>
//                 <form onSubmit={handleSubmit}>
//                     <div className="input-container username">
//                         <input
//                             type="text"
//                             id="username"
//                             value={username}
//                             onChange={(event) => setUsername(event.target.value)}
//                             placeholder="Username"
//                             required
//                         />
//                     </div>
//                     <div className="input-container password">
//                         <input
//                             type="password"
//                             id="password"
//                             value={password}
//                             onChange={(event) => setPassword(event.target.value)}
//                             placeholder="Password"
//                             required
//                         />
//                     </div>
//                     <div className="remember-me">
//                         <label htmlFor="remember">Remember me</label>
//                         <input type="checkbox" id="remember" />
//                     </div>
//                     <button type="submit" disabled={loading} className="btn-login">
//                         {loading ? "Logging in..." : "Log in"}
//                     </button>
//                     {error && <p className="error">{error}</p>}
//                 </form>
//                 <div className="register-link">
//                     <p>
//                         Don't have an account? <Link to="/register">Register</Link>
//                     </p>
//                 </div>
//             </div>
//         </div>
//     );
// };

// export default Login;
