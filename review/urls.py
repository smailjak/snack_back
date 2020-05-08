from django.urls  import path
from .views       import ReviewView , ReviewDetailView

urlpatterns = [
    path("<int:product_id>",                 ReviewView.as_view()),
    path("<int:product_id>/<int:review_id>", ReviewDetailView),
]
