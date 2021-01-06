FROM node:12.19.0-alpine3.10 as react_builder

WORKDIR /usr/src/app
COPY front-end/ .
RUN npm install && npm run build

FROM nginx:1.19.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY docker/nginx.conf /etc/nginx/conf.d
COPY --from=react_builder /usr/src/app/build/ /usr/src/app/
