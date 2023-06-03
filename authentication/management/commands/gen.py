import random
import datetime
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from faker import Faker
from authentication.models import Gender
from transliterate import translit
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

User = get_user_model()
fake = Faker('ru_RU')


class Command(BaseCommand):
    help = 'Generate unique records in the database'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of records to generate')
        parser.add_argument('filename', type=str, help='Filename for the exported data')

    def handle(self, *args, **options):
        count = options['count']
        filename = options['filename']

        users = []

        with ThreadPoolExecutor() as executor:
            for _ in range(count):
                future = executor.submit(self.generate_user)
                users.append(future.result()[0])

        df = pd.DataFrame(users, columns=['Username', 'Password', 'Email', 'Last Name', 'First Name', 'Middle Name', 'Phone Number', 'Gender', 'Date Joined'])
        df['Password'] = [user[1] for user in users]  # Используем пароль в открытом виде для записи в таблицу Excel
        df.to_excel(filename, index=False)

        self.stdout.write(f'Successfully generated {count} users and exported to {filename}')

    def generate_user(self):
        gender = random.choice([Gender.MALE, Gender.FEMALE])
        last_name = self.generate_last_name(gender)
        first_name = self.generate_first_name(gender)
        middle_name = self.generate_middle_name(gender)
        phone_number = self.generate_phone_number()
        username = self.generate_username(last_name)
        password = self.generate_password()
        email = self.generate_email(username)

        # Генерация случайной даты и времени
        start_date = datetime.datetime(2023, 1, 1)
        end_date = datetime.datetime(2023, 12, 31)
        random_date = start_date + datetime.timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )

        # Преобразование даты и времени в нужный формат
        date_joined = random_date.strftime("%Y-%m-%d %H:%M:%S.%f%z")

        user = (
            username,
            password,
            email,
            last_name,
            first_name,
            middle_name,
            phone_number,
            gender[0],
            date_joined  # Добавляем дату и время в кортеж
        )

        User.objects.create(
            username=username,
            password=make_password(password),  # Записываем зашифрованный пароль в базу данных
            email=email,
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            phone_number=phone_number,
            gender=gender[0],
            date_joined=random_date  # Записываем дату и время в базу данных
        )

        return user, password

    def generate_last_name(self, gender):
        if gender == Gender.MALE:
            # Generate a masculine last name
            return fake.last_name_male()

        else:
            # Generate a feminine last name
            return fake.last_name_female()

    def generate_first_name(self, gender):
        if gender == Gender.MALE:
            # Generate a masculine middle name
            return fake.first_name_male()

        else:
            # Generate a feminine middle name
            return fake.first_name_female()

    def generate_middle_name(self, gender):
        if gender == Gender.MALE:
            # Generate a masculine middle name
            return fake.middle_name_male()

        else:
            # Generate a feminine middle name
            return fake.middle_name_female()

    def generate_phone_number(self):
        while True:
            # Generate a unique phone number in Russian format
            phone_number = '+7('
            phone_number += ''.join(random.choice('34589'))
            phone_number += ''.join(random.choice('0123456789') for _ in range(2))
            phone_number += ')'
            phone_number += ''.join(random.choice('0123456789') for _ in range(3))
            phone_number += '-'
            phone_number += ''.join(random.choice('0123456789') for _ in range(2))
            phone_number += '-'
            phone_number += ''.join(random.choice('0123456789') for _ in range(2))

            # Check if the generated phone number is unique
            if not User.objects.filter(phone_number=phone_number).exists():
                return phone_number

    def generate_username(self, last_name):
        # Generate a unique username based on last name (transliterated)
        username = slugify(translit(last_name, 'ru', reversed=True))
        while User.objects.filter(username=username).exists():
            username += str(random.randint(0, 9))

        return username

    def generate_password(self):
        # Generate a random password
        return fake.password()

    def generate_email(self, username):
        # Generate a unique email based on username
        domain = random.choice(['gmail.com', 'yahoo.com', 'yandex.ru', 'mail.ru'])
        return f'{username}@{domain}'
