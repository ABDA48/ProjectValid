
from http.client import HTTPResponse
import random
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from main import form
from twilio.rest import Client
import json
from django.core.files.storage import FileSystemStorage
import requests
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
import pickle as pickle
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from main.form import PatientForm,MedicineForm,DiseasesForm,DoctorForm,RegistrationForm,loginForm,PneumoniaForm,AppointmentsForm
from main.models import AppointmentsModel, DiseasesModel,DoctorModel,HistoryModel,MedicineModel,PatientsModel,Profile,Discussion
from main.search import DiseaseSearch
DISEASE_HOST='http://127.0.0.1:8001/'
CHATBOT_HOST='http://127.0.0.1:8002/'
account_sid = 'AC91ee2b42485471796a886124787de050'
auth_token = '4dfc801c9fa59e200f29b4b0a57a3caf'
def registration(request):
    if request.method=='POST':
        print(request.POST)
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.refresh_from_db()
            user.profile.fullname= form.cleaned_data.get('fullname')
            user.profile.phone= form.cleaned_data.get('phone')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('prediction')
        else:
            print('login Error')
    form=RegistrationForm()
    return render (request,'userPage/registration.html',{'form':form})
@csrf_exempt
def loginView(request):
    #User.objects.filter(is_superuser=True).delete()
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            retractProfile(request,username)
            return redirect('prediction')
    form=loginForm()
    return render(request,'userPage/login.html',{'form':form})

def retractProfile(request,username):
    USERNAME=username
    u=User.objects.filter(username=USERNAME).values()[0]
    p=Profile.objects.get(user=u['id'])
    PHONE=p.phone
    FULLNAME=p.fullname
    request.session['uid']=u['id']
    request.session['username']=USERNAME
    request.session['phone']=PHONE
    request.session['fullname']=FULLNAME
    request.session['PROCESS']=0
    request.session['DISEASE']=''
    request.session['MEDICINE']=''
    

def index(request):
    return render(request,'userPage/home.html',{'page_title':'Home'})

def profileview(request):
    return render(request,'userPage/profile.html',{})


def dashboard(request):
    disease=DiseasesModel.objects.all()
    medicine=MedicineModel.objects.all()
    patient=PatientsModel.objects.all()
    doctor=DoctorModel.objects.all()
    numdisease=len(disease)
    nummedicine=len(medicine)
    numpatient=len(patient)
    numdoctor=len(doctor)
    data={
        'page_title':'Dashboard',
        'numdisease':numdisease,
        'nummedicine':nummedicine,
        'numpatient':numpatient,
        'numdoctor':numdoctor
        }
    return render(request,'dashboard.html',data)

def patient(request):
    form=PatientForm()
    data={
    'form':form,
     'page_title':'Add Patient'
    }
    return render(request,'patientForm.html',data)


def medicine(request):
    form=MedicineForm()
    data={
    'form':form,
     'page_title':'Add Medicine '
    }
    return render(request,'medicineForm.html',data)

def disease(request):
    form=DiseasesForm()
    data={
    'form':form,
     'page_title':'Add disease '
    }
    return render(request,'diseasForm.html',data)

def doctors(request):
    form=DoctorForm()
    data={
    'form':form,
     'page_title':'Add Doctors '
    }
    
    return render(request,'doctorForm.html',data)
def medicineManage(request):
    medicine=MedicineModel.objects.all()
    print(medicine.values())
    data={
     'results':medicine,
     'page_title':'Manage Medicines '
    }
    if request.method=='POST':
        if request.POST['id']:
            print(request.POST)
            id =request.POST['id']
            print('-------------yu')
            med=MedicineModel.objects.get(pk=id)
            med.name=request.POST['name']
            med.definition=request.POST['definition']
            med.warnings=request.POST['warnings']
            med.prescription=request.POST['prescription']
            med.effects=request.POST['effects']
             
            med.save()
            print('update')
            med=MedicineModel.objects.all()
            data={
            'results':med,
            'page_title':'Manage Medicines '
            }
            return render(request,'medicineManage.html',data)
        else:
            print('no id')
            med=MedicineForm(request.POST)
            if med.is_valid():
                med.save()
                print('saved')
                med=MedicineModel.objects.all()
                print(med.values())
                data={
                'results':med,
                'page_title':'Manage Medicines '
                }
                return render(request,'medicineManage.html',data)
    return render(request,'medicineManage.html',data)
    
