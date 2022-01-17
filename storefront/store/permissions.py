from rest_framework.permissions import BasePermission, SAFE_METHODS, DjangoModelPermissions


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # get, head, options
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class FullDjangoModelPermissions(DjangoModelPermissions):
    # reference error
    # perms_map['GET'] = ['%(app_label)s.get_%(model_name)s']
    def __init__(self):
        # to access the database record, the user needs to have the
        # corresponding permissions
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


# add hard permissions to a single user is not a good practice
# it's better to use groups,
# with group, we can filter to see who have which permissions
# don't have filter for permissions only have filter for groups
class ViewCustomerHistoryPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history')

# create custom model permissions in the Model Meta
# assign permissions to some users in admin panel
# create custom permissions for endpoints
