from django.db.models.aggregates import Min
from django.db.models.expressions import F
from .serializers import PersonSerializer, UserFullSerializer, UserSerializer, WaitingSerializer
from .models import Person, User, Waiting
from django.core.mail import EmailMessage


class Util:
  @staticmethod
  def send_email(data):
    email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
    email.send()

def SendEmailToFirstPersonInQueue(officeId):
  
  lowestSpot = Waiting.objects.all().filter(office = officeId).aggregate(Min("spot"))
  waitEntry = Waiting.objects.get(office = officeId,spot=lowestSpot['spot__min'])
  waiterSerializier = WaitingSerializer(waitEntry)

  #get the lucky loser 
 
  personToGetMail = Person.objects.get(id = waiterSerializier.data['person'])
  persSerializier = PersonSerializer(personToGetMail)
  userToGetMail = User.objects.get(id=persSerializier.data['user'])
  userSerializer = UserFullSerializer(userToGetMail)
  


  data = {}
  data['email_subject'] = 'Placeholder text, ready for appointment'
  data["email_body"] = 'bla bla http://localhost:8080/office/'+str(officeId)+'/'+ str(persSerializier.data['id'])
  data['to_email'] = userSerializer.data['email']
  Util.send_email(data)
  waitEntry.delete()


