from django.urls  import path
from .views       import ReviewView , ReviewDetailView

urlpatterns = [
    path("<str:product_id",ReviewView.as_view()),
]
