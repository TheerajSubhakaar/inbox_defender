# classifier/forms.py

from django import forms

class TextInputForm(forms.Form):
    message = forms.CharField(label='Enter message', max_length=500, widget=forms.Textarea)
