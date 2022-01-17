from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers


class UserCreateSerializer(DjoserUserCreateSerializer):
    # class Meta:
    #     model = User
    #     fields = tuple(User.REQUIRED_FIELDS) + (
    #         settings.LOGIN_FIELD, # email
    #         settings.USER_ID_FIELD, # username
    #         "password",
    #     )

    class Meta(DjoserUserCreateSerializer.Meta):
        # birth_date = serializers.DateField()
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email',
                  'password',
                  # password is not shown
                  # 'birth_date',
                  ]
        # all the fields included here must be defined in the default user table
        # we could define some fields that doesn't exist in the user table
        # but it's not a good practice

        # On the frontend, we can have a form capturing some fields for user, and
        # some fields for profile, and the client should send two separate requests
        # to the backend. The first request is to create the user account. And the
        # second is to update the profile.


class UserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserSerializer.Meta):
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email',
                  # 'password',
                  # password is shown, comment it
                  # 'birth_date',
                  ]
