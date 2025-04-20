import { Routes, Route } from 'react-router-dom';
import Layout from '@/layout/Layout';
import Home from '@/pages/home/Home';
import Demo from '@/pages/demo/Demo';
import Login from '@/pages/login/Login';
import Signup from '@/pages/signup/Signup';
import Test from '@/pages/test/Test';

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
        <Route path="/test" element={<Test />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/demo" element={<Demo />} />
      </Route>
    </Routes>
  );
};

export default App;
