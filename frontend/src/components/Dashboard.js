import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                const userId = localStorage.getItem('userId'); // Assuming you store user ID
                const response = await axios.get(`http://localhost:5000/api/recommendations/${userId}`);
                setRecommendations(response.data.recommendations);
                setLoading(false);
            } catch (err) {
                setError('Failed to load recommendations');
                setLoading(false);
            }
        };

        fetchRecommendations();
    }, []);

    return (
        <div className="dashboard">
            <h2>Recipe Recommendations</h2>
            
            {loading && <p>Loading recommendations...</p>}
            {error && <p className="error">{error}</p>}
            
            {!loading && !error && (
                <div className="recommendations-grid">
                    {recommendations.map((recipe, index) => (
                        <div key={index} className="recipe-card">
                            <h3>{recipe.recipe_title}</h3>
                            <p>Match Score: {(recipe.score * 100).toFixed(1)}%</p>
                            <button 
                                className="view-recipe-btn"
                                onClick={() => window.location.href = `/recipe/${recipe.recipe_id}`}
                            >
                                View Recipe
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Dashboard; 