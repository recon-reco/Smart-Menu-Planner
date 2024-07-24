from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content= models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #author : 추후 작성 예정
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}'