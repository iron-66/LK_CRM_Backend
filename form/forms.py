from django import forms
from .models import TestResult


class TestResultForm(forms.ModelForm):
    class Meta:
        model = TestResult
        fields = ['telegram_id', 'task1', 'task2', 'task3', 'task4', 'task5']
