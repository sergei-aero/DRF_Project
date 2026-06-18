from django.core.management.base import BaseCommand
from users.models import User, Payment
from materials.models import Course, Lesson
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generate random payments for users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        courses = Course.objects.all()
        lessons = Lesson.objects.all()

        if not users:
            self.stdout.write(self.style.ERROR('No users found. Create a superuser first.'))
            return

        for _ in range(10):  # создадим 10 платежей
            user = random.choice(users)
            amount = round(random.uniform(10, 200), 2)
            method = random.choice(['cash', 'transfer'])
            # случайный выбор: платёж за курс или за урок
            if random.choice([True, False]) and courses.exists():
                course = random.choice(courses)
                lesson = None
            elif lessons.exists():
                lesson = random.choice(lessons)
                course = None
            else:
                continue

            payment = Payment.objects.create(
                user=user,
                amount=amount,
                payment_method=method,
                course=course,
                lesson=lesson,
                payment_date=datetime.now() - timedelta(days=random.randint(0, 30))
            )
            self.stdout.write(self.style.SUCCESS(f'Created payment {payment.id} for {user.email}'))

        self.stdout.write(self.style.SUCCESS('Done.'))

