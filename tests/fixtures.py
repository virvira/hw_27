import pytest


@pytest.fixture
@pytest.mark.django_db
def access_token(client, django_user_model):
    username = "username_test"
    password = "qwerty"
    django_user_model.objects.create_user(username=username, password=password, role="moderator",
                                          email="test_mail@gmail.com")

    response = client.post("/user/token/", {"username": username, "password": password},
                           content_type="application/json")

    return response.data["access"]
