from django.urls import path
from .views import RegisterView,Verify,Login,CitiesList, UpdateCity


urlpatterns = [
  path('auth/register/', RegisterView.as_view(), name="register"),
  path('auth/login/', Login.as_view(), name="login"),
  path('auth/verify/<token>', Verify.as_view(), name="verify"),
  path('cities/', CitiesList.as_view(), name="cities"),
  path('cities/<int:pk>/', UpdateCity.as_view()),
]