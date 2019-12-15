from rest_framework import serializers
from User.models import User

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','password','first_name','last_name','is_active','is_staff','is_superuser')
