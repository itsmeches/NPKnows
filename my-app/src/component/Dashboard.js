import React, { useState, useEffect } from 'react';
import Navbar from './Navbar';
import '../Styles/Dashboard.css';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';

const Dashboard = ({ handleLogout, username }) => {
    const currentHour = new Date().getHours();
    let greeting = "Good day, Farmer!";
    if (currentHour < 12) {
        greeting = "Good morning, Farmer!";
    } else if (currentHour < 18) {
        greeting = "Good afternoon, Farmer!";
    } else {
        greeting = `Good evening, ${username || "User"}!`;
    }

    const [lastUploadedImage, setLastUploadedImage] = useState(null);

    useEffect(() => {
        const fetchLatestImage = async () => {
            try {
                const response = await fetch('/api/latest-uploaded-image');
                const data = await response.json();
                setLastUploadedImage(data.imageUrl);
            } catch (error) {
                console.error('Error fetching the latest uploaded image:', error);
            }
        };

        fetchLatestImage();
    }, []);

    const healthReports = [
        { date: "Feb 20", score: 75 },
        { date: "Feb 21", score: 80 },
        { date: "Feb 22", score: 78 },
        { date: "Feb 23", score: 85 },
        { date: "Feb 24", score: 88 },
        { date: "Feb 25", score: 90 },
        { date: "Feb 26", score: 87 },
    ];

    // Nutrient Data for Growth Tips
    const nutrientData = [
        { name: 'Nitrogen (N)', value: 35 },
        { name: 'Phosphorus (P)', value: 20 },
        { name: 'Potassium (K)', value: 50 }
    ];

    return (
        <div className="dashboard-app">
            <Navbar handleLogout={handleLogout} />
            <div className="dashboard-container">
                <div className="outer-card">
                    <div className="greeting">
                        <h1>{greeting}</h1>
                    </div>

                    <div className="dashboard-actions">
                        <div className="dashboard-card">
                            <i className="fa fa-leaf"></i>
                            <p>Leaf Health Diagnosis</p>
                            <div className="uploaded-image">
                                <img src="/4a072162-3ff0-47e0-934d-322d2e4e67a5_removalai_preview_7QFHzQj.png" 
                                     alt="Static Leaf" className="static-leaf-img" />
                                {lastUploadedImage && (
                                    <img src={lastUploadedImage} alt="Latest Leaf" className="uploaded-img" />
                                )}
                            </div>
                        </div>

                        <div className="dashboard-card">
                            <i className="fa fa-cogs"></i>
                            <p>Real-Time Soil Insights</p>
                            <div className="npk-data">
                                {nutrientData.map(nutrient => (
                                    <div className="npk-item" key={nutrient.name}>
                                        <p><strong>{nutrient.name}:</strong> {nutrient.value} mg/kg</p>
                                        <div className="progress-bar">
                                            <div className={`progress-fill ${nutrient.name.toLowerCase().split(' ')[0]}`} 
                                                 style={{ width: `${nutrient.value}%` }}>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                                <p className="last-updated">Last Updated: Feb 26, 2025, 10:30 AM</p>
                            </div>
                        </div>

                        <div className="dashboard-card">
                            <i className="fa fa-chart-line"></i>
                            <p>Recent Health Reports</p>
                            <ResponsiveContainer width="100%" height={200}>
                                <LineChart data={healthReports}>
                                    <XAxis dataKey="date" />
                                    <YAxis domain={[70, 100]} />
                                    <Tooltip />
                                    <Line type="monotone" dataKey="score" stroke="#4CAF50" strokeWidth={2} />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>

                        {/* Personalized Growth Tips Section */}
                        <div className="dashboard-card">
                            <i className="fa fa-pagelines"></i>
                            <p>Personalized Growth Tips</p>

                            {/* Bar Chart for Nutrient Levels */}
                            <ResponsiveContainer width="100%" height={200}>
                                <BarChart data={nutrientData}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="name" />
                                    <YAxis />
                                    <Tooltip />
                                    <Legend />
                                    <Bar dataKey="value" fill="#82ca9d" />
                                </BarChart>
                            </ResponsiveContainer>

                            {/* Growth Tips */}
                            <div className="growth-tips">
                                <h3>📌 Nutrient Balance:</h3>
                                <ul>
                                    <li><strong>Nitrogen:</strong> High | <strong>Phosphorus:</strong> Medium | <strong>Potassium:</strong> Low</li>
                                    <li><strong>Recommended Fertilizer:</strong> 14-14-14, 0-18-0, 0-0-60, or organic alternatives</li>
                                    <li><strong>Application:</strong> Mix half at planting, sidedress when fruits form</li>
                                    <li><strong>pH Tip:</strong> Maintain 6.0-7.0; avoid mixing lime with fertilizers</li>
                                </ul>
                            </div>
                        </div>

                    </div> 
                </div>
            </div>
        </div>
    );
};

export default Dashboard;





// import React from 'react';
// import Navbar from './Navbar';
// import '../Styles/Dashboard.css';

// const Dashboard = ({ handleLogout }) => {
//     // Get the current hour for personalized greeting
//     const currentHour = new Date().getHours();
//     let greeting = "Good day, Farmer!";
//     if (currentHour < 12) {
//         greeting = "Good morning, Farmer!";
//     } else if (currentHour < 18) {
//         greeting = "Good afternoon, Farmer!";
//     } else {
//         greeting = "Good evening, Farmer!";
//     }

//     return (
//         <div className="dashboard-app">
//             <Navbar handleLogout={handleLogout} />
//             <div className="dashboard-container">
//                 <h1 className="dashboard-title">{greeting}</h1>
//                 <div className="dashboard-content">
//                     <p>Welcome to the Bitter Gourd Leaf Analyzer Dashboard!</p>
//                     <p>Here you can view and manage your data, analyze leaf health, and receive personalized recommendations for soil and plant care.</p>
//                 </div>
//                 <div className="dashboard-actions">
//                     <div className="dashboard-card">
//                         <i className="fa fa-leaf" style={{ fontSize: '2rem', marginRight: '10px' }}></i>
//                         <p>Analyze Leaf Health</p>
//                     </div>
//                     <div className="dashboard-card">
//                         <i className="fa fa-cogs" style={{ fontSize: '2rem', marginRight: '10px' }}></i>
//                         <p>Soil Compatibility</p>
//                     </div>
//                     <div className="dashboard-card">
//                         <i className="fa fa-chart-line" style={{ fontSize: '2rem', marginRight: '10px' }}></i>
//                         <p>View Analysis Results</p>
//                     </div>
//                 </div>
//             </div>
//         </div>
//     );
// };

// export default Dashboard;