def diseaseManage(request):
    disease=DiseasesModel.objects.all()
    data={
     'results':disease,
     'page_title':'Manage Disease '
    }
    if request.method=='POST':
        if request.POST['id']:
            print(request.POST)
            id =request.POST['id']
            print('-------------yu')
            disease=DiseasesModel.objects.get(pk=id)
            disease.name=request.POST['name']
            disease.definition=request.POST['definition']
            disease.causes=request.POST['causes']
            disease.causes=request.POST['treatments']
            disease.save()
            print('update')
            disease=DiseasesModel.objects.all()
            data={
            'results':disease,
            'page_title':'Manage Disease '
            }
            return render(request,'diseaseManage.html',data)
        else:
            print('no id')
            disease=DiseasesForm(request.POST)
            print(request.POST)
            if disease.is_valid():
                disease.save()
                print('saved')
                disease=DiseasesModel.objects.all()
                print(disease.values())
                data={
                'results':disease,
                'page_title':'Manage Disease '
                }
                return render(request,'diseaseManage.html',data)
    return render(request,'diseaseManage.html',data)

def patientManage(request):
    patient=PatientsModel.objects.all()
    data={
     'results':patient,
     'page_title':'Manage Patient '
    }
    if request.method=='POST':
        if request.POST['id']:
            id =request.POST['id']
            print('-------------yu')
            patient=PatientsModel.objects.get(pk=id)
            patient.age=request.POST['age']
            patient.doctor=request.POST['doctor']
            patient.address=request.POST['address']
            patient.weight=request.POST['weight']
            if len(request.FILES)>0:
                            patient.image=request.FILES['image']
            patient.save()
            print('update')
            patient=PatientsModel.objects.all()
            print(patient.values())
            data={
            'results':patient,
            'page_title':'Manage Patient '
            }
            return render(request,'patientManage.html',data)
        else:
            print('no id')
            patient=PatientForm(request.POST,request.FILES)
            print(request.POST,request.FILES)
            if patient.is_valid():
                patient.save()
                print('saved')
                patient=PatientsModel.objects.all()
                print(patient.values())
                data={
                'results':patient,
                'page_title':'Manage Patient '
                }
                return render(request,'patientManage.html',data)
            else:
                print('not valid')
    return render(request,'patientManage.html',data)
 
    


def doctorsManage(request):
    doctor=DoctorModel.objects.all()
    print(doctor.values())
    data={
     'results':doctor,
     'page_title':'Manage Doctor '
    }
    if request.method=='POST':
        if request.POST['id']:
            print(request.POST)
            id =request.POST['id']
            print('-------------yu')
            doc=DoctorModel.objects.get(pk=id)
            doc.name=request.POST['name']
            doc.specialty=DiseasesModel.objects.get(pk=request.POST['specialty']) 
            if len(request.FILES)>0:
                            doc.image=request.FILES['image']   
            doc.save()      
            print('update')
            doc=DoctorModel.objects.all()
            data={
            'results':doc,
            'page_title':'Manage Doctor '
            }
            return render(request,'doctorManage.html',data)
        else:
            print('no id')
            doc=DoctorForm(request.POST,request.FILES)
            if doc.is_valid():
                doc.save()
                print('saved')
                doc=DoctorModel.objects.all()
                print(doc.values())
                data={
                'results':doc,
                'page_title':'Manage Doctors '
                }
                return render(request,'doctorManage.html',data)
    return render(request,'doctorManage.html',data)

def patientedit(request,id):
    form=PatientForm()
    print(id)
    data={
        'id':id,
        'form':form,
    }
    return render(request,'patientEdit.html',data)
  
   

def patientdelete(request,id):
    patient=PatientsModel.objects.get(pk=id)
    patient.delete()
    patient=PatientsModel.objects.all()
    print(patient.values())
    data={
     'results':patient,
     'page_title':'Manage Patient '
    }
    return render(request,'patientManage.html',data)
    
def diseaseedit(request,id):
    form=DiseasesForm()
    print(id)
    data={
        'id':id,
        'form':form,
    }
    return render(request,'diseaseEdit.html',data)

