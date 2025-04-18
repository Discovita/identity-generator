import { useContext, useRef, useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import RegisterEmoji from '@/assets/images/register-emoji.png';
import { Link } from 'react-router-dom';
import { FaInfoCircle, FaCheck, FaTimes } from 'react-icons/fa';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import { AuthContext } from '@/providers/AuthProvider';
import { useNavigate } from 'react-router-dom';
import { inputClasses } from '@/utils/contstants';

// This regular expression validates an email address.
// It checks for:
// - One or more alphanumeric characters, dots, underscores, percent signs, plus signs, or hyphens at the start (before the @ symbol)
// - Followed by the @ symbol
// - Followed by one or more alphanumeric characters, dots, or hyphens
// - Followed by a dot
// - Ending with two or more alphabetic characters
const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{8,24}$/;
// const USERNAME_REGEX = /^[a-zA-Z][a-zA-Z0-9-_]{3,23}$/;

const RegisterForm = () => {
  const emailRef = useRef(null);
  const errorRef = useRef(null);
  const [email, setEmail] = useState('');
  const [validEmail, setValidEmail] = useState(false); // whether the Email validates or not
  const [emailFocus, setEmailFocus] = useState(false); // whether the name input is focused or not
  const [password, setPassword] = useState('');
  const [validPassword, setValidPassword] = useState(false); // whether the password validates or not
  const [passwordFocus, setPasswordFocus] = useState(false); // whether the password input is focused or not
  const [matchPassword, setMatchPassword] = useState('');
  const [validMatch, setValidMatch] = useState(false);
  const [matchFocus, setMatchFocus] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const { createUser, user } = useContext(AuthContext);
  const navigate = useNavigate();

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

  const handleSubmit = async event => {
    event.preventDefault();
    const v1 = EMAIL_REGEX.test(email);
    const v2 = PASSWORD_REGEX.test(password);
    if (!v1 || !v2) {
      setErrorMessage('Invalid Entry');
      return;
    }
    try {
      createUser(email, password);
    } catch (error) {
      // Handle error here
      errorRef.current?.focus();
    }
  };

  useEffect(() => {
    if (user !== null) {
      navigate('/');
    }
  }, [user, navigate]);

  return (
    <motion.section
      className="_RegisterForm mt-10"
      key="register"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.8 }}
    >
      <div className="flex min-h-full flex-col justify-center px-6 py-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <motion.div
            className="m-auto flex justify-center"
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 1, delay: 0.5 }}
          >
            <img src={RegisterEmoji} className="h-72 w-72" />
          </motion.div>
        </div>
        <h2 className="mt-4 text-center text-2xl font-bold leading-9 tracking-tight ">Register</h2>
        <p ref={errorRef} className={errorMessage ? 'errmsg' : 'offscreen'} aria-live="assertive">
          {errorMessage}
        </p>
        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form className="space-y-6" method="POST" onSubmit={handleSubmit}>
            <div>
              <label htmlFor="email" className="block text-left text-sm font-medium leading-6">
                Email Address:
                <span>
                  <FaCheck
                    className={validEmail ? 'mb-1 ml-4 inline-block text-green-600' : 'hidden'}
                    aria-hidden="true"
                  />
                </span>
                <span>
                  <FaTimes
                    className={validEmail || !email ? 'hidden' : 'ml-4 inline-block text-red-600'}
                    aria-hidden="true"
                  />
                </span>
              </label>

              <input
                name="email"
                type="email"
                id="email"
                ref={emailRef}
                onChange={e => setEmail(e.target.value)}
                required
                aria-invalid={validEmail ? 'false' : 'true'}
                aria-describedby="emailnote"
                onFocus={() => setEmailFocus(true)}
                onBlur={() => setEmailFocus(false)}
                className={`${inputClasses} mt-2`}
              />
              <div
                id="emailnote"
                className={`mt-3 flex gap-5 rounded-lg bg-neutral-100 p-3 text-left text-sm dark:bg-neutral-950 ${
                  emailFocus && email && !validEmail ? '' : 'hidden'
                }`}
              >
                <FaInfoCircle className="mt-1" aria-hidden="true" size={15} />
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
            </div>

            <div>
              <label htmlFor="password" className="block text-left text-sm font-medium leading-6">
                Password:
                <span>
                  <FaCheck
                    className={validPassword ? 'mb-1 ml-4 inline-block text-green-600' : 'hidden'}
                    aria-hidden="true"
                  />
                </span>
                <span>
                  <FaTimes
                    className={
                      validPassword || !password ? 'hidden' : 'ml-4 inline-block text-red-600'
                    }
                    aria-hidden="true"
                  />
                </span>
              </label>

              <div className="relative flex">
                <input
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  onChange={e => setPassword(e.target.value)}
                  required
                  aria-invalid={validPassword ? 'false' : 'true'}
                  aria-describedby="passwordnote"
                  onFocus={() => setPasswordFocus(true)}
                  onBlur={() => setPasswordFocus(false)}
                  className={`${inputClasses} mt-2`}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-2 top-1/2 mt-1 -translate-y-1/2 transform text-sm leading-5"
                >
                  {showPassword ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
              <div
                id="passwordnote"
                className={`mt-3 flex gap-5 rounded-lg bg-neutral-100 p-3 text-left text-sm dark:bg-neutral-950 ${
                  passwordFocus && password && !validPassword ? '' : 'hidden'
                }`}
              >
                <FaInfoCircle className="mt-1" aria-hidden="true" size={15} />
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
            </div>

            <div>
              <div>
                <label
                  htmlFor="confirm_password"
                  className="block text-left text-sm font-medium leading-6"
                >
                  Confirm Password:
                  <span>
                    <FaCheck
                      className={
                        validMatch && matchPassword
                          ? 'mb-1 ml-4 inline-block text-green-600'
                          : 'hidden'
                      }
                      aria-hidden="true"
                    />
                  </span>
                  <span>
                    <FaTimes
                      className={
                        validMatch || !matchPassword ? 'hidden' : 'ml-4 inline-block text-red-600'
                      }
                      aria-hidden="true"
                    />
                  </span>
                </label>
              </div>

              <div className="relative flex">
                <input
                  name="confirm_password"
                  type={showPassword ? 'text' : 'password'}
                  id="confirm_password"
                  onChange={e => setMatchPassword(e.target.value)}
                  required
                  aria-invalid={validMatch ? 'false' : 'true'}
                  aria-describedby="confirmnote"
                  onFocus={() => setMatchFocus(true)}
                  onBlur={() => setMatchFocus(false)}
                  className={`${inputClasses} mt-2`}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-2 top-1/2 mt-1 -translate-y-1/2 transform text-sm leading-5"
                >
                  {showPassword ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
              <div
                id="confirmnote"
                className={`mt-3 flex gap-5 rounded-lg bg-neutral-100 p-3 text-left text-sm dark:bg-neutral-950 ${
                  matchFocus && matchPassword && !validMatch ? '' : 'hidden'
                }`}
              >
                <FaInfoCircle className="mt-1" aria-hidden="true" size={15} />
                <p>Passwords must match.</p>
              </div>
            </div>

            <div>
              <button
                type="submit"
                className={`flex w-full justify-center rounded-md bg-violet-500 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-violet-400 focus-visible:outline-violet-500 dark:bg-violet-500 dark:hover:bg-violet-400 dark:focus-visible:outline-violet-500 ${
                  !validEmail || !validPassword || !validMatch ? 'cursor-not-allowed' : ''
                }`}
                onClick={handleSubmit}
              >
                Sign Up
              </button>
            </div>
          </form>
          <p className="mt-5 text-center text-sm text-neutral-500">
            Already registered?
            <Link
              to="/login"
              className="font-semibold leading-6 text-violet-500 hover:text-violet-400 dark:text-violet-600 dark:hover:text-violet-500"
            >
              {' '}
              Sign In.
            </Link>
          </p>
        </div>
      </div>
    </motion.section>
  );
};

export default RegisterForm;
