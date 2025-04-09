import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./globals.css"
import Hello from "./Hello";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <Hello/>
    <App />
  </React.StrictMode>
);
