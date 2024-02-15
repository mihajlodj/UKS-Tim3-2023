FROM node:16.14-alpine

WORKDIR /usr/src/app

COPY . .

RUN npm install

COPY . .

RUN npm run build

# CMD ["npm", "run", "serve"]



# WORKDIR /app

# COPY --chown=node:node package*.json ./

# RUN npm install

# COPY --chown=node:node . .

# USER node

# CMD ["npm", "run", "serve"]
