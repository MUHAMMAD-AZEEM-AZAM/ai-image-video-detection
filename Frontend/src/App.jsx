
import './App.css'
import Home from './pages/Home/Home'
import { Route, Routes } from 'react-router-dom'
import Navbar from './components/Navbar/Navbar'
import About from './pages/About/About'

function App() {

  return (
    <>
    <Navbar /> 
      <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      </Routes>
    </>
  )
}

export default App
