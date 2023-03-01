import pytest

from ads.serializers import AdDetailSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_detail(client):
    ad = AdFactory.create()

    response = client.get(f'/ad/{ad.pk}/')
    assert response.status_code == 200
    assert response.data == AdDetailSerializer(ad).data
