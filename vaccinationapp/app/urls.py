from django.urls import path
from .views import RegisterView,Verify,Login,CountyList, CountyDetails, CityList, CityDetails, VaccineList


urlpatterns = [
  path('auth/register/', RegisterView.as_view(), name="register"),
  path('auth/login/', Login.as_view(), name="login"),
  path('auth/verify/<token>', Verify.as_view(), name="verify"),
  path('counties/', CountyList.as_view(), name="counties"),
  path('counties/<int:pk>/', CountyDetails.as_view()),
  path('cities/', CityList.as_view(), name="cities"),
  path('cities/<int:pk>/', CityDetails.as_view()),
  path('vaccine/', VaccineList.as_view(), name="vaccine"),
]