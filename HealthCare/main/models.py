
from email.policy import default
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from waitress import profile

 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname=models.CharField(max_length=30)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone= models.CharField(validators=[phone_regex], max_length=17, blank=True)
   
    def __str__(self):
        return self.user.username
    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
    


    

class DiseasesModel(models.Model):
    name=models.CharField(max_length=20)
    definition=models.CharField(  max_length=700)
    causes=models.CharField(  max_length=700)
    treatments=models.CharField(  max_length=700)
    preventions=models.CharField(  max_length=700,default='')
    
class MedicineModel(models.Model):
    name=models.CharField(max_length=20)
    definition=models.CharField(  max_length=700)
    disease=models.ForeignKey(DiseasesModel,on_delete=models.CASCADE,default='')
    warnings=models.CharField(  max_length=700)
    prescription=models.CharField(  max_length=700)
    effects=models.CharField( max_length=700)

class DoctorModel(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE,default='')
    image=models.ImageField(upload_to='images/')
    specialty=models.CharField(max_length=20,default='')
    
class PatientsModel(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    image= models.FileField(upload_to='images/')
    age=models.IntegerField(default=0)
    address=models.CharField(default='',max_length=30)
    doctor=models.ForeignKey(DoctorModel,on_delete=models.CASCADE)
    weight=models.DecimalField(decimal_places=2,max_digits=5,default=0.0)

class HistoryModel(models.Model):
    patient=models.ForeignKey(PatientsModel,on_delete=models.CASCADE)
    disease=models.ForeignKey(DiseasesModel,on_delete=models.CASCADE)
    medicine=models.ForeignKey(MedicineModel,on_delete=models.CASCADE)
    date=models.DateField(blank=True)


    

class PneumoniaCancerModel(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class AppointmentsModel(models.Model):
    patient=models.ForeignKey(PatientsModel,on_delete=models.CASCADE)
    disease=models.CharField(max_length=20)
    age=models.CharField(max_length=20)
    date=models.DateField(blank=True)
    slot=models.CharField(max_length=20)
   


class Discussion(models.Model):
    patient=models.ForeignKey(PatientsModel,on_delete=models.CASCADE,default='')
    doctor=models.ForeignKey(DoctorModel,on_delete=models.CASCADE,default='')
    message=models.CharField(max_length=30)
    time=models.CharField(max_length=10)


 