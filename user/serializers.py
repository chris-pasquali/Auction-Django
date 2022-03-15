from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
  # username = serializers.SerializerMethodField(read_only=True)
  first_name = serializers.CharField(required=False, write_only=True)
  last_name = serializers.CharField(required=False, write_only=True)
  name = serializers.CharField(source='get_full_name', read_only=True)
  password = serializers.CharField(
    required=True, write_only=True, style={'input_type': 'password'},
  )

  class Meta:
    model = User
    fields = (
      'id',
      'name',
      'first_name',
      'last_name',
      'email',
      'username',
      'password',
      'profile_picture',
      'is_active',
      'is_staff',
      'is_admin'
    )

class UserListSerializer(serializers.ModelSerializer):
  name = serializers.CharField(source='get_full_name')

  class Meta:
    model = User
    fields = ['username', 'profile_picture', 'name']


class RegistrationSerializer(serializers.ModelSerializer):
  password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

  class Meta:
    model = User
    fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password2']
    extra_kwargs = {
      'password': {'write_only': True},
    }
  
  def save(self):
    user = User(
      email=self.validated_data['email'],
      username=self.validated_data['username'],
      first_name=self.validated_data['first_name'],
      last_name=self.validated_data['last_name']
    )
    password = self.validated_data['password']
    password2 = self.validated_data['password2']

    if password != password2:
      raise serializers.ValidationError({'password': 'Passwords must match.'})
    
    user.set_password(password)
    user.save()
    return user