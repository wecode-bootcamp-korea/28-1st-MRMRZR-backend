from django.urls import path

from users.views import UserSignUpView, UserLogInView

urlpatterns = [
    path('/signup', UserSignUpView.as_view()),
    path('/login', UserLogInView.as_view()),
]