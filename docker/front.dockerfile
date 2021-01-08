FROM node:12.19.0-alpine3.10 as react_builder

# Install node modules first, without copying all files
# This allow to cache the install step
COPY front-end/package.json /tmp/
RUN cd /tmp && npm install

WORKDIR /usr/src/app
RUN cp -a /tmp/node_modules .
COPY ./front-end/ .
RUN npm run build

FROM nginx:1.19.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY docker/nginx.conf /etc/nginx/conf.d
COPY --from=react_builder /usr/src/app/build/ /usr/src/app/
