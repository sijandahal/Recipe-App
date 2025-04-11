import React, { useState } from "react";
import axios from "axios";

const GroceryForm = () => {
  const [ingredients, setIngredients] = useState("");
  const [dietaryPreferences, setDietaryPreferences] = useState("");
  const [budget, setBudget] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = {
      ingredients: ingredients.split(",").map(i => i.trim()),
      dietary_preferences: dietaryPreferences.split(",").map(d => d.trim()),
      budget: parseFloat(budget)
    };

    try {
      const res = await axios.post("http://localhost:5000/upload-groceries", data);
      setResponse(`✅ Success! ID: ${res.data.id}`);
    } catch (error) {
      setResponse("❌ Error sending data.");
      console.error(error);
    }
  };

  return (
    <div className="bg-blue-500 text-xl font-bold underline" style={{ maxWidth: 500, margin: "auto", padding: 20 }}>
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
        <button type="submit">Submit</button>
      </form>
      {response && <p style={{ marginTop: 20 }}>{response}</p>}
    </div>
  );
};

export default GroceryForm;