def diseasedelete(request,id):
    disease=DiseasesModel.objects.get(pk=id)
    disease.delete()
    disease=DiseasesModel.objects.all()
    print(disease.values())
    data={
     'results':disease,
     'page_title':'Manage Patient '
    }
    return render(request,'diseaseManage.html',data)

def doctoredit(request,id):
    form=DoctorForm()
    print(id)
    data={
        'id':id,
        'form':form,
    }
    return render(request,'doctorEdit.html',data)

def doctordelete(request,id):
    doctor=DoctorModel.objects.get(pk=id)
    doctor.delete()
    doctor=DoctorModel.objects.all()
    print(doctor.values())
    data={
     'results':doctor,
     'page_title':'Manage Doctor '
    }
    return render(request,'doctorManage.html',data)

def medicineedit(request,id):
    form=MedicineForm()
    print(id)
    data={
        'id':id,
        'form':form,
    }
    return render(request,'medicineEdit.html',data)

def medicinedelete(request,id):
    med=MedicineModel.objects.get(pk=id)
    med.delete()
    med=MedicineModel.objects.all()
    print(med.values())
    data={
     'results':med,
     'page_title':'Manage Medicine '
    }
    return render(request,'medicineManage.html',data)



def predictiondiabetes(request):
    if request.method=='POST':
        pregnancies=request.POST['pregnancies']
        glucose=request.POST['glucose']
        bloodPressure=request.POST['bloodPressure']
        skinThickness=request.POST['skinThickness']
        insulin=request.POST['insulin']
        bMI=request.POST['bmI']
        diabetesPedigreeFunction=request.POST['diabetesPedigreeFunction']
        age=request.POST['age']
        body={
        "pregnancies": int(pregnancies),
        "glucose": int(glucose),
        "bloodPressure": int(bloodPressure),
        "skinThickness": int(skinThickness),
        "insulin": int(insulin),
        "bmI": int(bMI),
        "diabetesPedigreeFunction": int(diabetesPedigreeFunction),
        "age": int(age)
        }
        print(body)
        app_json = json.dumps(body)
        url='http://127.0.0.1:8001/predict/diabetes'
        response=requests.post(url,app_json)
        print(response.json())
        data={
            'result':response.json(),
             'username':request.session['username'],
            'phone':request.session['phone'],
            'fullname':request.session['fullname'],
        }
        return render(request,'actions/diabetePrediction.html',data)
    data={
            'username':request.session['username'],
            'phone':request.session['phone'],
            'fullname':request.session['fullname'],
    }
    return render(request,'actions/diabetePrediction.html',data)
 
def predictionheart(request):
    if request.method=='POST':
        age=request.POST['age']
        sex=request.POST['sex']
        cp=request.POST['cp']
        trestbps=request.POST['trestbps']
        chol=request.POST['chol']
        fbs=request.POST['fbs']
        restecg=request.POST['restecg']
        thalach=request.POST['thalach']
        exang=request.POST['exang']
        oldpeak=request.POST['oldpeak']
        slope=request.POST['slope']
        ca=request.POST['ca']
        thal=request.POST['thal']
        body={
        "age": int(age),
        "sex": int(sex),
        "cp": int(cp),
        "trestbps": int(trestbps),
        "chol": int(chol),
        "fbs": int(fbs),
        "restecg": int(restecg),
        "thalach": int(thalach),
        "exang": int(exang),
        "oldpeak": int(oldpeak),
        "slope": int(slope),
        "ca": int(ca),
        "thal": int(thal)
        }
        print(body)
        app_json = json.dumps(body)
        url='http://127.0.0.1:8001/predict/heart'
        response=requests.post(url,app_json)
        print(response.json())
        data={
            'result':response.json(),
            'username':request.session['username'],
            'phone':request.session['phone'],
            'fullname':request.session['fullname'],
        }
        return render(request,'actions/heartdiseasePrediction.html',data)
    data={
           'username':request.session['username'],
            'phone':request.session['phone'],
            'fullname':request.session['fullname'],
         }
    return render(request,'actions/heartdiseasePrediction.html',data)
    
 
