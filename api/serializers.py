from rest_framework.serializers import ModelSerializer, CharField
from .models import Expense
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ['username', 'password']


class ExpenseSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
