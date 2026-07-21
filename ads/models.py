from django.db import models
from django.contrib.auth.models import User


class Ad(models.Model):
    """Объявление — главная сущность сайта."""

    # Категории (пары: значение в базе / название для человека)
    CATEGORY_CHOICES = [
        ('electronics', 'Электроника'),
        ('clothes', 'Одежда'),
        ('home', 'Дом и сад'),
        ('auto', 'Авто'),
        ('services', 'Услуги'),
        ('other', 'Другое'),
    ]

    # Статус объявления (челлендж-функция)
    STATUS_CHOICES = [
        ('active', 'Активно'),
        ('sold', 'Продано'),
    ]

    title = models.CharField('Название', max_length=100)
    price = models.DecimalField('Цена (сом)', max_digits=10, decimal_places=0)
    description = models.TextField('Описание')
    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='active')
    views = models.PositiveIntegerField('Просмотры', default=0)  # счётчик просмотров

    class Meta:
        ordering = ['-created_at']  # новые объявления сверху
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title

    def first_image(self):
        """Первое фото объявления (для карточки в списке)."""
        return self.images.first()


class AdImage(models.Model):
    """Фото объявления. У одного объявления может быть несколько фото."""

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images', verbose_name='Объявление')
    image = models.ImageField('Фото', upload_to='ads/')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def __str__(self):
        return f'Фото для {self.ad.title}'
