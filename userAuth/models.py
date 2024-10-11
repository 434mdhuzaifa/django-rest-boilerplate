from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
# Create your models here.
UserModel=get_user_model()

class ResetToken(models.Model):
    user=models.ForeignKey(UserModel,on_delete=models.CASCADE)
    token=models.CharField(max_length=50)
    isvalid=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now=True,editable=True,auto_created=True)
    def __str__(self) -> str:
        return f'{self.user.username}-----{self.token}'
    
    @property
    def is_expired(self):
        return timezone.now() >= (self.created_at + timezone.timedelta(minutes=5))
    
    @property
    def remaining_time(self):
        delta =(self.created_at + timezone.timedelta(minutes=5))-timezone.now()
        if delta.total_seconds()<0:
            return False
        else:
            t=divmod(delta.total_seconds(),60)
            return f'{t[0]} min {int(t[1])} sec'