@csrf_exempt
def prediction(request):
    if request.method=='POST':
        symp=request.POST['symptoms']
        sym=symp.strip()
        symptoms=sym.replace(" ","_")
        body={
             "symptoms":symptoms
            }
        app_json = json.dumps(body)
        url='http://127.0.0.1:8001/predict/diseases'
        response=requests.post(url,app_json)
        print(response.json())
        
        data={
            'result':response.json(),
            'form': form,
            'username':request.session['username'],
            'phone':request.session['phone'],
            'fullname':request.session['fullname'],
            }
        return render(request,'actions/generaldisease.html',data)
    user = User.objects.get(username=request.session['username'])
    print(user)
    data={
           'username':request.session['username'],
            'phone':request.session['phone'],
            'fullname':request.session['fullname'],
    }
    return render(request,'actions/generaldisease.html',data)

@csrf_exempt
def sendSymptoms(request):
     if request.method=='POST':
        symp=request.POST['symptom']
        sym=symp.strip()
        symptoms=sym.replace(" ","_")
        symptoms=symptoms.split(",")
        symptoms=symptoms[:len(symptoms)-1]
        symptoms=",".join(symptoms)
        print(symptoms)
        body={
             "symptoms":symptoms
            }
        response=sendrequest(body=body,host=DISEASE_HOST,url='predict/diseases',method='POST')
        print(response) 
        data={
            'res':response,
        }
        
        return JsonResponse({'statut':200,'data':data})


