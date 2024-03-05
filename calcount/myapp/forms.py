from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *




class register_form(UserCreationForm):
    
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        
class login_form(forms.Form):
    username=forms.CharField(label='your username', widget=forms.TextInput(attrs={'class':'form-controler'}))
    password=forms.CharField(label='Enter Password', widget=forms.PasswordInput(attrs={'class':'form-controler'}))
    
    class Meta:
        model=User
        fields=['username','password']
        
        
class userprofile_form(forms.ModelForm):
    
    
    class Meta:
        model=user_profile
        fields=('__all__')
        exclude=['user']


class DailyConsumedCaloriesForm(forms.ModelForm):
    date_consumed = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Select the date when the calories were consumed'
    )

    class Meta:
        model = ConsumedCalories
        fields = ['item_name', 'calories_consumed',]

        widgets = {
            'item_name': forms.TextInput(attrs={'placeholder': 'Enter item name'}),
            'calories_consumed': forms.NumberInput(attrs={'placeholder': 'Enter calories consumed'}),
        }