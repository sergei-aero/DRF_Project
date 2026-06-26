from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Course
from users.models import Subscription, User

@shared_task
def send_course_update_email(course_id):
    """
    Отправляет письмо всем подписчикам курса об обновлении.
    """
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return

    # Получаем всех подписчиков на этот курс
    subscriptions = Subscription.objects.filter(course=course).select_related('user')
    emails = [sub.user.email for sub in subscriptions if sub.user.email]

    if not emails:
        return

    subject = f'Курс "{course.title}" был обновлён!'
    message = f'Здравствуйте! Курс "{course.title}" был обновлён. Зайдите на платформу, чтобы узнать новое.'
    from_email = settings.DEFAULT_FROM_EMAIL or 'noreply@example.com'

    send_mail(
        subject,
        message,
        from_email,
        emails,
        fail_silently=False,
    )