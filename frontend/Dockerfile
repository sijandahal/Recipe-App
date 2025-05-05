FROM node:16
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
ENV NODE_ENV=production
ENV REACT_APP_BACKEND_URL=http://172.19.0.5:5000
CMD ["npm", "start"]
