from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from core.models import User
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem


# define the inline form
# tabular inline used for generic objects
class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']
    extra = 0


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline] + ProductAdmin.inlines


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # add_fieldsets: the fields we see when register a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2',
                       'email', 'first_name', 'last_name'),
        }),
        # email is required because we set it to be unique
        # username and password1 and password2 are required because of the
        # User Model default implementation
    )
    search_fields = ('first_name', 'last_name')

