from .models import Comment, Post, MainIngredient
from django import forms
from django.forms import inlineformset_factory


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=('content',)
        #exclude=('post','author','created_at', 'modified_at',)

# MainIngredient에 대한 Inline Formset 생성
MainIngredientFormSet = inlineformset_factory(
    Post, MainIngredient,
    fields=('name', 'quantity'),
    extra=1,  # 기본으로 제공할 빈 form의 개수
    can_delete=True  # 사용자가 form을 삭제할 수 있게 함
)