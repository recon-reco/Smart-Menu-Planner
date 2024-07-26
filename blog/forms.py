from django import forms
from .models import Post, MainIngredient

class PostForm(forms.ModelForm):
    class Meta: 
        model = Post
        fields = ['title', 'content','category']

class MainIngredientForm(forms.ModelForm):
    class Meta:
        model = MainIngredient
        fields =['name','quantity','serving_size']        