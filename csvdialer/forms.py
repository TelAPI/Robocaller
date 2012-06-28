from django import forms


class RobocallerForm(forms.Form):
    numbers_to_call = forms.FileField()
    message = forms.URLField(required=False)
    say_message = forms.CharField(required=False)

