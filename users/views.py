from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers_jwt import MyTokenObtainPairSerializer
from .serializers import UserSerializer, PaymentSerializer
from django.shortcuts import get_object_or_404
from .models import Payment, Subscription
from materials.models import Course, Lesson
from .models import Payment
from .payment_service import (
    create_stripe_product,
    create_stripe_price,
    create_checkout_session,
    retrieve_checkout_session,
)
from decimal import Decimal

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)

class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({'error': 'course_id обязателен'}, status=400)

        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)
        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({"message": message})

class PaymentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course_id')
        lesson_id = request.data.get('lesson_id')

        if not course_id and not lesson_id:
            return Response(
                {'error': 'Необходимо указать course_id или lesson_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Определяем объект и сумму (можно брать из модели, если есть поле price)
        if course_id:
            obj = get_object_or_404(Course, id=course_id)
            amount = Decimal('100.00')   # пример, можно хранить в модели
            obj_name = obj.title
        elif lesson_id:
            obj = get_object_or_404(Lesson, id=lesson_id)
            amount = Decimal('50.00')
            obj_name = obj.title

        # 1. Создаём продукт в Stripe (имитация)
        product_id = create_stripe_product(name=obj_name, description=f"Платёж за {obj_name}")

        # 2. Создаём цену в Stripe (имитация)
        price_id = create_stripe_price(amount=amount, product_id=product_id)

        # 3. Создаём сессию оплаты (имитация)
        success_url = request.build_absolute_uri('/api/payments/success/')   # можно сделать страницу
        cancel_url = request.build_absolute_uri('/api/payments/cancel/')
        session_id, payment_url = create_checkout_session(price_id, success_url, cancel_url)

        # 4. Сохраняем платёж в нашей системе
        payment = Payment.objects.create(
            user=request.user,
            course=obj if course_id else None,
            lesson=obj if lesson_id else None,
            amount=amount,
            payment_method='stripe',
            status='pending',
            stripe_product_id=product_id,
            stripe_price_id=price_id,
            stripe_session_id=session_id,
            payment_url=payment_url,
        )

        return Response({
            'payment_id': payment.id,
            'payment_url': payment_url,
            'status': payment.status,
        }, status=status.HTTP_201_CREATED)

class PaymentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id, user=request.user)

        # Имитация получения статуса из Stripe
        # В реальности: session = stripe.checkout.Session.retrieve(payment.stripe_session_id)
        # status = session.payment_status
        status = retrieve_checkout_session(payment.stripe_session_id)

        # Обновляем статус в нашей модели
        if status == 'paid':
            payment.status = 'paid'
        elif status == 'unpaid':
            payment.status = 'pending'
        else:
            payment.status = 'failed'
        payment.save()

        return Response({
            'payment_id': payment.id,
            'stripe_status': status,
            'our_status': payment.status,
        })

