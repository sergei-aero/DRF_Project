from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Payment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'city', 'avatar', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class PaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    course_title = serializers.ReadOnlyField(source='course.title', allow_null=True)
    lesson_title = serializers.ReadOnlyField(source='lesson.title', allow_null=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'user_email', 'payment_date', 'course', 'course_title',
                  'lesson', 'lesson_title', 'amount', 'payment_method']
