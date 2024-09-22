from django import forms
from .models import Comment
from .models import Post
from taggit.forms import TagField

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class PostForm(forms.ModelForm):
    tags = TagField()  # Add this field for tags

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
