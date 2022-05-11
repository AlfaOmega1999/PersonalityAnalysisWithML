import React from 'react';
import './App.css';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages';
import Tipos from './pages/tipos';
import Predictor from './pages/predictor';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path='/' exact element={<Home/>} />
        <Route path='/tipos' element={<Tipos/>} />
        <Route path='/predictor' element={<Predictor/>} />
      </Routes>
    </Router>
  );
}

export default App;