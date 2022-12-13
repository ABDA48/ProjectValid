from dataclasses import fields
from distutils.command.upload import upload
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError  
from django import forms
from .models import PatientsModel,MedicineModel,DiseasesModel,DoctorModel,Profile,PneumoniaCancerModel,AppointmentsModel
class PatientForm(forms.ModelForm):
    class Meta:
        model=PatientsModel
        fields=['profile','image','age','address','doctor','weight']

class MedicineForm(forms.ModelForm):
    class Meta:
        model=MedicineModel
        fields=['name','definition','disease','warnings','prescription','effects']
        widgets={
            'definition':forms.Textarea(attrs={'class':'form-control'}),
            'warnings':forms.Textarea(attrs={'class':'form-control'}),
            'prescription':forms.Textarea(attrs={'class':'form-control'}),
            'effects':forms.Textarea(attrs={'class':'form-control'}),
        }

class DoctorForm(forms.ModelForm):
    class Meta:
        model=DoctorModel
        fields=['profile','specialty','image']
class DiseasesForm(forms.ModelForm):
    class Meta:
        model=DiseasesModel
        fields=['name','definition','causes','treatments','preventions']
        widgets={
            'definition':forms.Textarea(attrs={'class':'form-control'}),
            'causes':forms.Textarea(attrs={'class':'form-control'}),
            'prescription':forms.Textarea(attrs={'class':'form-control'}),
            'treatments':forms.Textarea(attrs={'class':'form-control'}),
            'preventions':forms.Textarea(attrs={'class':'form-control'}),
        }
class loginForm(forms.Form):
    username = forms.CharField(label='username',widget=forms.TextInput(attrs={'placeholder':'Enter username'}), min_length=5, max_length=150) 
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder':'Enter password'}),)  

class RegistrationForm(UserCreationForm):
    fullname=forms.CharField(label='Full name', min_length=5, max_length=150)
    username = forms.CharField(label='username', min_length=5, max_length=150)  
    email = forms.EmailField(label='email')  
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone= forms.CharField(validators=[phone_regex], max_length=17)
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput) 
    
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            print("Password don't match")
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1'],
            


        )  
        return user  


class PneumoniaForm(forms.ModelForm):
    class Meta:
        model = PneumoniaCancerModel
        fields = ('description', 'document', )

class AppointmentsForm(forms.ModelForm):
    class Meta:
        model=AppointmentsModel
        fields=['patient','disease','age','date','slot']
        widgets={
         "date":forms.DateInput(attrs={"class":"form-control","type":"date","id":"date"}),
          "patient":forms.Select(attrs={"class":"form-control"}),
          "disease":forms.TextInput(attrs={"class":"form-control"}),
          "age":forms.TextInput(attrs={"class":"form-control"}),

        }