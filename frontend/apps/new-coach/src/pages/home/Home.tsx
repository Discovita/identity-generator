import { motion } from 'framer-motion';
import Markdown from 'react-markdown';

const markdown = '# Hi, *Pluto*!';
function Home() {
  return (
    <motion.div
      className="_Home text-center mb-12"
      key="home"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.8 }}
    >
      <h1 className="text-gold-700 text-2xl font-bold sm:text-4xl">Welcome to the Coach</h1>
      <Markdown>{markdown}</Markdown>
    </motion.div>
  );
}

export default Home;
