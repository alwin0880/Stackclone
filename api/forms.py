from django import forms
from api.models import MyUser,Questions
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control border border-info'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control border border-info'}))
    class Meta:                                                   #password1 and password2 models-nne varanna field alla user creation-lle field anne,so widget-nte ullil style cheyan pattila
        model=MyUser
        fields=['first_name','last_name','username','email',
        'phone','profile_pic','password1','password2']
        widgets={
            "first_name":forms.TextInput(attrs={'class':'form-control border border-info'}),
            "last_name":forms.TextInput(attrs={'class':'form-control border border-info'}),
            "username":forms.TextInput(attrs={'class':'form-control border border-info'}),
            "email":forms.EmailInput(attrs={'class':'form-control border border-info'}),
            "phone":forms.NumberInput(attrs={'class':'form-control border border-info'}),
            "profile_pic":forms.FileInput(attrs={'class':'form-select form-control border border-info'})

        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control border border-dark"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control border border-info"}))

# <p class="text-decoration-underline">This text has a line underneath it.</p>

class QuestionForm(forms.ModelForm):

    class Meta:
        model=Questions
        fields='description','image'
        widgets={
            'description':forms.Textarea(attrs={'class':'form-control border-dark','rows':3}),
            'image':forms.FileInput(attrs={'class':'form-select form-control border-dark'})
        }

     

class AnswerForm(forms.Form):
    answer=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))