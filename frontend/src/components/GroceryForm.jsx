import React, { useState } from "react";
import axios from "axios";
import config from "../config";

const GroceryForm = () => {
  const [ingredients, setIngredients] = useState("");
  const [dietaryPreferences, setDietaryPreferences] = useState("");
  const [budget, setBudget] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setRecommendations([]);

    const data = {
      ingredients: ingredients.split(",").map(i => i.trim()),
      dietary_preferences: dietaryPreferences.split(",").map(d => d.trim()),
      budget: parseFloat(budget)
    };

    try {
      const res = await axios.post(`${config.backendUrl}/upload-groceries`, data);
      setRecommendations(res.data.recommendations);
    } catch (error) {
      setError("❌ Error getting recommendations. Please try again.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-blue-500 text-xl font-bold underline" style={{ maxWidth: 800, margin: "auto", padding: 20 }}>
      <form onSubmit={handleSubmit}>
        <label className="text-4xl text-indigo-600 font-bold underline">Ingredients (comma separated)</label>
        <input
          type="text"
          value={ingredients}
          onChange={(e) => setIngredients(e.target.value)}
          required
          style={{ width: "100%", marginBottom: 10 }}
        />
        <label>Dietary Preferences (comma separated)</label>
        <input
          type="text"
          value={dietaryPreferences}
          onChange={(e) => setDietaryPreferences(e.target.value)}
          style={{ width: "100%", marginBottom: 10 }}
        />
        <label>Budget ($)</label>
        <input
          type="number"
          value={budget}
          onChange={(e) => setBudget(e.target.value)}
          required
          style={{ width: "100%", marginBottom: 10 }}
        />
        <button 
          type="submit"
          disabled={loading}
          style={{ 
            padding: "10px 20px", 
            backgroundColor: loading ? "#ccc" : "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: loading ? "not-allowed" : "pointer"
          }}
        >
          {loading ? "Loading..." : "Get Recommendations"}
        </button>
      </form>

      {error && <p style={{ color: "red", marginTop: 20 }}>{error}</p>}

      {recommendations.length > 0 && (
        <div style={{ marginTop: 20 }}>
          <h2 style={{ color: "white", marginBottom: 10 }}>Recommended Recipes:</h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: "20px" }}>
            {recommendations.map((recipe, index) => (
              <div 
                key={index} 
                style={{ 
                  backgroundColor: "white", 
                  padding: 15, 
                  borderRadius: 8,
                  boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
                }}
              >
                <h3 style={{ marginBottom: 10 }}>{recipe.recipe_title}</h3>
                <p style={{ marginBottom: 10 }}>
                  <strong>Match Score:</strong> {(recipe.score * 100).toFixed(1)}%
                </p>
                <div style={{ marginBottom: 10 }}>
                  <strong>Ingredients:</strong>
                  <ul style={{ marginLeft: 20 }}>
                    {JSON.parse(recipe.ingredients).map((ing, i) => (
                      <li key={i}>{ing}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <strong>Instructions:</strong>
                  <p style={{ whiteSpace: "pre-wrap" }}>{recipe.instructions}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default GroceryForm;
