from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #head_image
    #author
    #hook_text

    def __str__(self): #Post Listでpost.title
        return f'[{self.pk}]{self.title}'

    def get_absolute_url(self, pk):
        return f'/blog/{self.pk}/'