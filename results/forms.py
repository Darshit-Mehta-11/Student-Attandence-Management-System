from django import forms

class SemesterSelectForm(forms.Form):
    sem = forms.ChoiceField(
        choices=[("","Select Semester")]+[(i,f"Semester {i}")for i in range(1, 7)],
        label = "Select Semester",
        
        widget=forms.Select(attrs={
            'class': 'sem',
        })  
        
    )