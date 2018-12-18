
## Install from scratch!

Firstly, install requirements down below:

- [Docker](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com) 

##### Git clone

	git clone https://github.com/jairojair/emeeting.git

##### Setup

	cd emeeting

	docker-compose build
	docker-compose run app make migrate
	docker-compose run app make tests

##### Run

	docker-compose up

Access: [http://0.0.0.0:8000](http://0.0.0.0:8000) for see the API documentation.
