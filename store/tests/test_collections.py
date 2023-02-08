import pytest
from rest_framework import status
from store.models import Collection, Product
from model_bakery import baker

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection


VALID_DATA = {'title': 'a'}
INVALID_DATA = {'title': ''}


@pytest.mark.django_db
class TestCreateCollections:
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        response = create_collection(VALID_DATA)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, create_collection, authenticate):
        authenticate()
        response = create_collection(VALID_DATA)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_not_valid_return_400(self, create_collection, authenticate):
        authenticate(is_staff=True)
        response = create_collection(INVALID_DATA)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, create_collection, authenticate):
        authenticate(is_staff=True)
        response = create_collection(VALID_DATA)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_return_200(self, api_client):
        collection = baker.make(Collection)
        baker.make(Product, collection=collection, _quantity=10)
        response = api_client.get(f'/store/collections/{collection.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0,
        }