# Welcome to My Favorite Things!

Hello there! This is the favorite-things application, written using a Bootstrap-Vue user interface, and supported by a Python Django Web Server. Docker is used to containerize the python server code, as well as the front-end build process, and the Postgresql database. These technologies working together make deployment of the favorite-things application hassle free!

# Tech Stack

#### Serving Technologies
* Docker version 18.03.0
* python 3.7.4
* postgres

### Building UX Source
For production release:
```sh
$ cd favorite-things
$ cd app/favoritethings/ux
$ yarn build
```

### Docker Deployment
Starting to application via containers.

```sh
cd favorite-things
docker-compose up --build
```
