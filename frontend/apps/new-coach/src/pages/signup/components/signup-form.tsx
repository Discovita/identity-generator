import { useRef, useState, useEffect } from 'react';

import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Link } from 'react-router-dom';
import { FaGoogle, FaApple, FaInfoCircle } from 'react-icons/fa';
import { PASSWORD_REGEX, EMAIL_REGEX } from '@/pages/signup/constants/constants';

export function SignupForm({ className, ...props }: React.ComponentProps<'div'>) {
  const emailRef = useRef<HTMLInputElement>(null);
  const errorRef = useRef(null);
  const [email, setEmail] = useState('');
  const [validEmail, setValidEmail] = useState(false); // whether the Email validates or not
  const [password, setPassword] = useState('');
  const [validPassword, setValidPassword] = useState(false); // whether the password validates or not
  const [matchPassword, setMatchPassword] = useState('');
  const [validMatch, setValidMatch] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [attemptedSubmit, setAttemptedSubmit] = useState(false); // whether the form has been submitted or not

  // This useEffect hook is used to automatically focus the email input field
  // when the component mounts. The empty dependency array [] ensures that this
  // effect runs only once after the initial render.
  useEffect(() => {
    emailRef.current?.focus();
  }, []);

  // This useEffect hook is used to validate the email input every time it
  // changes. The dependency array [email] ensures that this effect runs
  // whenever the 'email' state changes. The EMAIL_REGEX.test(email) checks if
  // the email input matches the defined regular expression. The result is then
  // used to update the 'validEmail' state.
  useEffect(() => {
    const result = EMAIL_REGEX.test(email);
    setValidEmail(result);
  }, [email]);

  // This useEffect hook is used to validate the password and its confirmation
  // every time they change. The dependency array [password, matchPassword]
  // ensures that this effect runs whenever either 'password' or 'matchPassword'
  // state changes. The PASSWORD_REGEX.test(password) checks if the password
  // input matches the defined regular expression. The result is then used to
  // update the 'validPassword' state. The password === matchPassword checks if
  // the password and its confirmation match. The result is then used to update
  // the 'validMatch' state.
  useEffect(() => {
    const result = PASSWORD_REGEX.test(password);
    setValidPassword(result); // sets if password is valid or not
    const match = password === matchPassword;
    setValidMatch(match); // sets if password and its confirmation match
  }, [password, matchPassword]);

  // This useEffect hook is used to clear the error message every time the email
  // input, password, or its confirmation changes. The dependency array [email,
  // password, matchPassword] ensures that this effect runs whenever either
  // 'email', 'password', or 'matchPassword' state changes. The
  // setErrorMessage('') clears the error message.
  useEffect(() => {
    setErrorMessage('');
  }, [email, password, matchPassword]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setAttemptedSubmit(true);
    const v1 = EMAIL_REGEX.test(email);
    const v2 = PASSWORD_REGEX.test(password);
    if (!v1 || !v2) {
      // setErrorMessage('Invalid Entry');
      return;
    }
    // Implement Create User Logic
  };
  return (
    <div className={cn('_SignupForm flex flex-col gap-6 mx-auto w-[450px]', className)} {...props}>
      <Card className="w-full">
        <CardHeader className="text-center">
          <CardDescription>Signup with your Apple or Google account</CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-6" method="POST" onSubmit={handleSubmit}>
            <div className="grid gap-6">
              <div className="flex flex-col gap-4">
                <Button variant="outline" className="w-full">
                  <FaApple />
                  Signup with Apple
                </Button>
                <Button variant="outline" className="w-full">
                  <FaGoogle />
                  Signup with Google
                </Button>
              </div>
              <div className="after:border-border relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t">
                <span className="bg-card text-muted-foreground relative z-10 px-2">
                  Or create an account with
                </span>
              </div>

              <div className="grid gap-2">
                <div className="grid gap-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="m@example.com"
                    required
                    ref={emailRef}
                    aria-invalid={validEmail ? 'false' : 'true'}
                    aria-describedby="emailnote"
                    onChange={e => setEmail(e.target.value)}
                  />
                </div>
                <div className="grid gap-2">
                  <div className="flex items-center">
                    <Label htmlFor="password">Password</Label>
                  </div>
                  <Input
                    name="password"
                    type={'password'}
                    id="password"
                    onChange={e => setPassword(e.target.value)}
                    required
                    aria-invalid={validPassword ? 'false' : 'true'}
                    aria-describedby="passwordnote"
                    showPasswordToggle
                  />
                </div>

                <div className="grid gap-2">
                  <div className="flex items-center">
                    <Label htmlFor="password">Confirm Password</Label>
                  </div>
                  <Input
                    name="confirm_password"
                    type={'password'}
                    id="confirm_password"
                    onChange={e => setMatchPassword(e.target.value)}
                    required
                    aria-invalid={validMatch ? 'false' : 'true'}
                    aria-describedby="confirmnote"
                    showPasswordToggle
                  />
                </div>

                <Button type="submit" className="w-full">
                  Signup
                </Button>
              </div>
              <div className="text-center text-sm">
                Already have an account?{' '}
                <Link to="/login" className="underline underline-offset-4">
                  Log in
                </Link>
              </div>
              <p
                ref={errorRef}
                className={errorMessage ? 'errmsg' : 'offscreen'}
                aria-live="assertive"
              >
                {errorMessage}
              </p>
              <div
                id="emailnote"
                className={`mt-3 flex gap-5 rounded-lg bg-neutral-100 p-3 text-left text-sm dark:bg-neutral-950 ${
                  attemptedSubmit && !validEmail ? '' : 'hidden'
                }`}
              >
                <FaInfoCircle className="mt-1 text-gold-600" aria-hidden="true" size={15} />
                <p>
                  Must start with alphanumeric, <span aria-label="dot">.</span> ,{' '}
                  <span aria-label="underscore">_</span> , <span aria-label="percent sign">%</span>{' '}
                  , <span aria-label="plus sign">+</span> , or <span aria-label="hyphen">-</span> .
                  <br />
                  Must contain @ symbol.
                  <br />
                  Must have alphanumeric, dot, or hyphen after @.
                  <br />
                  Must contain a dot after @.
                  <br />
                  Must end with two or more alphabets.
                </p>
              </div>
              <div
                id="passwordnote"
                className={`mt-3 flex items-start gap-4 rounded-lg border-l-4 border-gold-400 bg-gold-50 p-4 text-left text-sm shadow-sm dark:border-gold-600 dark:bg-gold-950 dark:text-gold-100 ${
                  attemptedSubmit && !validPassword ? '' : 'hidden'
                }`}
              >
                <FaInfoCircle className="mt-1 text-gold-600" aria-hidden="true" size={15} />
                <p>
                  Must be at 8 to 24 characters long.
                  <br />
                  Must contain at least one uppercase letter.
                  <br />
                  Must contain at least one lowercase letter.
                  <br />
                  Must contain at least one number.
                  <br />
                  Must contain at least one special character.
                  <br />
                  Allowed special characters are: <span aria-label="exclamation mark">!</span>
                  <span aria-label="at symbol">@</span>
                  <span aria-label="pound sign">#</span>
                  <span aria-label="dollar sign">$</span>
                  <span aria-label="percent sign">%</span>
                  <span aria-label="caret">^</span>
                  <span aria-label="ampersand">&</span>
                  <span aria-label="asterisk">*</span>
                </p>
              </div>
              <div
                id="confirmnote"
                className={`mt-3 flex items-start gap-4 rounded-lg border-l-4 border-gold-400 bg-gold-50 p-4 text-left text-sm shadow-sm dark:border-gold-600 dark:bg-gold-950 dark:text-gold-100 ${
                  attemptedSubmit && !validMatch ? '' : 'hidden'
                }`}
              >
                <FaInfoCircle className="mt-1 text-gold-600" aria-hidden="true" size={15} />
                <p>Passwords must match.</p>
              </div>
            </div>
          </form>
        </CardContent>
      </Card>
      <div className="text-muted-foreground *:[a]:hover:text-gold-500 text-center text-xs text-balance *:[a]:underline *:[a]:underline-offset-4">
        By clicking continue, you agree to our <Link to="#">Terms of Service</Link> and{' '}
        <Link to="#">Privacy Policy</Link>.
      </div>
    </div>
  );
}
