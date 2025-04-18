import { Routes, Route } from 'react-router-dom';
import Layout from '@/layout/Layout';
import Home from '@/pages/home/Home';
import Demo from '@/pages/components-demo/Demo';

/**
 * Main App component
 * Defines the routing structure for the entire application
 * Each route is associated with a specific tool or feature
 */
const App = () => {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/demo" element={<Demo />} />
      </Route>
    </Routes>
  );
};

export default App;
