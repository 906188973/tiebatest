from django import forms
from .models import Topic, poster, Poster_reply
from django.core.exceptions import ValidationError

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text_topic']
        labels = {'text_topic': ''}

class PosterForm(forms.ModelForm):
    class Meta:
        model = poster
        fields = ['text_poster']
        labels = {'text_poster': ''}
        widgets = {'text_poster': forms.Textarea(attrs={'cols': 80})}

class PosterReplyForm(forms.Form):
    text = forms.CharField()