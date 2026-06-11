from rest_framework import serializers
from .models import Payment, User

class PaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    course_title = serializers.ReadOnlyField(source='course.title', allow_null=True)
    lesson_title = serializers.ReadOnlyField(source='lesson.title', allow_null=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'user_email', 'payment_date', 'course', 'course_title',
                  'lesson', 'lesson_title', 'amount', 'payment_method']

class UserPaymentSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'city', 'avatar', 'payments']

