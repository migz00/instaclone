from django import forms
from .models import Post, Comment

class NewPost(forms.ModelForm):
    picture = forms.ImageField(required=True)
    caption = forms.CharField(widget=forms.Textarea(), required=True)

    class Meta:
        model = Post
        fields = ('picture', 'caption')

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class':"form-control", 'rows':"3", 'placeholder':"Add a comment..."}), required=True)

    class Meta:
        model = Comment
        fields = ('body',)