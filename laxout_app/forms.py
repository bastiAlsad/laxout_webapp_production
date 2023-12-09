from django import forms
from .models import LaxoutUser

class UserForm(forms.ModelForm):
    class Meta:
        model = LaxoutUser
        fields = ["laxout_user_name", "note"] # not  fields = ["laxout_user_name, note"] !


