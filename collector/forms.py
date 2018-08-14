from django import forms
from .models import Review, Question


class MessageForm(forms.Form):
    message = forms.CharField(required=True)

class ResponseForm(forms.Form):
    response = forms.CharField(required=True)
    response_for = forms.IntegerField(required=True)
