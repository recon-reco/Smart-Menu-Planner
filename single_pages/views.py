from django.shortcuts import render
from blog.models import Post

from rest_framework.decorators import api_view
from rest_framework.response import Response

def landing(request):
    recent_posts =Post.objects.order_by('-pk')[:5]

    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_posts' : recent_posts,
        }

    )

def about_me(request):
    return render(
        request, 
        'single_pages/about_me.html',
    )

@api_view(['GET'])
def get_menu(request):
    menu = {
        'carbs': ['Rice', 'Bread'],
        'main': ['Chicken', 'Beef'],
        'soup': ['Miso Soup', 'Tomato Soup'],
    }
    return Response(menu)
