PROJECT_NAME=space_api
BACKEND_CONTAINER_NAME=django

build-docker:
	docker build -t $(PROJECT_NAME):build -f docker/Dockerfile --target build .

compile-requirements-file: build-docker
	docker run -v $$PWD:/project/app --rm $(PROJECT_NAME):build pip-compile --generate-hashes

upgrade-all-requirements: build-docker
	docker run -v $$PWD:/project/app --rm $(PROJECT_NAME):build pip-compile --generate-hashes --upgrade

upgrade-requirement: build-docker
	docker run -v $$PWD:/project/app --rm $(PROJECT_NAME):build pip-compile --generate-hashes --upgrade-package $(package)

manage:
	docker-compose run --rm $(BACKEND_CONTAINER_NAME) manage $(filter-out $@,$(MAKECMDGOALS))

lint:
	docker-compose run --rm $(BACKEND_CONTAINER_NAME) lint

format:
	docker-compose run --rm $(BACKEND_CONTAINER_NAME) fmt

test:
	docker-compose run --rm $(BACKEND_CONTAINER_NAME) test

%: #Ignore unknown commands (and extra parameters)
	@:
