from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TransferModel(models.Model):
    class Meta:
        ordering = ['-date']
        
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='user_sender')
    other_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='user_recipient')
    commentary = models.TextField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    translation_money = models.IntegerField()
    read_status_sender = models.BooleanField(default=False, blank=True, null=True)
    read_status_recipient = models.BooleanField(default=False, blank=True, null=True)
    
        


class UserProfile(models.Model):

    profile = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, default=None)
    money = models.IntegerField(default=10000)
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
        return result

    def __str__(self):
        return self.profile.username


