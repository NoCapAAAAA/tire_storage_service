from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Gender(models.TextChoices):
    MALE = 'M', 'Мужской'
    FEMALE = 'F', 'Женский'


class User(AbstractUser):
    middle_name = models.CharField('Отчество', max_length=150, blank=True, null=True)
    phone_number = models.CharField('Телефон', max_length=127, blank=True,)
    gender = models.CharField('Пол', max_length=1, choices=Gender.choices, blank=True, null=True)
    photo = models.ImageField('Фото', blank=True, upload_to='avatars/', default='avatars/user_default.jpg')

    @property
    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return "/static/images/user_default.jpg"

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'username': self.username})

    def get_short_name(self) -> str:
        return f'{self.last_name} {self.first_name}'

    def get_full_name(self) -> str:
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def get_first_order_date(self):
        return self.order_set.order_by('created_at').first().created_at