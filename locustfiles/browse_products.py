import random

from locust import HttpUser, task, between

# In the homepage, hostname means where to find the server
# hostname: http://localhost:8000 not 81
# because the locust package is running in the virtual machine
# localhost would mean the machine the locust is current running

# when we run a performance test,
# locust will create an instance of this class for each simulated user
# the on_start will be executed for each instance before tasks
# and executes the tasks we define for this class

# how could a parent class knows a child class?
# the @task may provide some information
# about which child class should be picked up
# no
# when we run this module, the runtime should collection class information

class WebUser(HttpUser):
    # viewing products
    # viewing product details
    # adding product to cart

    wait_time = between(1, 5)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.cart_id = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cart_id = None

    @task(2)
    def view_products(self):
        # print('view products')
        collection_id = random.randint(2, 6)
        self.client.get(
            f'store/products/?collection_id={collection_id}',
            name='store/products/'
        )
        # name is used to group urls together in the report,
        # otherwise, each url will have a separate line in the report

    @task(4)
    def view_product(self):
        # print('view product details')
        product_id = random.randint(1, 1000)
        self.client.get(
            f'store/products/{product_id}/',
            name='store/products/:id',
        )

    @task(1)
    def add_product_to_cart(self):
        # print('add product to cart')
        product_id = random.randint(1, 10)
        self.client.post(
            f'store/carts/{self.cart_id}/items/',
            name='store/carts/items',
            json={'product_id': product_id, 'quantity': 1}
        )

    @task
    def say_hello7(self):
        self.client.get(
            'playground/hello7/',
            name='hello7',
        )

    def on_start(self):
        # different packages define different response objects
        # that returns from the client request
        response = self.client.post('store/carts/')
        # print('response', response)
        result = response.json()
        # print('result', result)
        self.cart_id = result['id']
