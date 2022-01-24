# fixtures we define here will be automatically loaded when it's referenced in
# the test_func parameter and return the result to the parameter
import pytest
from rest_framework.test import APIClient

# here we define fixtures that we can use across test modules.

# not pytest.fixture()
from core.models import User


@pytest.fixture
def client():
    # no self parameter
    api_client = APIClient()
    # print('api client is executed')
    return api_client


@pytest.fixture
def authenticate(client):
    def do_authenticate(is_staff=False):
        return client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate
