import { Routes, Route, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import Landing from './pages/Landing';
import TaxPlanner from './pages/TaxPlanner';
import InvestPlanner from './pages/InvestPlanner';

function App() {
  const location = useLocation();
  const [fadeKey, setFadeKey] = useState(location.pathname);

  useEffect(() => {
    setFadeKey(location.pathname);
  }, [location.pathname]);

  return (
    <div className="app-shell">
      <Navbar />
      <main key={fadeKey} className="fade-in">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/tax" element={<TaxPlanner />} />
          <Route path="/invest" element={<InvestPlanner />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;
