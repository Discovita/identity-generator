import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Link } from 'react-router-dom';
import { FaGoogle, FaApple } from 'react-icons/fa';

/**
 * LoginForm Component
 * ------------------
 * Renders a login form with social login options, email/password fields, and links.
 * Fully styled for both light and dark themes using Tailwind and custom theme variables.
 *
 * Usage: Place inside a page for authentication.
 */
export function LoginForm({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div className={cn('_LoginForm flex flex-col gap-6 mx-auto w-[450px]', className)} {...props}>
      {/* Card container with adaptive background and shadow for dark mode */}
      <Card className="w-full bg-card dark:bg-gold-400 shadow-gold-sm dark:shadow-gold-md border border-border dark:border-gold-700">
        <CardHeader className="text-center">
          <CardTitle className="text-xl text-gold-900 dark:text-gold-100">Welcome back</CardTitle>
          <CardDescription className="text-muted-foreground dark:text-gold-200">
            Login with your Apple or Google account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form>
            <div className="grid gap-6">
              <div className="flex flex-col gap-4">
                <Button
                  variant="outline"
                  className="w-full bg-white dark:bg-gold-700/90 dark:text-gold-50 border border-border dark:border-gold-600 hover:dark:bg-gold-600/90"
                >
                  <FaApple className="mr-2" />
                  Login with Apple
                </Button>
                <Button
                  variant="outline"
                  className="w-full bg-white dark:bg-gold-700/90 dark:text-gold-50 border border-border dark:border-gold-600 hover:dark:bg-gold-600/90"
                >
                  <FaGoogle className="mr-2" />
                  Login with Google
                </Button>
              </div>
              {/* Divider with adaptive color */}
              <div className="after:border-border relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t dark:after:border-gold-700">
                <span className="text-muted-foreground dark:text-gold-200 relative z-10 px-2 bg-gold-50 dark:bg-gold-400">
                  or continue with
                </span>
              </div>
              {/* Email/password fields with gold highlights in dark mode */}
              <div className="grid gap-6">
                <div className="grid gap-3">
                  <Label htmlFor="email" className="text-gold-900 dark:text-gold-100">
                    Email
                  </Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="m@example.com"
                    required
                    className="bg-background dark:bg-gold-700/40 border border-border dark:border-gold-600 text-foreground dark:text-gold-50 placeholder:text-muted-foreground dark:placeholder:text-gold-300 focus:ring-2 focus:ring-gold-500"
                  />
                </div>
                <div className="grid gap-3">
                  <div className="flex items-center">
                    <Label htmlFor="password" className="text-gold-900 dark:text-gold-100">
                      Password
                    </Label>
                    <a
                      href="#"
                      className="ml-auto text-sm underline-offset-4 hover:underline text-gold-700 dark:text-gold-200 hover:dark:text-gold-100"
                    >
                      Forgot your password?
                    </a>
                  </div>
                  <Input
                    id="password"
                    type="password"
                    required
                    className="bg-background dark:bg-gold-700/40 border border-border dark:border-gold-600 text-foreground dark:text-gold-50 placeholder:text-muted-foreground dark:placeholder:text-gold-300 focus:ring-2 focus:ring-gold-500"
                  />
                </div>
                <Button
                  type="submit"
                  className="w-full bg-gold-500 hover:bg-gold-600 text-white dark:bg-gold-700 dark:hover:bg-gold-600 dark:text-gold-50 font-semibold shadow-gold-md"
                >
                  Login
                </Button>
              </div>
              {/* Signup link with gold hover in dark mode */}
              <div className="text-center text-sm text-muted-foreground dark:text-gold-200">
                Don&apos;t have an account?{' '}
                <Link
                  to="/signup"
                  className="underline underline-offset-4 hover:text-gold-700 dark:hover:text-gold-300"
                >
                  Sign up
                </Link>
              </div>
            </div>
          </form>
        </CardContent>
      </Card>
      {/* Terms and privacy links with gold hover in dark mode */}
      <div className="text-muted-foreground dark:text-gold-300 *:[a]:hover:text-gold-500 dark:*:[a]:hover:text-gold-200 text-center text-xs text-balance *:[a]:underline *:[a]:underline-offset-4">
        By clicking continue, you agree to our <Link to="#">Terms of Service</Link> and{' '}
        <Link to="#">Privacy Policy</Link>.
      </div>
    </div>
  );
}
