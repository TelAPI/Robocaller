from django import forms


class RobocallerForm(forms.Form):
    numbers_to_call = forms.FileField()
    audio_message = forms.URLField(required=False, help_text="URL to an audio file, such as an MP3")
    say_message = forms.CharField(required=False, help_text="A text message, that will be translated into an audio message")

