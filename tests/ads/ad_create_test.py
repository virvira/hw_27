import pytest

from ads.models import Advertisement


@pytest.mark.django_db
def test_ad_create(client, user, category):
    data = {
        "name": "Сибирская котята, 3 месяца",
        "price": 2500,
        "category": category.name,
        "author": user.username,
        "description": "Продаю сибирских котят, возраст 3 месяца",
        "is_published": True
    }

    expected_response = {
            "id": 1,
            "category": category.name,
            "author": user.username,
            "is_published": True,
            "name": "Сибирская котята, 3 месяца",
            "price": 2500,
            "description": "Продаю сибирских котят, возраст 3 месяца"
    }

    response = client.post(
        '/ad/create/',
        data,
        content_type='application/json'
    )
    assert response.status_code == 201
    assert response.data == expected_response
