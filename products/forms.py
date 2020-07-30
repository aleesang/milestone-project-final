from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    """
    a simple comment form that only asks the user to input their text
    other comment information will be pulled from elsewhere
    """
    class Meta:
        model = Comment
        fields = ['body']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'