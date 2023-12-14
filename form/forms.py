from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['fullname', 'course', 'study_org', 'email', 'telegram']
