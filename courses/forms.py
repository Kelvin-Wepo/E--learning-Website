from django import forms
from django.forms.models import inlineformset_factory
from courses.models import Course, Module, Review, Subject, Content
from students.models import (
    User, Profile
)

class ModuleForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'cols': 40, 'rows': 8}))

    class Meta:
        model = Module
        exclude = ()

ModuleFormSet = inlineformset_factory(Course, Module, form=ModuleForm, fields=['title', 'description',], extra=2, can_delete=True)


