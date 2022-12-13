from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name='index'),
     path("dashboard/",views.dashboard,name='dashboard'),
    path("patient/",views.patient,name='patient'),
     path("medicine/",views.medicine,name='medicine'),
     path("disease/",views.disease,name='disease'),
     path("doctors/",views.doctors,name='doctors'),
      path("profile",views.profileview,name='profile'),
      #manage
    path("medicine/manage",views.medicineManage,name='medicinemanage'),
     path("disease/manage",views.diseaseManage,name='diseasemanage'),
      path("patient/manage",views.patientManage,name='patientmanage'),
        path("doctors/manage",views.doctorsManage,name='doctorsmanage'),
        path("patient/manage/edit/<int:id>",views.patientedit,name='patientedit'),
        path("patient/manage/delete/<int:id>",views.patientdelete,name='patientdelete'),
         path("disease/manage/edit/<int:id>",views.diseaseedit,name='diseaseedit'),
        path("disease/manage/delete/<int:id>",views.diseasedelete,name='diseasedelete'),
         path("doctors/manage/edit/<int:id>",views.doctoredit,name='doctoredit'),
        path("doctors/manage/delete/<int:id>",views.doctordelete,name='doctordelete'),
         path("medicine/manage/edit/<int:id>",views.medicineedit,name='medicineedit'),
         
        path("medicine/manage/delete/<int:id>",views.medicinedelete,name='medicinedelete'),
        #registration
         path("patient/registration",views.registration,name='registration'),
          path("login/",views.loginView,name='login'),
          path("logout/",views.logoutview,name='logout'),
           path("disease/prediction/diabetes",views.predictiondiabetes,name='predictiondiabetes'),
            path("disease/prediction/heart",views.predictionheart,name='predictionheart'),
            path("disease/prediction/pneumonia",views.pneumonia,name='pneumonia'),
            path("disease/prediction/",views.prediction,name='prediction'),
            path("disease/prediction/sendSymptoms",views.sendSymptoms,name='sendSymptoms'),
            path("disease/prediction/chatbot",views.chatbot,name='chatbot'),
             path("disease/prediction/chatbotsend",views.chatbotsend,name='chatbotsend'),
            path('doctors/patients/appointment',views.doctorappointment,name='doctorappointment'),
             path('doctors/patients/slots',views.doctorappointmentdate,name='doctorappointmentdate'),
            path('doctors/chatbot/<int:id>/<int:patentid>',views.doctorchatpatient,name='doctorchatpatient'),
            path('doctors/home/<int:id>',views.doctorhome,name='doctorhome'),
            path('doctors/patients/<int:id>',views.doctorpatients,name='doctorpatients'),
            path('disease/prediction/appointment',views.chatappointment, name='chatappointment'),
            path('disease/prediction/slots',views.doctorappointmentdate, name='patientappointmentdate'),
            path('disease/prediction/chat',views.doctorchat, name='doctorchat'),
            path('disease/prediction/patientchat',views.patientchat, name='patientchat'),
            


              



      

]