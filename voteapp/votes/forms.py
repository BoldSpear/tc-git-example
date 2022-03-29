from django import forms
from .models import Vote, Topic


class PollCreateForm(forms.Form):
    topic = forms.CharField(label='poll topic', min_length='2', max_length='100')
    options = forms.CharField(label='option for poll selection', min_length=2, max_length=300)


class PollUpdateForm(forms.ModelForm):
    options = forms.CharField(label = 'vote choice option', min_length=2, max_length=300)

    class Meta:
        model = Topic
        fields = ['title']
        labels = {
            'title': '제목'
        }

class VoteForm(forms.ModelForm):
    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=forms.HiddenInput())
    class Meta:
        model = Vote
        fields = ['topic', 'option']
        labels = {
            'option': '선택지'
        }
