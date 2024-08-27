from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .forms import CommentForm

import random


class PostList(ListView):
    model = Post
    ordering='-pk'

    #PostListにcategory contextを配信
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()#to base.html
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()#to base.html
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form']=CommentForm
        return context
def category_page(request, slug):
    if slug =='no_category':
        category='未分類'
        post_list = Post.objects.filter(category=None).order_by('-pk')
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category).order_by('-pk')
    #Instance of Category
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list' : post_list, 
            'categories' : Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count(),
            'category' : category,
        }
    )
    
class PostCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Post
    fields = ['title', 'content','head_image','file_upload','category']

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser # T/F

    def form_valid(self, form):
        current_user =self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')

class PostUpdate(UpdateView):
    model=Post
    fields = ['title', 'content','head_image','file_upload','category']#tag

    template_name = 'blog/post_update_form.html' #default : model_form.html

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_authenticated and (request.user == self.get_object().author):
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionError

class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/confirm_delete.html'
    success_url = '/blog/'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)
    
def new_comment(request, pk):
    if request.user.is_authenticated:
        post=get_object_or_404(Post, pk=pk)

        if request.method=='POST':
            comment_form =CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post=post
                comment.author=request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else : 
        raise PermissionDenied

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model=Comment
    form_class=CommentForm
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_authenticated and request.user ==self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def delete_comment(request, pk):
    comment=get_object_or_404(Comment, pk=pk)
    post=comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

class PostSearch(PostList):
    paginate_by =None
    
    def get_queryset(self) :
        q=self.kwargs['q']
        post_list=Post.objects.filter(
            Q(title__contains =q)
        ).distinct()
        return post_list
    
    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q}({self.get_queryset().count()})'
        return context
    

def category_post_lists(request):
    # 모든 카테고리를 가져옵니다.
    categories = Category.objects.all()
    
    # 카테고리별로 포스트 리스트를 저장할 딕셔너리
    category_post_dict = {}

    for category in categories:
        # 각 카테고리별로 해당되는 포스트의 타이틀 리스트를 가져옵니다.
        posts = Post.objects.filter(category=category)
        post_titles = [post.title for post in posts]
        
        # 카테고리 이름을 키로, 포스트 타이틀 리스트를 값으로 딕셔너리에 저장합니다.
        category_post_dict[category.name] = post_titles

    # 각 카테고리별로 10개의 랜덤한 원소를 뽑아내는 리스트 생성
    r1 = random.sample(category_post_dict['炭水化物'], 10)  # 중복 불허
    r2 = random.sample(category_post_dict['スープ'], 10)  # 중복 불허
    r3 = random.sample(category_post_dict['メイン'], 10)  # 중복 불허
    r4 = [random.choice(category_post_dict['サーブ']) for _ in range(10)]  # 중복 허용

    # week 리스트 초기화
    week = [[] for _ in range(5)]

    # week 리스트에 r1, r2, r3, r4의 요소 추가
    for i in range(5):
        week[i] += [r1[i], r1[i + 5]]
        week[i] += [r2[i], r2[i + 5]]
        week[i] += [r3[i], r3[i + 5]]
        week[i] += [r4[i], r4[i + 5]]

    # week 리스트를 템플릿에 전달
    return render(request, 'week_menu.html', {'week': week})