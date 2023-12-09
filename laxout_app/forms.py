from django import forms
from .models import LaxoutUser, Physio

class UserForm(forms.ModelForm):
    class Meta:
        model = LaxoutUser
        fields = ["laxout_user_name", "note"] # not  fields = ["laxout_user_name, note"] !


class User(forms.ModelForm):
    model = Physio
    fields = ["username", "password"]