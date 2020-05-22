from django.urls import path, include
from .views      import BasketView

urlpatterns = [
    path('basket', BasketView.as_view()),
]
