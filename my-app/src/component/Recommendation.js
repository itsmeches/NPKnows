// import React, { useState, useEffect } from "react";
// import { useLocation } from "react-router-dom";
// import Navbar from "./Navbar";
// import "../Styles/Recommendation.css";

// const Recommendation = ({ handleLogout }) => {
//     const location = useLocation();
//     const { nitrogen, phosphorus, potassium } = location.state || { nitrogen: 0, phosphorus: 0, potassium: 0 };
//     const [recommendation, setRecommendation] = useState(null);
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState(null);

//     useEffect(() => {
//         if (nitrogen !== 0 || phosphorus !== 0 || potassium !== 0) {
//             const url = `http://127.0.0.1:8000/api/recommendation/?n=${nitrogen}&p=${phosphorus}&k=${potassium}`;
            
//             fetch(url)
//                 .then(response => {
//                     if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
//                     return response.json();
//                 })
//                 .then(data => {
//                     setRecommendation(data);
//                     setLoading(false);
//                 })
//                 .catch(error => {
//                     setError("Failed to fetch recommendation");
//                     setLoading(false);
//                 });
//         } else {
//             setError("Invalid sensor data");
//             setLoading(false);
//         }
//     }, [nitrogen, phosphorus, potassium]);

//     const toggleAccordion = (index) => {
//         const content = document.getElementById(`accordion-content-${index}`);
//         content.style.display = content.style.display === "block" ? "none" : "block";
//     };

//     return (
//         <div className="Recommendation-app">
//             <Navbar handleLogout={handleLogout} />
//             <div className="Recommendation-container">
//                 <h1 className="Recommendation-title">Fertilizer Recommendation</h1>

//                 {loading ? (
//                     <p>Loading recommendation...</p>
//                 ) : error ? (
//                     <p className="error">{error}</p>
//                 ) : recommendation ? (
//                     <div className="Recommendation-content">
//                         {/* 🍃 Nutrient Combination Display */}
//                         <div className="nutrient-combination">{recommendation.Combination}</div>

//                         {/* 📜 Accordion List */}
//                         {Object.entries(recommendation).map(([key, value], index) => (
//                             key !== "Combination" && (
//                                 <div key={index} className="accordion">
//                                     <button className="accordion-button" onClick={() => toggleAccordion(index)}>
//                                         {key}
//                                     </button>
//                                     <div className="accordion-content" id={`accordion-content-${index}`}>
//                                         <p>{value}</p>
//                                     </div>
//                                 </div>
//                             )
//                         ))}
//                     </div>
//                 ) : null}
//             </div>
//         </div>
//     );
// };

// export default Recommendation;

import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import Navbar from "./Navbar";
import "../Styles/Recommendation.css";

const Recommendation = ({ handleLogout }) => {
    const location = useLocation();
    const { nitrogen, phosphorus, potassium } = location.state || { nitrogen: 0, phosphorus: 0, potassium: 0 };
    const [recommendation, setRecommendation] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [expanded, setExpanded] = useState(null);

    useEffect(() => {
        if (nitrogen !== 0 || phosphorus !== 0 || potassium !== 0) {
            const url = `http://127.0.0.1:8000/api/recommendation/?n=${nitrogen}&p=${phosphorus}&k=${potassium}`;
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    setRecommendation(data);
                    setLoading(false);
                })
                .catch(() => {
                    setError("Failed to fetch recommendation");
                    setLoading(false);
                });
        } else {
            setError("Invalid sensor data");
            setLoading(false);
        }
    }, [nitrogen, phosphorus, potassium]);

    const toggleDropdown = (index) => {
        setExpanded(expanded === index ? null : index);
    };

    return (
        <div className="Recommendation-app">
            <Navbar handleLogout={handleLogout} />
            <div className="Recommendation-container">
                <h1 className="Recommendation-title">Fertilizer Recommendation</h1>

                {loading ? (
                    <p>Loading recommendation...</p>
                ) : error ? (
                    <p className="error">{error}</p>
                ) : (
                    recommendation && (
                        <div className="Recommendation-content">
                            <h2 className="highlight-text">{recommendation.Combination}</h2>
                            <div className="dropdown">
                                <button className="accordion-button" onClick={() => toggleDropdown(1)}>
                                    Fertilizer Recommended Rate
                                </button>
                                {expanded === 1 && <div className="accordion-content">{recommendation["Fertilizer Recommended Rate"]}</div>}
                            </div>
                            <div className="dropdown">
                                <button className="accordion-button" onClick={() => toggleDropdown(2)}>
                                    Option 1 (1st & 2nd Application)
                                </button>
                                {expanded === 2 && (
                                    <div className="accordion-content">
                                        <p><strong>1st Application:</strong> {recommendation["Option 1 - 1st Application"]}</p>
                                        <p><strong>2nd Application:</strong> {recommendation["Option 1 - 2nd Application"]}</p>
                                    </div>
                                )}
                            </div>
                            <div className="dropdown">
                                <button className="accordion-button" onClick={() => toggleDropdown(3)}>
                                    Option 2 (1st & 2nd Application)
                                </button>
                                {expanded === 3 && (
                                    <div className="accordion-content">
                                        <p><strong>1st Application:</strong> {recommendation["Option 2 - 1st Application"]}</p>
                                        <p><strong>2nd Application:</strong> {recommendation["Option 2 - 2nd Application"]}</p>
                                    </div>
                                )}
                            </div>
                            <div className="dropdown">
                                <button className="accordion-button" onClick={() => toggleDropdown(4)}>
                                    Mode of Application
                                </button>
                                {expanded === 4 && <div className="accordion-content">{recommendation["Mode of Application"]}</div>}
                            </div>
                            <div className="dropdown">
                                <button className="accordion-button" onClick={() => toggleDropdown(5)}>
                                    Slightly Acid Loving Crops
                                </button>
                                {expanded === 5 && <div className="accordion-content">{recommendation["Slightly Acid Loving Crops"]}</div>}
                            </div>
                        </div>
                    )
                )}
            </div>
        </div>
    );
};

export default Recommendation;
