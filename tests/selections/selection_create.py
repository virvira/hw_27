import pytest

from ads.models import Selection
from tests.factories import AdFactory


@pytest.mark.django_db
def test_selection_create(client, user, access_token):
    ad_list = AdFactory.create_batch(3)

    data = {
        "items": [ad.pk for ad in ad_list],
        "name": "Подборка Васи",
        "owner": user.pk
    }

    expected_response = {
        "id": 1,
        "items": [ad.pk for ad in ad_list],
        "name": "Подборка Васи",
        "owner": user.pk
    }

    # {
    #     "id": 29,
    #     "items": [
    #         1,
    #         2
    #     ],
    #     "name": "Подборка Васи",
    #     "owner": 19
    # }
    response = client.post(
        '/selection/create/',
        data,
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Bearer + {access_token}'
    )
    assert response.status_code == 201
    assert response.data == expected_response
