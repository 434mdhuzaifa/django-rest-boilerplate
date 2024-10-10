from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from common.utility import format_timedelta
# Create your models here.
UserModel=get_user_model()

class ResetToken(models.Model):
    user=models.ForeignKey(UserModel,on_delete=models.CASCADE)
    token=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now=True,editable=False)
    
    def __str__(self) -> str:
        return f'{self.user.username}-----{self.token}'
    
    @property
    def is_expired(self):
        return timezone.now() - self.created_at < timezone.timedelta(minutes=5)
    
    @property
    def remaining_time(self):
        if self.is_expired:
            return "Expired"
        else:
            delta = self.created_at + timezone.timedelta(minutes=5) - timezone.now()
            return format_timedelta(delta)