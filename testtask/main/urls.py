from django.urls import path
from . import views
urlpatterns = [
    path('', views.main),
    path('api/titles', views.titles),
    path('api/titles_details', views.titles_details),
    path('api/chapter', views.chapter),
    path('api/like_chapter', views.like_chapter)
]