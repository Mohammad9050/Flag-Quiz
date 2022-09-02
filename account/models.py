from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    best_record = models.PositiveIntegerField(default=0)
    best_record2 = models.PositiveIntegerField(default=0)  # game mode 2 record

    def computing_record(self, record, num):
        if num == 1: # game mode
            if record > self.best_record:
                self.best_record = record
                self.save()
        else:
            if record > self.best_record2:
                self.best_record2 = record
                self.save()

    def __str__(self):
        return f'{0} : {1}'.format(self.user.username, self.best_record)
