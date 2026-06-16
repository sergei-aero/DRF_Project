from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from materials.models import Course, Lesson

class Command(BaseCommand):
    help = 'Создаёт группу модераторов с правами на просмотр и изменение уроков/курсов (без удаления и создания)'

    def handle(self, *args, **kwargs):
        # Создаём группу, если её нет
        group, created = Group.objects.get_or_create(name='Moderator')
        if created:
            self.stdout.write('Группа "Moderator" создана')
        else:
            self.stdout.write('Группа "Moderator" уже существует')

        # Получаем типы контента для моделей Course и Lesson
        course_ct = ContentType.objects.get_for_model(Course)
        lesson_ct = ContentType.objects.get_for_model(Lesson)

        # Разрешения: просмотр (view) и изменение (change) – исключаем add и delete
        permissions = Permission.objects.filter(
            content_type__in=[course_ct, lesson_ct],
            codename__in=['view_course', 'change_course', 'view_lesson', 'change_lesson']
        )
        # Назначаем права группе
        group.permissions.set(permissions)
        group.save()

        self.stdout.write(self.style.SUCCESS(
            f'Группе "Moderator" назначены права: {", ".join([p.codename for p in permissions])}'
        ))