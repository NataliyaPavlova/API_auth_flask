.PHONY: help up stop build clean

help:
	@echo "Docker Compose Help"
	@echo "-----------------------"
	@echo ""
	@echo "To up containers from docker-compose.yml:"
	@echo "    make up"
	@echo ""
	@echo "To build:"
	@echo "    make build"
	@echo ""
	@echo "Really, really start over:"
	@echo "    make clean"
	@echo ""
	@echo "Run tests locally:"
	@echo "    make test"
	@echo ""

up:
	@docker-compose -f docker-compose.yml up -d

stop:
	@docker-compose stop

build:
	@docker-compose up --build

clean: stop
	@docker-compose rm --force
	@find . -name \*.pyc -delete

test:
	@echo "Run tests"
	pytest -svvv -rs tests/views
