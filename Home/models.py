from django.db import models
import random


def random_answer():
    return random.randint(1, 4)


class Question(models.Model):
    op1 = models.CharField(max_length=50)
    op2 = models.CharField(max_length=50)
    op3 = models.CharField(max_length=50)
    op4 = models.CharField(max_length=50)
    answer = models.IntegerField(default=random_answer)

    def __str__(self):
        return f'1-{self.op1}, 2-{self.op2}, 3-{self.op3}, 4-{self.op4}'


class QuestionCapital(models.Model):
    op1 = models.CharField(max_length=50)
    op2 = models.CharField(max_length=50)
    op3 = models.CharField(max_length=50)
    op4 = models.CharField(max_length=50)
    answer = models.IntegerField(default=random_answer)

    def __str__(self):
        return f'1-{self.op1}, 2-{self.op2}, 3-{self.op3}, 4-{self.op4}'
