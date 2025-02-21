interface Config {
  enableTestStates: boolean
  apiBaseUrl: string
}

// Default to enabled in development, disabled in production
const isProduction = process.env.NODE_ENV === 'production'

const config: Config = {
  enableTestStates: !isProduction,
  apiBaseUrl: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1'
}

// Debug configuration loading
console.log('Loading configuration:', {
  rawEnableTestStates: process.env.REACT_APP_ENABLE_TEST_STATES,
  parsedEnableTestStates: config.enableTestStates,
  rawApiBaseUrl: process.env.REACT_APP_API_BASE_URL,
  parsedApiBaseUrl: config.apiBaseUrl
})

export default config
