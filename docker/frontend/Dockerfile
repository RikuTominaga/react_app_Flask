FROM node:latest
WORKDIR /frontend

COPY package.json .
RUN npm install

COPY /src /frontend/src
COPY /public /frontend/public

CMD ["npm", "start"]
