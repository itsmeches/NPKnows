import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from './Navbar';
import '../Styles/Soil.css';

const getNPKCategory = (value, type) => {
    if (type === 'nitrogen') {
        if (value < 10) return 'LOW';
        if (value >= 10 && value <= 20) return 'MEDIUM';
        return 'HIGH';
    } else if (type === 'phosphorus') {
        if (value <= 15) return 'LOW';
        if (value >= 16 && value <= 25) return 'MEDIUM';
        return 'HIGH';
    } else if (type === 'potassium') {
        if (value < 60) return 'LOW';
        if (value >= 61 && value <= 130) return 'MEDIUM';
        return 'HIGH';
    }
    return 'LOW';
};

const Soil = ({ handleLogout }) => {
    const [sensorData, setSensorData] = useState({ Nitrogen: 0, Phosphorus: 0, Potassium: 0 });
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem('authToken');
            if (!token) {
                navigate('/login');
                return;
            }

            try {
                const response = await axios.get('http://127.0.0.1:8000/api/arduino/', {
                    headers: { Authorization: `Token ${token}` }
                });

                const data = response.data.sensor_data;
                if (data) {
                    setSensorData({
                        Nitrogen: parseFloat(data.nitrogen) || 0,
                        Phosphorus: parseFloat(data.phosphorus) || 0,
                        Potassium: parseFloat(data.potassium) || 0,
                    });
                    setError(null);
                } else {
                    setError('No sensor data available');
                }
            } catch (error) {
                setError('Failed to fetch sensor data');
            }
        };

        fetchData();
        const intervalId = setInterval(fetchData, 5000);
        return () => clearInterval(intervalId);
    }, [navigate]);

    const handleGetRecommendation = () => {
        const categoricalData = {
            nitrogen: getNPKCategory(sensorData.Nitrogen, 'nitrogen'),
            phosphorus: getNPKCategory(sensorData.Phosphorus, 'phosphorus'),
            potassium: getNPKCategory(sensorData.Potassium, 'potassium'),
        };

        navigate('/recommendation', {
            state: {
                nitrogen: categoricalData.nitrogen,
                phosphorus: categoricalData.phosphorus,
                potassium: categoricalData.potassium,
            },
        });
    };

    return (
        <div className="Soil-app">
            <Navbar handleLogout={handleLogout} />
            <div className="Soil-container">
                <h1 className="Soil-title">Live Sensor Data</h1>
                
                {error && <p className="error-message">{error}</p>}
                
                <div className="Soil-data">
                    <div className="Soil-card">
                        <h3>Nitrogen</h3>
                        <p className="Soil-value">{sensorData.Nitrogen} <span>ppm</span></p>
                    </div>
                    <div className="Soil-card">
                        <h3>Phosphorus</h3>
                        <p className="Soil-value">{sensorData.Phosphorus} <span>ppm</span></p>
                    </div>
                    <div className="Soil-card">
                        <h3>Potassium</h3>
                        <p className="Soil-value">{sensorData.Potassium} <span>ppm</span></p>
                    </div>
                </div>

                <button className="Soil-button" onClick={handleGetRecommendation}>
                    Get Recommendation
                </button>
            </div>
        </div>
    );
};

export default Soil;

















// import React, { useState, useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';
// import axios from 'axios';
// import Navbar from './Navbar';
// import '../Styles/Soil.css';

// // Define the getNPKCategory function
// const getNPKCategory = (value, type) => {
//     if (type === 'nitrogen') {
//         if (value < 10) return 'LOW';
//         if (value >= 10 && value <= 20) return 'MEDIUM';
//         return 'HIGH';
//     } else if (type === 'phosphorus') {
//         if (value <= 15) return 'LOW';
//         if (value >= 16 && value <= 25) return 'MEDIUM';
//         return 'HIGH';
//     } else if (type === 'potassium') {
//         if (value < 60) return 'LOW';
//         if (value >= 61 && value <= 130) return 'MEDIUM';
//         return 'HIGH';
//     }
//     return 'LOW'; // Default
// };

