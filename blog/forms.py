from .models import Comment, Post, MainIngredient, Category
from django import forms
from django.forms import inlineformset_factory


class PostForm(forms.ModelForm):
    new_category = forms.CharField(max_length=100, required=False, help_text="Create a new category or leave blank.")

    class Meta:
        model = Post
        fields = ['title', 'content', 'head_image', 'file_upload', 'category']

    def save(self, commit=True):
        instance = super().save(commit=False)
        new_category_name = self.cleaned_data.get('new_category')
        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
            instance.category = category
        if commit:
            instance.save()
        return instance
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=('content',)
        #exclude=('post','author','created_at', 'modified_at',)

# MainIngredient에 대한 Inline Formset 생성
MainIngredientFormSet = inlineformset_factory(
    Post, MainIngredient,
    fields=('name', 'quantity' , 'serving_size'
    ),
    extra=1,  # 기본으로 제공할 빈 form의 개수
    can_delete=True  # 사용자가 form을 삭제할 수 있게 함
)