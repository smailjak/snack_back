from django.urls  import path
from .views       import (SearchView,
                          ProductDetailView,
                          ProductView,
                          CategoryView)

urlpatterns = [
    path("/<str:category_name>" , ProductView.as_view()),
    path("/<int:product_id>"    , ProductDetailView.as_view()),
    path("category"             , CategoryView.as_view()),
    path("search"               , SearchView.as_view()),
]