def pneumonia(request):
    if request.method == 'POST':
        form = PneumoniaForm(request.POST, request.FILES)
        print(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(request.FILES['document'])
            urlfile="C:/Users/jaola/Documents/GitHub/Project CP3/HealthCare/"
            media='media/documents/'
            filename=request.FILES['document']
            urlpath=urlfile+media+str(filename)
            print(urlpath)
            body={
             "path":urlpath
            }
            app_json = json.dumps(body)
            url='http://127.0.0.1:8001/predict/pneumonia'
            response=requests.post(url,app_json)
            print(response.json())
            data={
                'result':response.json(),
                 'form': form,
                'username':request.session['username'],
                'phone':request.session['phone'],
                'fullname':request.session['fullname'],
            }
            return render(request, 'actions/pneumoniaPrediction.html',data)
    else:
        form = PneumoniaForm()
        data={
           'username':request.session['username'],
            'phone':request.session['phone'],
            'fullname':request.session['fullname'],
            'form': form,
        }
        
    return render(request, 'actions/pneumoniaPrediction.html',data )

def chatbot(request):
    p=Profile.objects.get(user=request.session['uid'])
    patient=PatientsModel.objects.get(profile=p.id) 
    doctor=patient.doctor
    data={
           'username':request.session['username'],
            'room':str(doctor.profile.user.id)+"/"+str(patient.id),
        }
    return render(request,"actions/chatbot.html",data)
#request id
def doctorchatpatient(request,id,patentid):
    patient=PatientsModel.objects.filter(doctor_id=id)
    doctor=DoctorModel.objects.get(id=id)
    doc={}
    doc['idprofile']=doctor.profile.id
    doc['idname']=doctor.profile.fullname
    
    patient=list(patient)
    datapatient=[]
    for p in patient:
        d={}
        profile=Profile.objects.get(id=p.profile_id)
        u=User.objects.filter(username=profile).values()[0]
        d['name']=u['username']
        d['pid']=p.id
        d['did']=id
        d['image']=PatientsModel.objects.get(id=p.id).image.url  
        datapatient.append(d)
   
    data={
     'patients':datapatient,
     'doctor':doc,
      'doctorid':id,
      'patentid':patentid,
       'room':str(doctor.profile.user.id)+"/"+str(patentid),
       'username':request.session['username'],
    }
    return render(request, 'doctor/doctorchatbot.html',data )
   
def doctorhome(request,id):
    doctor=DoctorModel.objects.get(id=id)
    doc={}
    doc['idprofile']=doctor.profile.id
    doc['idname']=doctor.profile.fullname
    doc['image']=doctor.image.url   
    doc['specialty']=doctor.specialty 
   
    from datetime import date
    today = date.today()
    print(today)
    patient=PatientsModel.objects.filter(doctor=id)
    todayappointment=[]
    appointment=[]
    for p in patient:
        app=AppointmentsModel.objects.filter(patient=p.id,date=today)
        if len(app)>0:
            appointment.append(app)
    print(appointment)
    for ap in appointment:
        appoint={}
        appoint['time']=ap[0].slot
        appoint['date']=ap[0].date
        appoint['age']=ap[0].age
        appoint['disease']=ap[0].disease
        appoint['patient']=ap[0].patient.id
        appoint['image']=ap[0].patient.image.url
        appoint['name']=ap[0].patient.profile.fullname
        todayappointment.append(appoint)
    print(todayappointment)
    data={
        'doctor':doc,
        'id':id,
        'todayappointment':todayappointment
    }
    return render(request,'doctor/doctorhome.html',data)

def doctorpatients(request,id):
    patient=PatientsModel.objects.filter(doctor=id)
    print('values')
    print(patient.values())
    doctor=DoctorModel.objects.get(id=id)
    doc={}
    doc['idprofile']=doctor.profile.id
    doc['idname']=doctor.profile.fullname
    doc['image']=doctor.image.url   
    doc['specialty']=doctor.specialty 
    patlist=[]
    for p in patient:
        pat={}
        pat['id']=p.id
        pat['name']=p.profile.fullname
        pat['image']=p.image.url
        pat['age']=p.age
        patlist.append(pat)
    print(patlist)
    data={
        'doctor':doc,
        'id':id,
        'patient':patlist
    }
    return render(request,'doctor/doctorpatients.html',data)

def patientchat(request):
    p=Profile.objects.get(user=request.session['uid'])
    patient=PatientsModel.objects.get(profile=p.id) 
    doctor=patient.doctor
    data={
           'username':request.session['username'],
            'room':str(doctor.profile.user.id)+"/"+str(patient.id),
        }
    return render(request,'actions/patientchat.html',data)

def doctorappointment(request):
    if request.method=='POST':
        form=AppointmentsForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print('form accepted')
            form.save()
            data={
            'form':form
            }
            return render(request,'doctor/doctorappointment.html',data)
        else:
            print('form invalid')
    form=AppointmentsForm()
    data={
   'form':form
    }
    return render(request,'doctor/doctorappointment.html',data)


@csrf_exempt
def chatappointment(request):
    if request.method=='POST':
        p=Profile.objects.get(user=request.session['uid'])
        patient=PatientsModel.objects.get(profile=p.id)
        print(request.POST)
        disease=request.POST['disease']
        age=request.POST['age']
        date=request.POST['date']
        slot=request.POST['slot']
        app=AppointmentsModel.objects.create(patient=patient,disease=disease,age=age,date=date,slot=slot)
        print(app)
        print('Appo saved')
        data={
            'res':'Appointment Submitted'
        }
        return JsonResponse({'statut':'200','data':data})
  
@csrf_exempt
def doctorchat(request):
    if request.method=='POST':
        p=Profile.objects.get(user=request.session['uid'])
        patient=PatientsModel.objects.get(profile=p.id) 
        doctor=patient.doctor
        data={'doctorname':doctor.profile.fullname,'id':doctor.profile.user.id,
        'patientid':patient.id,
        'patUsername':patient.profile.user.username,
        'docUsername':doctor.profile.user.username,
        }
        print(data)
        return JsonResponse({'statut':'200','data':data})



         
         


        
        
        

@csrf_exempt
def doctorappointmentdate(request):

    if request.method=="POST":
        date=request.POST['date']
        print(request.POST)
        slots=[
                '9:00','10:00','11:00','12:00','14:00','15:00'
            ]
        og=AppointmentsModel.objects.all()
        obj=AppointmentsModel.objects.filter(date=date)
        print(obj)
        for o in obj:
            slots.remove(o.slot)
            print(o.slot)
        data={
        "slots":slots
        }
        print(data)
        return JsonResponse({'statut':'200','data': data})
        
        

    
    

     
 
     
@csrf_exempt
def chatbotsend(request):
    if request.method=='POST':
        message=''
        print(request.POST)
        if len(request.POST)==14:
            message=request.POST['Body']
            if message.lower()=='login':
                request.session['fullname']=request.POST['ProfileName']
                request.session['PROCESS']=0
                request.session['DISEASE']=''
                request.session['MEDICINE']=''
                sendtowatsapp('you are succesfully logged in Healthcare chatbot',request.POST['From'])


        else:
            message=request.POST['message']
        PROCESS=request.session['PROCESS']
        DISEASE=request.session['DISEASE']
        MEDICINE=request.session['MEDICINE']
        
        body={
            "question": message,
            "PROCESS": PROCESS,
            "DISEASE":DISEASE,
            'MEDICINE':MEDICINE
            }
        response,process,disease,medicine=sendrequest(CHATBOT_HOST,'chatbot/first',body,'POST')
        print(response)
        request.session['MEDICINE']=medicine    
        request.session['PROCESS']=process
        request.session['DISEASE']=disease
        p=0
        if response=='ASK':
            p=1
            response=showDisease(disease)
        if response=='cause':
            p=2
            response=causemessage(disease,DiseaseSearch(disease).causes())
        if response=='treatment':
            p=2
            response=treatmentmessage(disease,DiseaseSearch(disease).treatments())
        if response=='medicine':
            p=2
            response=medicinemessage(disease,DiseaseSearch(disease).medicine())
            MEDICINE=DiseaseSearch(disease).medicinename()
        if response=='prevention':
            p=2
            response=preventionmessage(disease,DiseaseSearch(disease).preventions())
        if response=='followup':
            p=1
            response=followupmessage(2)
        if response=='prescription':
            p=2
            response=prescriptionmessage(DiseaseSearch(disease).medicineprecription())
        if response=='effects':
            p=2
            response=effectsmessage(DiseaseSearch(disease).medicineeffects())
        
       
        print(response,PROCESS,DISEASE)
        data={
            'res':response,
            'position':p
        }
        if len(request.POST)==14:
            sendtowatsapp(response,request.POST['From'])
            

        
        return JsonResponse({'statut':200,'data':data})







def sendrequest(host,url,body,method):
    if method=='POST':
         app_json = json.dumps(body)
         uri=host+url
         response=requests.post(uri,app_json)
         return response.json()
def sendtowatsapp(body,tonumber):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
                              from_='whatsapp:+14155238886',
                              body=body,
                              to=tonumber
                          )

