from django.db import models
from django.contrib.auth.models import User
from main.models import CollectionPoint

class Review(models.Model):
    review = models.CharField(max_length=500)
    creater = models.ForeignKey(User, on_delete=models.PROTECT)
    receiver = models.ForeignKey(CollectionPoint, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

class ReviewResponse(models.Model):
    creater = models.ForeignKey(User, on_delete=models.PROTECT)
    responseto = models.ForeignKey(Review, on_delete=models.PROTECT)
    meaasage = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    question = models.CharField(max_length=2000)
    creater = models.ForeignKey(User, on_delete=models.PROTECT)
    receiver = models.ForeignKey(CollectionPoint, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

class QuestionResponse(models.Model):
    creater = models.ForeignKey(User, on_delete=models.PROTECT)
    responseto = models.ForeignKey(Question, on_delete=models.PROTECT)
    meaasage = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
