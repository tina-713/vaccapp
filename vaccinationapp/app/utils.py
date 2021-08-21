from django.db.models.aggregates import Min
from django.db.models.expressions import F
from django.http.response import FileResponse
from django.template.response import SimpleTemplateResponse
from .serializers import PersonSerializer, UserFullSerializer, UserSerializer, WaitingSerializer
from .models import Person, User, Waiting
from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape,A4,inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

import datetime
import io

class Util:
  @staticmethod
  def send_email(data):
    email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
    email.send()

def SendEmailToFirstPersonInQueue(officeId,WaitingList):
  
  lowestSpot = Waiting.objects.all().filter(office = officeId).aggregate(Min("spot"))
  waitEntry = Waiting.objects.get(office = officeId,spot=lowestSpot['spot__min'])
  waiterSerializier = WaitingSerializer(waitEntry)
 
  personToGetMail = Person.objects.get(id = waiterSerializier.data['person'])
  persSerializier = PersonSerializer(personToGetMail)
  userToGetMail = User.objects.get(id=persSerializier.data['user'])
  userSerializer = UserFullSerializer(userToGetMail)
  
  if WaitingList > 1 :
    WaitingTobeUpdated = Waiting.objects.filter(office=officeId,spot__gte=lowestSpot['spot__min']).update(spot=F('spot')-1)
  
  data = {}
  data['email_subject'] = 'Placeholder text, ready for appointment'
  data["email_body"] = 'bla bla http://localhost:8080/office/'+str(officeId)+'/'+ str(persSerializier.data['id'])
  data['to_email'] = userSerializer.data['email']
  try :
    Util.send_email(data)
  except Exception as e :
    return e

  waitEntry.delete()
  if WaitingList > 1 :
    Waiting.objects.filter(office=officeId,spot__gte=lowestSpot['spot__min']).update(spot=F('spot')-1)

def ConstructAppointmentPdf(data):
  d = datetime.datetime.today().strftime('%Y-%m-%d')
  buffer = io.BytesIO()

  p = canvas.Canvas(buffer,pagesize=A4)

  p.setFont("Helvetica",15,leading=None)
  p.drawString(260,800,"Programare")
  p.line(0,780,1000,780)
  p.line(0,778,1000,778)
  x1 = 20
  y1=750
  print(data)
  p.drawString(x1,y1-30,"Beneficiar")
  p.drawString(x1+100,y1-30,"Beneficiar")
  p.setTitle(f'Progamare')
  p.showPage()
  p.save()
  buffer.seek(0)
  return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold',16)
    canvas.drawString(330,500,"Programare Vaccin")
    canvas.setFont('Times-Roman',9)
    canvas.drawString(0,100,"")
    canvas.restoreState()


def ConstructTabletPdf(data):
  buffer = io.BytesIO()
  doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
  doc.pagesize = landscape(A4)
  elements = [Spacer(1,2*inch)]
  dt = [
  ["Beneficiar", "Tip Programare", "Status", "Locatie Centru de Vaccinare","Data Programarii","Ora Programarii"],
  [data['person']['name']+" "+data['person']['last_name'], data['kind'], data['status'], data['office']['name']+", "+data['office']['city']['name']+", "+data['office']['county']['name'],data['date'],str(data['time'])],
  ]


  #TODO: Get this line right instead of just copying it from the docs
  style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                        ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                        ('VALIGN',(0,0),(0,-1),'TOP'),
                        ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                        ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                        ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ])

  #Configure style and word wrap
  s = getSampleStyleSheet()
  s = s["BodyText"]
  s.wordWrap = 'CJK'
  data2 = [[Paragraph(cell, s) for cell in row] for row in dt]
  t=Table(data2)
  t.setStyle(style)

  #Send the data and build the file

  elements.append(t)
  
  doc.build(elements,onFirstPage=myFirstPage)
  buffer.seek(0)

  return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

