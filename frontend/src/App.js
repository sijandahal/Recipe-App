import React from 'react';
import GroceryForm from './components/GroceryForm';
import Home from "./pages/Homepage";
import LoginPage from './components/Auth/Login';
import RegisterPage from './components/Auth/Register';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard/Dashboard';
function App() {
  return (
    <Router>
      <Routes>
        <Route path = "/signup" element = {<RegisterPage/>} />
        <Route path = "/login" element = {<LoginPage/>} />
        <Route path = "/dashboard" element = {<Dashboard/>} />
      <Route path = "/"  element = {<Home/>}/>
      {/* <GroceryForm/> */}
      </Routes>
    </Router>
  );
}
export default App;
