from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.PostList.as_view()),
    path("<int:pk>", views.PostDetail.as_view()),
    path("category/<str:slug>/", views.category_page),
    path("create_post/", views.PostCreate.as_view()),
    path("updated_post/<int:pk>/", views.PostUpdate.as_view()),
    path("accounts/", include("allauth.urls")),
    path("search/<str:q>/", views.PostSearch.as_view()),
    #path("", views.index),
    #path("<int:pk>", views.single_post_page),
]