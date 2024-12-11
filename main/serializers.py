from rest_framework import serializers
from .models import User, Ticket

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

class TicketSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    assigned_to = serializers.StringRelatedField(many=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description', 'status', 'response',
            'created_by', 'assigned_to', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        # Conditionally set title and description as not required for updates
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields['title'].required = False
            self.fields['description'].required = False

    def validate(self, data):
        # Ensure title and description are required only during creation
        if not self.instance:  # Only enforce validation for title and description during creation
            if not data.get('title'):
                raise serializers.ValidationError({"title": "This field is required."})
            if not data.get('description'):
                raise serializers.ValidationError({"description": "This field is required."})
        return data

    def update(self, instance, validated_data):
        # Preserve the existing title and description if they are not provided in the request
        if 'title' not in validated_data:
            validated_data['title'] = instance.title
        if 'description' not in validated_data:
            validated_data['description'] = instance.description

        return super().update(instance, validated_data)