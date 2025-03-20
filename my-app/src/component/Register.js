import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../Styles/Register.css';

const Register = ({ onRegister }) => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [rememberMe, setRememberMe] = useState(false); // New state
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage('');
        setLoading(true);

        if (!username || !email || !password || !confirmPassword) {
            setMessage('All fields are required.');
            setLoading(false);
            return;
        }

        if (password !== confirmPassword) {
            setMessage('Passwords do not match.');
            setLoading(false);
            return;
        }

        try {
            const response = await axios.post('http://localhost:8000/api/register/', { 
                username, 
                email, 
                password 
            });

            console.log("Backend Response:", response); // Debugging log

            if (response.status === 201) {  
                const token = response.data.token;
                localStorage.setItem('authToken', token);  
                onRegister(token);  // Update state in App.js
                navigate('/dashboard');  // Redirect to Dashboard
            } else {
                setMessage("Unexpected response. Please try again.");
            }
        } catch (error) {
            console.error("Registration Error:", error.response); // Log error response
            setMessage(error.response?.data?.error || "Registration failed. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="register-container">
            <form onSubmit={handleSubmit} className="register-form">
                <div className="register-logo-container">
                    <img src="/rb_661 copy.png" alt="NPKnows Logo" className="register-logo" />
                    <span className="register-logo-text">NPKnows</span>
                </div>
                <hr className="divider" />
                <h2>Create an account</h2>
                
                <div className="input-container">
                    <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
                </div>
                
                <div className="input-container">
                    <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
                </div>
                
                <div className="input-container">
                    <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
                </div>
                
                <div className="input-container">
                    <input type="password" placeholder="Re-enter Password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} required />
                </div>

                {/* Remember Me Checkbox */}
                <div className="remember-me-container">
                    <input
                        type="checkbox"
                        id="remember"
                        checked={rememberMe}
                        onChange={() => setRememberMe(!rememberMe)}
                    />
                    <label htmlFor="remember">Remember me</label>
                </div>
                
                <button className="btn-register" type="submit" disabled={loading}>
                    {loading ? 'Registering...' : 'Register'}
                </button>
                
                {message && <p className="error">{message}</p>}
                
                <div className="register-link">
                    <p>
                        Already have an account? <Link to="/login">Login</Link>
                    </p>
                </div>
            </form>
        </div>
    );
};

export default Register;























// import React, { useState } from 'react';
// import { Link, useNavigate } from 'react-router-dom';
// import axios from 'axios';
// import '../Styles/Register.css';

// const Register = ({ onRegister }) => {
//     const [username, setUsername] = useState('');
//     const [email, setEmail] = useState('');
//     const [password, setPassword] = useState('');
//     const [confirmPassword, setConfirmPassword] = useState('');
//     const [message, setMessage] = useState('');
//     const [loading, setLoading] = useState(false);
//     const navigate = useNavigate();

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         setMessage('');
//         setLoading(true);

//         if (!username || !email || !password || !confirmPassword) {
//             setMessage('All fields are required.');
//             setLoading(false);
//             return;
//         }

//         if (password !== confirmPassword) {
//             setMessage('Passwords do not match.');
//             setLoading(false);
//             return;
//         }

//         try {
//             const response = await axios.post('http://localhost:8000/api/register/', { 
//                 username, 
//                 email, 
//                 password 
//             });

//             console.log("Backend Response:", response); // Debugging log

//             if (response.status === 201) {  
//                 const token = response.data.token;
//                 localStorage.setItem('authToken', token);  
//                 onRegister(token);  // Update state in App.js
//                 navigate('/dashboard');  // Redirect to Dashboard
//             } else {
//                 setMessage("Unexpected response. Please try again.");
//             }
//         } catch (error) {
//             console.error("Registration Error:", error.response); // Log error response
//             setMessage(error.response?.data?.error || "Registration failed. Please try again.");
//         } finally {
//             setLoading(false);
//         }
//     };

//     return (
//         <div className="register-container">
//             <form onSubmit={handleSubmit} className="register-form">
//                 <div className="register-logo-container">
//                     <img src="/rb_661 copy.png" alt="NPKnows Logo" className="register-logo" />
//                     <span className="register-logo-text">NPKnows</span>
//                 </div>
//                 <hr className="divider" />
//                 <h2>Create an account</h2>
                
//                 <div className="input-container">
//                     <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
//                 </div>
                
//                 <div className="input-container">
//                     <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
//                 </div>
                
//                 <div className="input-container">
//                     <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
//                 </div>
                
//                 <div className="input-container">
//                     <input type="password" placeholder="Re-enter Password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} required />
//                 </div>
                
//                 <button className="btn-register" type="submit" disabled={loading}>
//                     {loading ? 'Registering...' : 'Register'}
//                 </button>
                
//                 {message && <p className="error">{message}</p>}
                
//                 <div className="register-link">
//                     <p>
//                         Already have an account? <Link to="/login">Login</Link>
//                     </p>
//                 </div>
//             </form>
//         </div>
//     );
// };

// export default Register;
