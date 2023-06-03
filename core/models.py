from PIL.ImImagePlugin import number
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class TireSize(models.Model):
    size = models.IntegerField()

    def __str__(self):
        return f'{self.size}'

    class Meta:
        verbose_name = 'Диаметр шины'
        verbose_name_plural = 'Диаметр шин'


class PeriodOfStorage(models.Model):
    period = models.IntegerField()

    def __str__(self):
        return f'{self.period}'

    class Meta:
        verbose_name = 'Срок хранения'


class QuantityOfTires(models.Model):
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.quantity}'

    class Meta:
        verbose_name = 'Количество шин'


class OrderStatus(models.IntegerChoices):
    CREATE = 0, 'Создан'
    STORAGE = 1, 'На хранении'
    CANCELED = 2, 'Отменён'
    FINISH = 3, 'Завершен'


class AddressService(models.Model):
    address = models.CharField(verbose_name='Адрес сервиса', max_length=125, )

    def __str__(self):
        return f'{self.address}'

    class Meta:
        verbose_name = 'Адрес сервиса'
        verbose_name_plural = 'Адреса сервисов'


class OrderStorage(models.Model):
    user = models.ForeignKey(to=User, verbose_name='User', on_delete=models.CASCADE)
    quantity = models.ForeignKey(verbose_name='Количество', to=QuantityOfTires, on_delete=models.CASCADE)
    size = models.ForeignKey(verbose_name='Размер', to=TireSize, on_delete=models.CASCADE)
    period = models.ForeignKey(verbose_name='Период', to=PeriodOfStorage, on_delete=models.CASCADE)
    address = models.ForeignKey(verbose_name='Адрес', to=AddressService, on_delete=models.CASCADE)
    status = models.IntegerField(verbose_name='Статус', choices=OrderStatus.choices, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_payed = models.BooleanField(verbose_name='Оплачен', default=False)
    payed_at = models.DateTimeField(verbose_name='Дата оплаты', blank=True, null=True)
    date_start = models.DateTimeField(verbose_name='Дата начала хранения', blank=True, null=True)
    date_finish = models.DateTimeField(verbose_name='Дата окончания хранения', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлён', auto_now=True)
    cheque = models.FileField('Чек', upload_to='checks/', null=True, blank=True)
    notification_finish  = models.BooleanField(verbose_name='Письмо', default=False, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return f'Клиент - {self.user}, перирод - {self.period} '

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__original_is_payed = self.is_payed

    def save(self, force_insert=False, force_update=False, *args, **kwargs) -> None:
        if self.is_payed != self.__original_is_payed:
            self.payed_at = timezone.now()
            self.__original_is_payed = self.is_payed
        return super().save(force_insert, force_update, *args, **kwargs)

    def get_nds(self):
        from decimal import Decimal, ROUND_HALF_DOWN
        try:
            res = self.price * Decimal(0.2)
            return res.quantize(Decimal("1.00"), ROUND_HALF_DOWN)
        except:
            return None

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class CallApplication(models.Model):

    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=16, verbose_name='Номер телефона')
    topic = models.CharField(max_length=50, verbose_name='Тема обращения')
    msg = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
