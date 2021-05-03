from django.urls import path
from .views import RegisterView,Verify, Login


urlpatterns = [
  path('auth/register/', RegisterView.as_view(), name="register"),
  path('auth/login/', Login.as_view(), name="login"),
  path('auth/verify/<token>', Verify.as_view(), name="verify"),
]