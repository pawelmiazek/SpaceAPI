from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from cores.models import Core


User = get_user_model()


@pytest.fixture
def test_user(db):
    user = User.objects.create(
        username="test",
        email="test_email@mail.com",
        password="test_password",
        is_staff=True,
        is_superuser=True,
    )
    return user


@pytest.fixture
def api_client(db, test_user):
    token = RefreshToken.for_user(test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(token.access_token))
    return client


@pytest.mark.django_db
def test_users_endpoint(api_client):
    url = reverse("user-list")

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("count", 0) == 1


@pytest.mark.django_db
def test_users_me_endpoint(api_client):
    url = reverse("user-me")

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_users_set_core(api_client, test_user):
    core = Core.objects.create(api_id="B10490")
    data = {"core_id": core.id}
    url = reverse("user-detail", kwargs={"pk": test_user.pk})

    response = api_client.patch(url, data=data)
    assert response.status_code == status.HTTP_200_OK
    assert test_user in core.users.all()


@pytest.mark.django_db
def test_empty_cores_endpoint(api_client):
    url = reverse("core-list")

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("count", 0) != 0


@pytest.mark.django_db
def test_not_empty_cores_endpoint(api_client):
    Core.objects.create(api_id="B10490")
    url = reverse("core-list")

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("count", 0) == 1
