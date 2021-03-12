FROM node:lts-alpine

WORKDIR /app

RUN apk update && \
    npm install -g npm && \
    npm install -g @vue/cli

EXPOSE 8080
# ENTRYPOINT ["npm","run","dev"]