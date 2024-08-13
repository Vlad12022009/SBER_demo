from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TransferModel(models.Model):
    class Meta:
        verbose_name = 'транзакцию'
        verbose_name_plural = 'Транзакции'
        ordering = ['-date']
        
        
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='user_sender', verbose_name='Отправитель')
    other_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='user_recipient', verbose_name='Получатель')
    commentary = models.TextField(max_length=100, blank=True, null=True, verbose_name='Комментарий')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    translation_money = models.IntegerField(verbose_name='Сумма')
    read_status_sender = models.BooleanField(default=False, blank=True, null=True, verbose_name='Отправитель прочитал')
    read_status_recipient = models.BooleanField(default=False, blank=True, null=True, verbose_name='Получатель прочитал')

    def __str__(self):
        money = f"{self.translation_money:,}$".replace(',', '.')
        return f'\n\nОт: {self.user}  |  Кому: {self.other_user}  |  Сумма: {money}  |  Комментарий: {self.commentary}'
    
        


class UserProfile(models.Model):

    profile = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, default=None)
    money = models.IntegerField(default=10000)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.jpg')
    transition = models.ManyToManyField(TransferModel)

    def get_new_transitions(self):
        result = 0
        for i in self.transition.all():
            if self.profile == i.user:
                if not i.read_status_sender:
                    result += 1
            elif self.profile == i.other_user:
                if not i.read_status_recipient:
                    result += 1
        if result > 99:
            return '99+'
        return result

    def __str__(self):
        return self.profile.username

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'Профили'
