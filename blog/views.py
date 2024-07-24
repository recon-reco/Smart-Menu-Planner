from typing import Any
from django.shortcuts import render, redirect
from .models import Post, Category
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class PostList(ListView):
    model = Post
    ordering='-pk'

    def get_context_data(self,**kwargs):
        context=super(PostList, self).get_context_data()
        context['categories']=Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
        


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
    
def category_page(request, slug):
    category = Category.objects.get(slug=slug)
    if slug=='no_category':
        category='미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list':post_list,
            'categories':Category.objects.all(),
            'no_category_post_count':Post.objects.filter(category=None).count(),
            'category':category,
        }
    )
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category']

    def test_ftn(self):
        #포스트 작성 페이지 접근 권한 확인
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        #Post 작성 권한 : 로그인 & 관리자 또는 스태프
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author =  current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')

"""
def index(request):
    posts = Post.objects.all().order_by('-pk')
    return render(
        request,
        'blog/index.html'.
        {'posts':posts}    
    )
def single_post_page(request,pk):
    post = Post.objects.get(pk=pk)
    return render(
        request,
        'blog/single_post_page.html',
        {'post':post}
    )
"""