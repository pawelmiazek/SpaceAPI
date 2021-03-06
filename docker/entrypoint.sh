#!/bin/sh
set -e

MANAGE_CMD='python src/manage.py'

if [ "$1" = 'manage' ]; then
    shift
    exec ${MANAGE_CMD} $@
elif [ "$1" = 'runserver' ]; then
    shift
    exec ${MANAGE_CMD} runserver 0.0.0.0:8000 $@
elif [ "$1" = 'uwsgi' ]; then
    shift
    exec uwsgi --ini=/project/app/docker/uwsgi.ini $@
elif [ "$1" = 'test' ]; then
    shift
    exec pytest $@
elif [ "$1" = 'djangotest' ]; then
    shift
    exec ${MANAGE_CMD} test src/ $@
elif [ "$1" = 'lint' ]; then
    shift
    OPTS=${@:-'.'}
    echo "-- black --" && black --check --diff $OPTS || EXIT=$?
    echo "-- isort --" && isort -c --diff $OPTS || EXIT=$?
    echo "-- flake8 --" && flake8 $OPTS || EXIT=$?
    MYPY_OPTS=${@:-'src/'}
    echo "-- mypy --" && mypy $MYPY_OPTS || EXIT=$?
    exit ${EXIT:-0}
elif [ "$1" = 'fmt' ]; then
    shift
    OPTS=${@:-'.'}
    echo "-- black --" && black $OPTS
    echo "-- isort --" && isort --atomic $OPTS
    exit 0
fi

exec "$@"
