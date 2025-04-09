import React from 'react';
import GroceryForm from './components/GroceryForm';
function App() {
  return (
    <div>
      <h1 className='text-3xl'>Forkast Frontend</h1>
      <p>Frontend connected to Flask backend.</p>
      <GroceryForm/>
    </div>
  );
}
export default App;
