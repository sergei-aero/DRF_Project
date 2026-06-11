from django.urls import path
from .views import PaymentListAPIView, UserDetailView, RegisterView, UserDetailView

urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),  # CRUD пользователя
    path('register/', RegisterView.as_view(), name='register'),
]