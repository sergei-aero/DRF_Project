from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.contrib.auth.models import Group
from rest_framework import status
from materials.models import Course, Lesson
from users.models import Subscription

User = get_user_model()

class LessonAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        # Создаём модератора и добавляем его в группу
        self.moderator = User.objects.create_user(
            email='moderator@example.com',
            password='moderpass123'
        )
        moderator_group, _ = Group.objects.get_or_create(name='Moderator')
        self.moderator.groups.add(moderator_group)

        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )
        self.lesson_data = {
            'title': 'Test Lesson',
            'description': 'Lesson Desc',
            'video_link': 'https://www.youtube.com/watch?v=abc',
            'course': self.course.id
        }

    def test_create_lesson_authenticated_owner(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/lessons/', self.lesson_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        lesson = Lesson.objects.first()
        self.assertEqual(lesson.owner, self.user)

    def test_create_lesson_moderator_forbidden(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post('/api/lessons/', self.lesson_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_lesson_owner(self):
        lesson = Lesson.objects.create(
            title='Old Title',
            description='Old Desc',
            video_link='https://www.youtube.com/watch?v=old',
            course=self.course,
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f'/api/lessons/{lesson.id}/',
            {'title': 'New Title'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson.refresh_from_db()
        self.assertEqual(lesson.title, 'New Title')

    def test_update_lesson_moderator_allowed(self):
        lesson = Lesson.objects.create(
            title='Old Title',
            description='Old Desc',
            video_link='https://www.youtube.com/watch?v=old',
            course=self.course,
            owner=self.user
        )
        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(
            f'/api/lessons/{lesson.id}/',
            {'title': 'Changed by Moderator'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson.refresh_from_db()
        self.assertEqual(lesson.title, 'Changed by Moderator')

    def test_delete_lesson_owner(self):
        lesson = Lesson.objects.create(
            title='To Delete',
            description='...',
            video_link='https://www.youtube.com/watch?v=del',
            course=self.course,
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/lessons/{lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_delete_lesson_moderator_forbidden(self):
        lesson = Lesson.objects.create(
            title='To Delete',
            description='...',
            video_link='https://www.youtube.com/watch?v=del',
            course=self.course,
            owner=self.user
        )
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(f'/api/lessons/{lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_youtube_validator(self):
        self.client.force_authenticate(user=self.user)
        invalid_data = self.lesson_data.copy()
        invalid_data['video_link'] = 'https://example.com/video'
        response = self.client.post('/api/lessons/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Разрешены только ссылки на YouTube', str(response.data))

    def test_subscription(self):
        self.client.force_authenticate(user=self.user)
        # Подписаться
        response = self.client.post('/api/subscription/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # Отписаться
        response = self.client.post('/api/subscription/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_is_subscribed_field(self):
        self.client.force_authenticate(user=self.user)
        # Подписываемся
        self.client.post('/api/subscription/', {'course_id': self.course.id})
        response = self.client.get(f'/api/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])
