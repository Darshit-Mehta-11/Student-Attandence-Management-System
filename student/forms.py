from django import forms
from teachers.models import LeaveRequest

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['date', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'input-field'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'input-field'}),
        }
