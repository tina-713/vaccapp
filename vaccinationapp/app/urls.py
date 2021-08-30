from django.urls import path
from .views import AppointmentUserDetails,RegisterView,Verify,Login,CountyList, CountyDetails, CityList, CityDetails, VaccineList, CategoryList, OfficeList, OfficeDetails, PersonList,AppointmentDetails, PersonDetails, AppointmentList, WaitingList, WaitingDetails,UserDetails,PersonUserDetails,CountyCityDetails,OfficeAppointmentDateDetails,OfficeAppointmentHourDetails,OfficeUserList,WaitingPersonOfficeDetails,AppointmentPdfDetails,AppointmentOfficeDetails,AppointmentPdfOfficeToday

urlpatterns = [
  path('auth/register/', RegisterView.as_view(), name="register"),
  path('auth/verify/<token>', Verify.as_view(), name="verify"),
  path('auth/login/', Login.as_view(), name="login"),
  path('counties/', CountyList.as_view(), name="counties"),
  path('counties/<int:pk>/', CountyDetails.as_view()),
  path('cities/', CityList.as_view(), name="cities"),
  path('cities/<int:county>/', CityDetails.as_view()),
  path('vaccine/', VaccineList.as_view(), name="vaccine"),
  path('categories/', CategoryList.as_view(), name="categories"),
  path('office/', OfficeList.as_view(), name="office"),
  path('office/user/<int:person>', OfficeUserList.as_view(), name="office"),
  path('office/<int:pk>/', OfficeDetails.as_view()),
  path('office/<int:pk>/<date>/',OfficeAppointmentDateDetails.as_view()),
  path('office/<int:pk>/<date>/rapel/<rapel>',OfficeAppointmentDateDetails.as_view()),
  path('office/<int:pk>/<date>/time/',OfficeAppointmentHourDetails.as_view()),
  path('person/', PersonList.as_view(), name="person"),
  path('person/<int:pk>/', PersonDetails.as_view()),
  path('person/user/<int:user>/', PersonUserDetails.as_view()),
  path('appointment/', AppointmentList.as_view(), name="appointment"),
  path('appointment/<int:pk>/', AppointmentDetails.as_view()),
  path('appointment/pdf/<int:appointment>/', AppointmentPdfDetails.as_view()),
  path('appointment/office/<int:office>/<date>', AppointmentOfficeDetails.as_view()),
  path('appointment/office/<int:office>/', AppointmentOfficeDetails.as_view()),
  path('appointment/user/<int:user>/', AppointmentUserDetails.as_view()),
  path('appointments/pdf/<int:office>/<date>', AppointmentPdfOfficeToday.as_view()),
  path('waiting-list/', WaitingList.as_view(), name="waiting-list"),
  path('waiting-list/<int:pk>/', WaitingDetails.as_view()),
  path('waiting-list/person/<int:person>/office/<int:office>', WaitingPersonOfficeDetails.as_view()),
  path('user/<email>/', UserDetails.as_view()),
]