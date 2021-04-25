from django.db import models

# Create your models here.
class Question(models.Model):
    def __str__(self):
        return self.question_text

    question_text = models.CharField(max_length=200)

class UserInput(models.Model):
    def __str__(self):
        return self.choice_text
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.IntegerField(default=200)