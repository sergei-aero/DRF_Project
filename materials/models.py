from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='courses/previews/', blank=True, null=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    preview = models.ImageField(upload_to='lessons/previews/', blank=True, null=True)
    video_link = models.URLField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lessons'
    )

    def __str__(self):
        return self.title