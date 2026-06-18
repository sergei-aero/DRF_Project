import re
from django.core.exceptions import ValidationError

def validate_youtube_url(value):
    """
    Проверяет, что ссылка ведёт на youtube.com (или youtu.be).
    """
    # Паттерн для youtube: основной домен или сокращённый youtu.be
    youtube_pattern = re.compile(
        r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'
    )
    if not youtube_pattern.match(value):
        raise ValidationError(
            'Разрешены только ссылки на YouTube (youtube.com или youtu.be).'
        )