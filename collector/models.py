from django.db import models
from main.models import CollectionPoint, User

class Review(models.Model):
    review = models.CharField(max_length=500,default="")
    creater = models.ForeignKey(User, on_delete=models.PROTECT,default="")
    receiver = models.ForeignKey(CollectionPoint, on_delete=models.PROTECT,default="")
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class ReviewResponse(models.Model):
    creater = models.ForeignKey(User, on_delete=models.PROTECT,default="")
    responseto = models.ForeignKey(Review, on_delete=models.PROTECT,default="")
    meaasage = models.CharField(max_length=2000, default="")
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Question(models.Model):
    question = models.CharField(max_length=2000,default="")
    creater = models.ForeignKey(User, on_delete=models.PROTECT,default="")
    receiver = models.ForeignKey(CollectionPoint, on_delete=models.PROTECT,default="")
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class QuestionResponse(models.Model):
    creater = models.ForeignKey(User, on_delete=models.PROTECT,default="")
    responseto = models.ForeignKey(Question, on_delete=models.PROTECT,default="")
    meaasage = models.CharField(max_length=200,default="")
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
