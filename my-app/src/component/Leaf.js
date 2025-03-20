import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from './Navbar';
import '../Styles/Leaf.css';

const Leaf = ({ handleLogout }) => {
    const [image, setImage] = useState(null);
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const checkToken = async () => {
            const token = localStorage.getItem('authToken');
            if (!token) {
                navigate('/login');
                return;
            }

            try {
                await axios.get('http://localhost:8000/api/validate-token/', {
                    headers: { Authorization: `Token ${token}` }
                });
            } catch (error) {
                console.log('Token expired or invalid:', error);
                localStorage.removeItem('authToken');
                navigate('/login');
            }
        };
        checkToken();
    }, [navigate]);

    const handleImageChange = async (event) => {
        const file = event.target.files[0];
        if (file) {
            const imgUrl = URL.createObjectURL(file);
            setImage(imgUrl);
            await analyzeImage(file);
        }
    };

    const analyzeImage = async (imageFile) => {
        setLoading(true);
        setError(null);
        setPrediction(null);

        try {
            const formData = new FormData();
            formData.append('image', imageFile);

            let token = localStorage.getItem('authToken');
            if (token) {
                token = token.replace(/"/g, '').trim();
            }

            const response = await axios.post('http://localhost:8000/api/predict/', formData, {
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'multipart/form-data',
                },
            });

            if (response.data.predictions && response.data.predictions.length > 0) {
                const { className, probability } = response.data.predictions[0];
                setPrediction({ className, probability });
            } else {
                setPrediction({ className: "Unknown", probability: "N/A" });
            }
        } catch (error) {
            if (error.response) {
                if (error.response.status === 401) {
                    setError('Session expired. Redirecting to login...');
                    localStorage.removeItem('authToken');
                    setTimeout(() => navigate('/login'), 2000);
                } else {
                    setError(error.response.data.error || 'Error analyzing image. Please try again.');
                }
            } else {
                setError('Network error. Please check your connection.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="leaf-analyzer-app">
            <Navbar handleLogout={handleLogout} />
            <div className="leaf-analyzer-container">
                <h1 className="title">Bitter Gourd Leaf Analyzer</h1>
                <label htmlFor="file-upload" className="custom-file-upload">Upload Image</label>
                <input
                    id="file-upload"
                    type="file"
                    accept="image/*"
                    onChange={handleImageChange}
                    className="file-input"
                />
                {image && <img src={image} alt="Uploaded" className="preview-image" />}
                {loading && <p className="loading">Analyzing...</p>}
                {prediction && (
                    <div className="prediction-result">
                        <h2>Prediction</h2>
                        <p>Class: <strong>{prediction.className}</strong></p>
                        <p>Confidence: <strong>{prediction.probability.toFixed(2)}%</strong></p>
                    </div>
                )}
                {error && <p className="error-message">{error}</p>}
            </div>
        </div>
    );
};

export default Leaf;



// import React, { useState, useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';
// import axios from 'axios';
// import Navbar from './Navbar';
// import '../Styles/Leaf.css';

// const Leaf = ({ handleLogout }) => {
//     const [image, setImage] = useState(null);
//     const [prediction, setPrediction] = useState(null);
//     const [loading, setLoading] = useState(false);
//     const [error, setError] = useState(null);
//     const navigate = useNavigate();

//     useEffect(() => {
//         const checkToken = async () => {
//             const token = localStorage.getItem('authToken');
//             if (!token) {
//                 navigate('/login');
//                 return;
//             }
    
//             try {
//                 await axios.get('http://localhost:8000/api/validate-token/', {
//                     headers: { Authorization: `Token ${token}` }
//                 });
//             } catch (error) {
//                 console.log('Token expired or invalid:', error);
//                 localStorage.removeItem('authToken');
//                 navigate('/login');
//             }
//         };
//         checkToken();
//     }, [navigate]);

//     const handleImageChange = async (event) => {
//         const file = event.target.files[0];
//         if (file) {
//             const imgUrl = URL.createObjectURL(file);
//             setImage(imgUrl);
//             await analyzeImage(file);
//         }
//     };

//     const analyzeImage = async (imageFile) => {
//         setLoading(true);
//         setError(null);
//         setPrediction(null);

//         try {
//             const formData = new FormData();
//             formData.append('image', imageFile);

//             let token = localStorage.getItem('authToken');
//             if (token) {
//                 token = token.replace(/"/g, ''); // Remove extra quotes
//             }

//             token = token.trim();
//             console.log("Using Token:", token); // Debugging token

//             const response = await axios.post('http://localhost:8000/api/predict/', formData, {
//                 headers: {
//                     'Authorization': `Token ${token}`,
//                     'Content-Type': 'multipart/form-data',
//                 },
//             });

//             console.log("Server Response:", response.data);
//             if (response.data.predictions && response.data.predictions.length > 0) {
//                 const { className, probability } = response.data.predictions[0];
//                 setPrediction({ className, probability });
//             } else {
//                 setPrediction({ className: "Unknown", probability: "N/A" });
//             }
//         } catch (error) {
//             console.error("Error Response:", error.response);
//             if (error.response) {
//                 if (error.response.status === 401) {
//                     setError('Session expired. Redirecting to login...');
//                     localStorage.removeItem('authToken');
//                     setTimeout(() => navigate('/login'), 2000);
//                 }
//                  else {
//                     setError(error.response.data.error || 'Error analyzing image. Please try again.');
//                 }
//             } else {
//                 setError('Network error. Please check your connection.');
//             }
//         } finally {
//             setLoading(false);
//         }
//     };

//     return (
//         <div className="image-uploader-app">
//             <Navbar handleLogout={handleLogout} />
//             <div className="image-uploader-container">
//                 <h1>Bitter Gourd Leaf Analyzer</h1>
//                 <input
//                     type="file"
//                     accept="image/*"
//                     onChange={handleImageChange}
//                     className="file-input"
//                 />
//                 {image && <img src={image} alt="Uploaded" className="preview-image" />}
//                 {loading && <p>Loading...</p>}
//                 {prediction && (
//                     <div className="prediction-result">
//                         <h2>Prediction:</h2>
//                         <p>Class: {prediction.className} - Confidence: {prediction.probability.toFixed(2)}%</p>
//                     </div>
//                 )}
//                 {error && <p className="error-message">{error}</p>}
//             </div>
//         </div>
//     );
// };

// export default Leaf;
