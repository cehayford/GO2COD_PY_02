from django.urls import path
from . import views

urlpatterns = [
    path('', views.scrape, name='scrape'),
    path('results/<int:pk>/', views.results, name='scraping_results'),
]