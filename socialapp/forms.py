from django import forms
from .models import Tweet

class TweetForm(forms.ModelForm):
    body = forms.CharField(required=True,
                            widget=forms.widgets.Textarea(attrs={
                            "placeholder": "Whats on your mind?",
                            "class":"form-control",                                  
                            }
                            ),
                            label="",
                        )
    class Meta:
        model = Tweet
        fields = '__all__'
        exclude = ("user",)