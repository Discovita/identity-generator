import { LoginForm } from '@/components/login-form';
function Home() {
  return (
    <div className="w-72">
      <div className="text-center mb-12">
        <h1 className="text-2xl font-bold tracking-tight sm:text-4xl mb-4">
          Welcome to the Coach Website
        </h1>
      </div>
      <div className="">
        <LoginForm />
      </div>
    </div>
  );
}

export default Home;
