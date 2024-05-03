from django import forms
# from django_quill.fields import QuillField  # quill text editor
from blog.models import Post


class NewPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'details'

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'summary',
            'category',
        ]
