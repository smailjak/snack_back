from django.urls  import path
from .views       import (SearchView,
                          ProductDetailView,
                          ProductView)

urlpatterns = [
    path("search"                               , SearchView.as_view()),
    path("<str:category_name>"                  , ProductView.as_view()),
    path("<str:category_name>/<int:product_id>" , ProductDetailView.as_view()),
]
