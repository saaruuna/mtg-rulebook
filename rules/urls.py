from django.urls import path

from . import views

urlpatterns = [
    path('', views.homeView, name='index'),
    path('<int:sectionid>/', views.chapterView, name='chapter'),
    path('search/', views.searchView, name='search'),
]
