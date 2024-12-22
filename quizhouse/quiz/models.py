from django.db import models

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
    