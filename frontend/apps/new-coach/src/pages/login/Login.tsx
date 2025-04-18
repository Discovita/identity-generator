import { LoginForm } from '@/components/login-form';
import { motion } from 'framer-motion';
function Login() {
  return (
    <div className="_Login text-center mb-12">
      <motion.h1
        className="text-gold-700 text-2xl font-bold tracking-tight sm:text-4xl mb-4"
        key="login-text"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.8 }}
      >
        Login to Your Account
      </motion.h1>
      <motion.div
        key="login-form"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.8 }}
      >
        <LoginForm />
      </motion.div>
    </div>
  );
}

export default Login;