// const Soil = ({ handleLogout }) => {
//     const [sensorData, setSensorData] = useState({ Nitrogen: 0, Phosphorus: 0, Potassium: 0 });
//     const [error, setError] = useState(null);
//     const navigate = useNavigate();

//     useEffect(() => {
//         const fetchData = async () => {
//             const token = localStorage.getItem('authToken');
//             if (!token) {
//                 navigate('/login');  // Redirect if not logged in
//                 return;
//             }

//             try {
//                 const response = await axios.get('http://127.0.0.1:8000/api/arduino/', {
//                     headers: { Authorization: `Token ${token}` }
//                 });

//                 console.log('Full API Response:', response.data);
//                 const data = response.data.sensor_data;
//                 console.log('Sensor Data:', data); // Log the sensor data

//                 if (data) {
//                     setSensorData({
//                         Nitrogen: parseFloat(data.nitrogen) || 0,
//                         Phosphorus: parseFloat(data.phosphorus) || 0,
//                         Potassium: parseFloat(data.potassium) || 0,
//                     });
//                     setError(null); // Clear any previous errors
//                 } else {
//                     setError('No sensor data available');
//                 }
//             } catch (error) {
//                 console.error('Error fetching sensor data:', error);
//                 if (error.response) {
//                     console.error('Error Response Data:', error.response.data);
//                     console.error('Error Response Status:', error.response.status);
//                     console.error('Error Response Headers:', error.response.headers);
//                     setError(`Error fetching sensor data: ${error.response.data.error || 'Please try again.'}`);
//                 } else if (error.request) {
//                     console.error('Error Request:', error.request);
//                     setError('Error fetching sensor data. No response received.');
//                 } else {
//                     console.error('Error Message:', error.message);
//                     setError(`Error fetching sensor data: ${error.message}`);
//                 }
//             }
//         };

//         fetchData();
//         const intervalId = setInterval(fetchData, 5000);
//         return () => clearInterval(intervalId);
//     }, [navigate]);

//     const handleGetRecommendation = () => {
//         // Convert numerical sensor data to categorical values
//         const categoricalData = {
//             nitrogen: getNPKCategory(sensorData.Nitrogen, 'nitrogen'),
//             phosphorus: getNPKCategory(sensorData.Phosphorus, 'phosphorus'),
//             potassium: getNPKCategory(sensorData.Potassium, 'potassium'),
//         };

//         console.log("Categorical Sensor Data:", categoricalData); // Debugging log

//         // Navigate to the Recommendation component with categorical data
//         navigate('/recommendation', {
//             state: {
//                 nitrogen: categoricalData.nitrogen,
//                 phosphorus: categoricalData.phosphorus,
//                 potassium: categoricalData.potassium,
//             },
//         });
//     };

//     return (
//         <div className="soil-sensor-app">
//             <Navbar handleLogout={handleLogout} />
//             <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
//                 <div className="table-container">
//                     <h1 className="table-title">Live Sensor Data</h1>
//                     {error && <p className="error-message">{error}</p>}
//                     <table className="table-auto">
//                         <thead>
//                             <tr>
//                                 <th className="px-4 py-2">Nutrient</th>
//                                 <th className="px-4 py-2">Value</th>
//                             </tr>
//                         </thead>
//                         <tbody>
//                             <tr>
//                                 <td className="border px-4 py-2">Nitrogen</td>
//                                 <td className="border px-4 py-2">{sensorData.Nitrogen}</td>
//                             </tr>
//                             <tr>
//                                 <td className="border px-4 py-2">Phosphorus</td>
//                                 <td className="border px-4 py-2">{sensorData.Phosphorus}</td>
//                             </tr>
//                             <tr>
//                                 <td className="border px-4 py-2">Potassium</td>
//                                 <td className="border px-4 py-2">{sensorData.Potassium}</td>
//                             </tr>
//                         </tbody>
//                     </table>
//                     <button
//                         onClick={handleGetRecommendation}
//                         className="mt-4 bg-blue-500 text-white px-4 py-2 rounded"
//                     >
//                         Get Recommendation
//                     </button>
//                 </div>
//             </div>
//         </div>
//     );
// };

// export default Soil;