from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError

import requests


def test_success_fetch():
    args = [10, False, False]
    result = call_command("fetch_cores", *args)
    assert result.startswith("[(")


def test_wrong_argument():
    args = ["test", False, False]
    try:
        call_command("fetch_cores", *args)
        assert False
    except CommandError:
        assert True


def test_results_count():
    args = [1000000, False, False]
    result = call_command("fetch_cores", *args)
    assert result.startswith("There are only")


@patch.object(requests, "post")
def test_unsuccessful_fetch(mock_request_post):
    r = requests.Response()
    r.status_code = 500
    mock_request_post.status_code = r.status_code
    args = [10, False, False]
    result = call_command("fetch_cores", *args)
    assert result == "Unable to fetch data from the API."
