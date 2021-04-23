from django import forms
from .models import Comment
from mptt.forms import TreeNodeChoiceField


class CommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update({
            'class': 'd-none'
        })
        self.fields['parent'].label = ""
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ("post", "parent", "content",)
        widgets = {
            "content": forms.Textarea(attrs={"class": 'form-control ml-5 mb-3 pl-3 border-1 comment-add rounded required', 'rows': '1', 'placeholder': 'Add a public comment'})
        }