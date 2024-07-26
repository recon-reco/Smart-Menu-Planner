from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Post, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from django.urls import reverse_lazy

from django.forms import inlineformset_factory
from .models import Post, MainIngredient, Category
from .forms import PostForm, MainIngredientForm

# Create your views here.

MainIngredientFormSet =  inlineformset_factory(Post, MainIngredient, form=MainIngredientForm, extra=1)

class PostList(ListView):
    model = Post
    ordering='-pk'
    #form_class = PostForm
    #template_name = 'blog/post_list.html'
    #paginate_by = 5

    
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
    form_class = PostForm
    template_name = 'blog/post_form.html'
    ##success_url = reverse_lazy('post_list')
    ##fields = ['title', 'content', 'category']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = MainIngredientFormSet(self.request.POST)
        else:
            context['formset'] = MainIngredientFormSet()
        return context
    
    def test_ftn(self):
        #포스트 작성 페이지 접근 권한 확인
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            context = self.get_context_data()
            formset = context['formset']
            if formset.is_valid():
                response = super().form_valid(form)
                formset.instance = self.object
                formset.save()
                return response
            else:
                return self.render_to_response(self.get_context_data(form=form))
        else:
            return redirect('/blog/')
    """##def form_valid(self, form):
        #Post 작성 권한 : 로그인 & 관리자 또는 스태프
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author =  current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')"""
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = MainIngredientFormSet(self.request.POST, instance=self.get_object())
        else:
            context['formset'] = MainIngredientFormSet(instance=self.get_object())
        return context

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and current_user == form.instance.author:
            context = self.get_context_data()
            formset = context['formset']
            if formset.is_valid():
                response = super().form_valid(form)
                formset.instance = self.object
                formset.save()
                return response
            else:
                return self.render_to_response(self.get_context_data(form=form))
        else:
            return redirect('/blog/')
"""##class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields=['title','content','category']
    
    template_name = 'blog/post_update_form.html'
    #포스트작성자만 포스트를 수정할 수 있다.
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs:Any):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied"""

class PostSearch(PostList):
    paginate_by=None #한 페이지의 포스트 수 

    def get_queryset(self):
        q= self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q)
        ).distinct()
        return post_list
    
    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        return context

class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/confirm_delete.html'
    success_url = '/blog/'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)
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