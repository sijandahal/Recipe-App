const isDevelopment = process.env.NODE_ENV === 'development';

const config = {
  backendUrl: isDevelopment ? 'http://localhost:5000' : 'http://172.19.0.5:5000'
};

export default config; 