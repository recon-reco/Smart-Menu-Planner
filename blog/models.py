from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    #author
    #hook_text

    def __str__(self): #Post Listでpost.title
        return f'[{self.pk}]{self.title}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'