""" модели категория, объявление, отклик """
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce import models as tinymce_models


class Advert(models.Model):
    """ модель Объявление """

    CATEGORY_CHOICES = (
        ("tanks", "Танки"),
        ("heals", "Хилы"),
        ("dnd", "ДНД"),
        ("merchants", "Торговцы"),
        ("guildmasters", "Гилдамастеры"),
        ("giver_quest", "Квестгиверы"),
        ("blackmiths", "Кузнецы"),
        ("leatherworkers", "Кожевники"),
        ("potions_masters", "Зельевары"),
        ("spellmasters", "Мастера заклинаний"),
    )

    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50,
                                null=False, blank=False, verbose_name='Категория')
    title = models.CharField(max_length=255, null=False, blank=False,
                             verbose_name='Заголовок объявления')
    text = tinymce_models.HTMLField(max_length=4000, null=False, blank=False,
                                    verbose_name='Текст объявления')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Время создания объявления')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False,
                               blank=False, verbose_name='Автор объявления')
    
    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-created_at']
       
    def __str__(self):
        return f'{self.get_category_display()}.{str(self.title)[:50]}'
    
    def get_absolute_url(self):
        return reverse("one_advert", kwargs={"pk": self.pk})
    
    @staticmethod
    def get_category_title(need_key):
        for key, title in Advert.CATEGORY_CHOICES:
            if key == need_key:
                return title
    
   
class Comment(models.Model):
    """ модель Комментария """
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE, null=False,
                                blank=False, verbose_name='Объявление')
    accepted = models.BooleanField(default=False, verbose_name='Принят')
    text = models.TextField(max_length=1000, null=False, blank=False,
                            verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Время создания')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False,
                               blank=False, verbose_name='Автор')
    
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-created_at']
       
    def __str__(self):
        return str(self.text)[:50]

