from django.urls import path
from .views import RegisterView,Verify, Login


urlpatterns = [
  path('register/', RegisterView.as_view(), name="register"),
  path('login/', Login.as_view(), name="login"),
  path('verify/<token>', Verify.as_view(), name="verify"),
]