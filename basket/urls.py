from django.urls import path
from .views      import (BasketView ,
                         WishProductView)

urlpatterns = [
    path('/basket' , BasketView.as_view()),
    path('/wish'   , WishProductView.as_view()),
]
