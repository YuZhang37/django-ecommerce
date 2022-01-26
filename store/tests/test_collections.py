import pytest
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from core.models import User

# when running tests, a temporary database 'test_storefront' is created
# when all tests are done, the 'test_storefront' is destroyed

# fixtures specific to this module are defined here.
# if the fixtures need to take arguments, replace with a closure
# it's like decorators needing to take arguments, replace with a closure
# decorators can supply the parameters when first time called
# fixtures are supplied parameters later.

# <when doing authenticated users, the create_collection is using an anonymous user
# why it still passes the test?>

# the argument client is a safe guarantee, to get a client object.
# if the calling scope has an object client, then that object is referred to,
# otherwise the safe client is referred to.
# or
# the argument client is always referring to client object since it's a constant
# the second understanding is correct
from store.models import Collection


@pytest.fixture
def create_collection(client):
    # the arguments create_collection takes will go to do_create_collection
    # because this fixture is executed before tests and evaluates to a function
    # print('create_collection is executed')
    def do_create_collection(title):
        # print('username:', client.handler._force_user)
        return client.post('/store/collections/', title)
    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        # Arrange
        # Act
        response = create_collection({'title': 'a'})
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # test authenticated users
    def test_if_user_is_auth_not_admin_returns_403(self, authenticate, create_collection):
        # Arrange
        authenticate()
        # Act
        response = create_collection({'title': 'a'})
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_invalid_data_returns_400(self, authenticate, create_collection):
        # Arrange
        authenticate(True)
        # Act
        response = create_collection({'title': ''})
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_user_is_admin_valid_data_returns_201(self, authenticate, create_collection):
        # Arrange
        authenticate(True)
        # Act
        response = create_collection({'title': 'a'})
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        # just check the id, if a record is created, it should return an id > 0
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:

    def test_if_collection_exists_return_200(self, client):
        # arrange
        # not good, because if post endpoint is not working,
        # this retrieve test also fails even it works fine
        # client.post('store/collections/', {'title':'a'}) or
        # go into implementation details for this test, we have to compromise
        # Collection.objects.create(title='a')
        collection = baker.make(Collection)
        # act
        response = client.get(f'/store/collections/{collection.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == collection.id
        assert response.data['title'] == collection.title




#
# @pytest.mark.django_db
# class TestCreateCollection:
#     # def test_authentication(self, client, create_collection):
#     # title = {'title': 'a'}
#     # response1 = client.post('/store/collections/', title)
#     # print('status 1', response1.status_code)
#     # print('username 1', client.handler._force_user)
#     # client.force_authenticate(user=User(username='Marvin'))
#     # response2 = client.post('/store/collections/', title)
#     # print('status 2', response2.status_code)
#     # print('username 2', client.handler._force_user)
#     # client2 = APIClient()
#     # response3 = client2.post('/store/collections/', title)
#     # print('status 3', response3.status_code)
#     # print('username 3', client2.handler._force_user)
#
#     # this proves that force_authenticate only applies to
#     # the user instance which calls this method
#
#     # client1 = APIClient()
#     # title = {'title': 'a'}
#     # response1 = create_collection(title=title)
#     # print('status: ', response1.status_code)
#     #
#     # client1.force_authenticate(user=User(username='Marvin'))
#     # response2 = create_collection(title=title)
#     # print('status: ', response2.status_code)
#
#     # some understandings:
#     # fixtures can only take fixtures as arguments
#     # fixtures are executed before each individual test, all fixtures define a variable pool
#     # if a variable can't be got from the current scope, then the program refers
#     # to the variable pool to retrieve the object.
#
#
#     # @pytest.mark.skip
#     # def test_if_user_is_anonymous_returns_401(self, client, create_collection):
#     def test_if_user_is_anonymous_returns_401(self, create_collection):
#         print('test_if_user_is_anonymous_returns_401')
#         # Arrange
#         # Act
#         # client = APIClient()
#         # response = client.post('/store/collections/', {'title': 'a'})
#         response = create_collection({'title': 'a'})
#         # Assert
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         print('ends')
#
#     # test authenticated users
#     def test_if_user_is_auth_not_admin_returns_403(self, client, create_collection):
#         print('test_if_user_is_auth_not_admin_returns_403')
#         # Arrange
#         # Act
#         # client = APIClient()
#         # client.force_authenticate() not correct
#         # client.force_authenticate(user='Marvin') not correct
#         client.force_authenticate(user={})
#         # response = client.post('/store/collections/', {'title': 'a'})
#         response = create_collection({'title': 'a'})
#         # Assert
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         print('ends')
#
#     def test_if_user_is_admin_invalid_data_returns_400(self, client, create_collection):
#         print('test_if_user_is_admin_invalid_data_returns_400')
#         # Arrange
#         # Act
#         # client = APIClient()
#         client.force_authenticate(user=User(is_staff=True))
#         # field title: blank is false, not allowing empty value
#         # response = client.post('/store/collections/', {'title': ''})
#         response = create_collection({'title': ''})
#         # Assert
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['title'] is not None
#         print('ends')
#
#     def test_if_user_is_admin_valid_data_returns_201(self, client, create_collection):
#         print('test_if_user_is_admin_valid_data_returns_201')
#         # Arrange
#         # Act
#         # client = APIClient()
#         client.force_authenticate(user=User(is_staff=True))
#         # response = client.post('/store/collections/', {'title': 'a'})
#         response = create_collection({'title': 'a'})
#         # Assert
#         assert response.status_code == status.HTTP_201_CREATED
#         # just check the id, if a record is created, it should return an id > 0
#         assert response.data['id'] > 0
#         print('test4', response.data)
#         print('ends')
