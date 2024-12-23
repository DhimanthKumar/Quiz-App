from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory
from .models import Quiz,questions,options,userquizdata
class basicquizdetails(forms.Form):
    name = forms.CharField(max_length=200)
    maxtime=forms.IntegerField()
    numquestions=forms.IntegerField()
class QuestionForm(forms.ModelForm):
    class Meta:
        model = questions
        fields = ['question',  'answer']
    
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        from django.contrib.auth.models import User
        model=User
        fields=['username', 'email', 'password1', 'password2']
class optionform(forms.ModelForm):
    class Meta:
        model = options
        fields=fields = ['option',]
OptionFormSet = modelformset_factory(options, form=optionform, extra=4)
class userquizform(forms.ModelForm):
    class Meta:
        model = userquizdata
        fields=['choice',]
userquizformset=modelformset_factory(userquizdata , form=userquizform , extra=5 )