from django import forms
from django.forms import Textarea

class NewPostForm(forms.Form):
    Post_content = forms.CharField(widget= forms.Textarea(attrs={'rows':3,'cols': 40}), max_length= 200,label="Post Content")
