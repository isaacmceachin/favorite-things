FROM node:11 as ux_build

RUN groupadd -r nodejs && useradd -m -r -g nodejs -s /bin/bash nodejs

WORKDIR ./
RUN mkdir ux
COPY ./favoritethings/ux ./ux

RUN cd ./ux
RUN mkdir package
ADD ./favoritethings/ux/package*.json ./package
RUN cd package && yarn install
WORKDIR ./package

COPY ./favoritethings/ux ./

RUN yarn build
RUN rm -r node_modules

FROM python:3-alpine
MAINTAINER Harry Liang <blurrcat@gmail.com>

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  && pip install psycopg2 \
  && apk del build-deps

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

COPY --from=ux_build ./package/dist/js ./favoritethings/static/js
COPY --from=ux_build ./package/dist/css ./favoritethings/static/css
COPY --from=ux_build ./package/dist/index.html ./favoritethings/templates

#COPY --from=ux_build ./ux/package/dist/js ./favoritethings/static
#COPY --from=ux_build ./ux/package/dist/css ./favoritethings/static
#COPY --from=ux_build ./ux/package/dist/index.html ./favoritethings/templates

#CMD python manage.py collectstatic
CMD python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000
