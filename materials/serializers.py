from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_link', 'course', 'owner', 'owner_email']

class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lessons_count', 'lessons']

    def get_lessons_count(self, obj):
        return obj.lessons.count()