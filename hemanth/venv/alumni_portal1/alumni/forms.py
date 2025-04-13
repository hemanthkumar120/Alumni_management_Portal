from django import forms
from django.contrib.auth.models import User
from .models import Alumni

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

class AlumniForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = ['graduation_year', 'course', 'job_title', 'location', 'bio', 'profile_picture']
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']
from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
