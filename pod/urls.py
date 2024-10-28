from django.urls import path
from .views import scrape

urlpatterns = [
    path('', scrape, name='scrape'),  # Update this to the root of the app
]


# from django.urls import path
# from .views import scrape_view

# urlpatterns = [
#     path('scrape/', scrape_view, name='scrape_view'),
# ]