from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Quiz(models.Model):
    quiz = models.CharField(max_length=200)
    maxtime=models.IntegerField()
    numquestions=models.IntegerField(default=10)
class questions(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    question=models.CharField(max_length=200)
    answer=models.CharField(default='',max_length=200)
    def __str__(self):
        return f"Question: {self.question} (Quiz: {self.quiz.quiz})"
class options(models.Model):
    question = models.ForeignKey(questions , on_delete=models.CASCADE)
    option = models.CharField(max_length=200)
    def __str__(self):
        return f"Option: {self.option} (Question: {self.question.question})"
class userquizdata(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE )
    # choice=models.ForeignKey(options,on_delete=models.CASCADE , related_name="choices")
    choice = models.ForeignKey(options,on_delete=models.CASCADE)
