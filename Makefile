#!make

build:
	sudo -E docker-compose build

up-prod:
	sudo -E docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d