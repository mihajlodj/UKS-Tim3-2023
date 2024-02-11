FROM node:16.14.2

WORKDIR /vue

COPY package*.json ./

RUN npm install

COPY . .

CMD ["npm", "run", "serve"]