def causemessage(disease,cause):
    p1='Oh, you have {} .{} .Would you like to know the treatment of {}'.format(disease,cause,disease)
    p2='I am sorry you have {}.{} .Don\'t you   like to know how to treat of {}'.format(disease,cause,disease)
    return random.choice([p1,p2])
def treatmentmessage(disease,treatment):
    p1="Here are the treatment for {} {} .Would you like to know what medicine to take ? ".format(disease,treatment)
    p2="for {} you should {}.Would you want to take medicine?".format(disease,treatment)
    return random.choice([p1,p2])
def medicinemessage(disease,medicine):
    p1='for {} medicine you should take {} would you like to have prescriptions for it '.format(disease,medicine)
    p2='I recommend you to take {} .It is very effective for {}. do you want to know ho to use it ?'.format(medicine,disease)
    return random.choice([p1,p2])

def prescriptionmessage(prescr):
    p1='{} .Would you like to know the sides effects for it?'.format(prescr)
    p2='{} .Would you like to know what happen if you overdose ?'.format(prescr)
    return random.choice([p1,p2])
def effectsmessage(effects):
    p1='{} .Always make sure you follow doctors prescription? Would you like to know how to prevent this disease ?'.format(effects)
    p2='{} .Please take it according to the appropriate dosage ? Would you like to know how to prevent this disease?'.format(effects)
    return random.choice([p1,p2])
def preventionmessage(disease,prevention):
    p1='To prevent {} .The preventions are {}.Would you like me to follow up ?'.format(disease,prevention)
    p2='for {} preventions. You should {}. Would you like me to follow up ?'.format(disease,prevention)
    return random.choice([p1,p2])
def followupmessage(no):
    p1='Take care of yourself.After {} days follow up would be necessary. In case you should take an oppointment '.format(no)
    p2='After {} days .If  no result then you should go to the doctor'.format(no)
    return random.choice([p1,p2])

def showDisease(d):
    p1='you might be suffering from {} . which service would you like to take'.format(d)
    p2='you have {} . which service would you like to take'.format(d)
    return random.choice([p1,p2])

def logoutview(request):
    logout(request)
    return render(request,'userPage/home.html',{'page_title':'Home'})
    