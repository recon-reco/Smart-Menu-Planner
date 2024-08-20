from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .forms import CommentForm


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
        return redirect(post.get_absolute_url)
    else:
        raise PermissionDenied