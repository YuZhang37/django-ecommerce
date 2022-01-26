
from store.models import Product

# Preload related objects
Product.objects.select_related('...')
Product.objects.prefetch_related('...')

# Load only what you need
Product.objects.only('name')
Product.objects.defer('description')

# Use values
# initializing a dict or a list is cheaper than initializing a model,
# if don't need model methods like create or update or delete, we can use
# values or values_list
Product.objects.values() # get a dict
Product.objects.values_list() # get a list

# count properly
Product.objects.count()
len(Product.objects.all()) # BAD, pull all instances in memory and count

# Bulk create/update
Product.objects.bulk_create([])

