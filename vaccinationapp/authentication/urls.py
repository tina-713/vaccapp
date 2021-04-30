from django.urls import path
from .views import RegisterView,Verify


urlpatterns = [
  path('register/', RegisterView.as_view(), name="register"),
  path('verify/<token>', Verify.as_view(), name="verify"),
]