from django.urls import path
from .views      import (SignUpView,
                         SignInView,
                         KakaoView,
                         ProfileView,
                         ActivateView)

urlpatterns = [
    path('sign-up'                           , SignUpView.as_view()),
    path('sign-in'                           , SignInView.as_view()),
    path('kakao_login'                       , KakaoView.as_view()),
    path('profile'                           , ProfileView.as_view()),
    path('activate/<str:uidb64>/<str:token>' , ActivateView.as_view())
]
