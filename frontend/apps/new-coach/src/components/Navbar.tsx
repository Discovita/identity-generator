import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ThemeSwitcher } from '@/components/ThemeSwitcher';

/**
 * Navbar Component (Full Version)
 *
 * Renders a two-row navigation bar:
 * 1. Top row: Logo, contact info, and Login button.
 * 2. Bottom row: Main navigation links (Home, Company, Team, Features).
 *
 * - Uses shadcn/ui Button for the Login action.
 * - Uses react-router-dom Link for navigation.
 * - Includes ThemeSwitcher for theme toggling.
 * - All elements are styled with Tailwind and shadcn/ui conventions.
 * - 100% comment coverage for clarity and maintainability.
 */
export default function Navbar() {
  return (
    <nav className="_Navbar w-full">
      {/* Top navigation row: Logo, contact, login, theme switcher */}
      <div className="flex flex-wrap justify-between items-center mx-auto p-4 bg-white border-b border-gray-200 dark:bg-gray-900 dark:border-gray-800">
        {/* Logo and brand name */}
        <Link to="/" className="flex items-center space-x-3 rtl:space-x-reverse">
          {/* Brand name */}
          <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">
            Coach
          </span>
        </Link>
        {/* Contact info, Login button, ThemeSwitcher */}
        <div className="flex items-center space-x-6 rtl:space-x-reverse">
          {/* Login action as a shadcn/ui Button wrapped in Link */}
          <Link to="/login">
            <Button variant="link" className="text-blue-600 dark:text-blue-500 p-0 h-auto text-sm">
              Login
            </Button>
          </Link>
          <Link to="/login">
            <Button variant="link" className="text-blue-600 dark:text-blue-500 p-0 h-auto text-sm">
              Sign Up
            </Button>
          </Link>
          {/* Theme switcher for dark/light mode */}
          <ThemeSwitcher />
        </div>
      </div>
      {/* Bottom navigation row: Main page links */}
      <div className="bg-gray-50 dark:bg-gray-700">
        <div className="max-w-screen-xl px-4 py-3 mx-auto">
          <div className="flex items-center">
            {/* Main navigation links */}
            <ul className="flex flex-row font-medium mt-0 space-x-8 rtl:space-x-reverse text-sm">
              {/* Home link */}
              <li>
                <Link
                  to="/"
                  className="text-gray-900 dark:text-white hover:underline"
                  aria-current="page"
                >
                  Home
                </Link>
              </li>
              {/* Company link */}
              <li>
                <Link to="/company" className="text-gray-900 dark:text-white hover:underline">
                  Company
                </Link>
              </li>
              {/* Team link */}
              <li>
                <Link to="/team" className="text-gray-900 dark:text-white hover:underline">
                  Team
                </Link>
              </li>
              {/* Features link */}
              <li>
                <Link to="/features" className="text-gray-900 dark:text-white hover:underline">
                  Features
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>
  );
}
