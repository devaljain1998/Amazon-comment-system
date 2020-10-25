from django.urls import path

from .views import get_amazon_review, get_amazon_link, get_link_number, get_algorithm, homepage

urlpatterns = [
    path('amazon_analyser/number', get_link_number, name='get-link-number'),
    path('amazon_analyser/link', get_amazon_link, name='get-amazon-link'),
    path('amazon_analyser/algorithm', get_algorithm, name='get-algorithm'),
    path('amazon_analyser/result', get_amazon_review, name='get-amazon-review'),
    path('', homepage, name='homepage'),
]