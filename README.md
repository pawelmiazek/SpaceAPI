# SpaceAPI

## Technology

- Django
- django rest framework
- PostgreSQL
- requests

The reason of chosen technology is that they have good community support and official documentation. Additionaly these technologies are used in many companies around the world.

## Prequesites

- Due to compose file format 3.8 (Required Docker Engine release 19.03.0+)

## Development Setup

1. Create your own version of `env` by simply copying contents of `env.example`.

2. In root directory run `docker-compose up` to build the app.

## Task 1

1. Run `make manage fetch_cores {cores_count(int)} {exclude_unsuccessful(bool)} {exclude_upcoming(bool)}` to fetch list of cores.

## Task 2

1. Run `make manage create_test_users` to create 3 users for testing purposes.

2. API Schema: `/v1/docs/`.

## Tests

1. Write `make test` to run unit tests.