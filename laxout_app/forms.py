from django import forms
from .models import LaxoutUser, Uebungen_Models
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

class UserForm(forms.ModelForm):
    befund = forms.BooleanField(required=False, initial=False)
    class Meta:
        model = LaxoutUser
        fields = ["laxout_user_name", "email_adress", "befund", ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Crispy Forms Helper definieren
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('laxout_user_name', placeholder='Benutzername des Patienten'),
            Field('email_adress', placeholder='E-Mail Adresse des Patienten'),
            Field('befund', id='id_custom_befund', name='Möchten Sie mit einem Befund starten?'),
            # Hier kannst du weitere Felder hinzufügen oder anpassen
        )


 # not  fields = ["laxout_user_name, note"] !


class User(forms.ModelForm):
    model = User
    fields = ["username", "password"]

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Uebungen_Models
        fields = ["execution", "name", "dauer", "videoPath", "looping", "timer", "required", "imagePath", "onlineVideoPath", ]

class TrainingDataForm(forms.Form):
    illness = forms.CharField(max_length=100, required=True)
    
