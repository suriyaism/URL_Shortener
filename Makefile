build:
	docker-compose build url-shortener

start:
	docker-compose up

test:
	docker-compose run --rm url-shortener python -m unittest
