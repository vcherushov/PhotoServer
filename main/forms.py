from django import forms
from .models import *
import django_filters


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'






class AddPostForm(forms.ModelForm):

    class Meta:
        model = TrackCar
        fields = ['time_create', 'time_time']
        widgets = {
            'time_create': DateInput(),
            'time_time': TimeInput(format='%H:%M')
        }


class DownloadForm(forms.ModelForm):
    class Meta:
        model = Download
        fields = ['day_start', "day_end", 'time_start']
        widgets = {
            'day_start': DateInput(),
            'day_end': DateInput(),
            'time_start': TimeInput(format='%H:%M'),
        }




