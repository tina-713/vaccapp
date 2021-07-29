from django.urls import path
from .views import RegisterView,Verify,Login,CountyList, CountyDetails, CityList, CityDetails, VaccineList, CategoryList, OfficeList, OfficeDetails, PersonList, PersonDetails, AppointmentList, WaitingList, WaitingDetails, PassordTokenCheck, RequestPasswordResetEmail


urlpatterns = [
  path('auth/register/', RegisterView.as_view(), name="register"),
  path('auth/verify/<token>', Verify.as_view(), name="verify"),
  path('auth/login/', Login.as_view(), name="login"),
  path('auth/request-reset-password/', RequestPasswordResetEmail.as_view(), name="request-reset-password"),
  path('auth/password-reset/<uidb64>/<token>', PassordTokenCheck.as_view(), name="password-reset"),
  path('counties/', CountyList.as_view(), name="counties"),
  path('counties/<int:pk>/', CountyDetails.as_view()),
  path('cities/', CityList.as_view(), name="cities"),
  path('cities/<int:pk>/', CityDetails.as_view()),
  path('vaccine/', VaccineList.as_view(), name="vaccine"),
  path('categories/', CategoryList.as_view(), name="categories"),
  path('office/', OfficeList.as_view(), name="office"),
  path('office/<int:pk>/', OfficeDetails.as_view()),
  path('person/', PersonList.as_view(), name="person"),
  path('person/<int:pk>/', PersonDetails.as_view()),
  path('appointment/', AppointmentList.as_view(), name="appointment"),
  path('waiting-list/', WaitingList.as_view(), name="waiting-list"),
  path('waiting-list/<int:pk>/', WaitingDetails.as_view()),
  
]