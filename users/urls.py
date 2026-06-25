from django.urls import path
from .views import PaymentListAPIView, UserDetailView, RegisterView, UserDetailView, UserListView, SubscriptionView, PaymentCreateView, PaymentStatusView

urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),  # CRUD пользователя
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('payments/create/', PaymentCreateView.as_view(), name='payment-create'),
    path('payments/<int:payment_id>/status/', PaymentStatusView.as_view(), name='payment-status'),
]