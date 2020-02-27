from django.forms import CharField, TextInput
from django.forms import ModelForm
from .models import Comment


class CommentForm(ModelForm):
    content = CharField(widget=TextInput(attrs={'placeholder': 'Write a comment here...'}))

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = ""

    class Meta:
        model = Comment
        fields = ('content',)
