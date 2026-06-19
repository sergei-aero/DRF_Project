from rest_framework import serializers
from .models import Course, Lesson
from .validators import validate_youtube_url
from users.models import Subscription

class LessonSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    video_link = serializers.URLField(validators=[validate_youtube_url], required=False)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_link', 'course', 'owner', 'owner_email']

class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    owner_email = serializers.ReadOnlyField(source='owner.email')
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'preview', 'description', 'owner', 'owner_email',
            'lessons_count', 'lessons', 'is_subscribed'
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from users.models import Subscription
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    def get_lessons_count(self, obj):
        return obj.lessons.count()
