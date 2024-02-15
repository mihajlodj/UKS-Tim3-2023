FROM node:16.14-alpine

WORKDIR /usr/src/app

COPY . .

RUN npm install

COPY . .

RUN npm run build