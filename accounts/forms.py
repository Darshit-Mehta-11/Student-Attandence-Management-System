from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    # include explicit choice for role, default student
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, initial='student',
                             widget=forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}))
    # rollno will be auto-generated; do not expose on registration

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'password1': forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'password2': forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data.get('role', 'student')
        # staff status and active state handled in view
        if commit:
            user.save()
        return user


# keep teacher form for backwards compatibility if needed, but re-use registration form
class TeacherRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        pass
