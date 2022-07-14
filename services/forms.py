from .models import *
from django import forms

class WorkCreateForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ("title","description","deadline","assigned_to")
class ProgressUpdateForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ('reference',)