from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import os

class Category(models.Model):
    name = models.CharField(max_length=10, unique=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    """人が読めるURL生成"""
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Categories'
    def get_absolute_url(self):
           return f'/blog/category/{self.slug}/'


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = MarkdownxField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)
    author = models.ForeignKey(User, null=True ,on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, blank=True ,null=True, on_delete=models.SET_NULL)
    #hook_text = models.CharField()

    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.author}'
    
    def get_absolute_url(self):
        return f'/blog/{self.pk}'


    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    
    def get_file_ext(self):
        return self.get_file_name().split(".")[-1]
    
    def get_content_markdown(self):
        return markdown(self.content)
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'
    
    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

class MainIngredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    serving_size = models.IntegerField()
    post = models.ForeignKey(Post, related_name='main_ingredients', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.quantity} for {self.serving_size} servings)'

    @property
    def standard(self):
        # Calculate standard as quantity divided by serving_size
        try:
            quantity_value = float(self.quantity)  # Assuming quantity is a numeric value stored as string
            return quantity_value / self.serving_size
        except (ValueError, ZeroDivisionError):
            return 0
