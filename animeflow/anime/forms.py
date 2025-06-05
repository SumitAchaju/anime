from django import forms
from .models import AnimeComments


class AnimeCommentForm(forms.ModelForm):
    class Meta:
        model = AnimeComments
        fields = ["comment", "user", "anime"]
