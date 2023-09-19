from django import forms
from .models import Tweet, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Profile Extras form
class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture")
    profile_bio = forms.CharField(label="Profile Bio", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Profile Bio'}))
    website_link = forms.CharField(label= "Website Link",widget=forms.TextInput(attrs={'class':'forms-control', 'placeholder': 'Website'}))
    facebook_link = forms.CharField(label= "Facebook Link",widget=forms.TextInput(attrs={'class':'forms-control', 'placeholder': 'Facebook'}))
    instagram_link = forms.CharField(label= "Instagram Link",widget=forms.TextInput(attrs={'class':'forms-control', 'placeholder': 'Instagram'}))
    linkedin_link = forms.CharField(label= "Linkedin Link",widget=forms.TextInput(attrs={'class':'forms-control', 'placeholder': 'Linkedin'}))
    
    class Meta:
        model = Profile
        fields = ('profile_image','profile_bio','website_link','facebook_link','instagram_link','linkedin_link',)


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
        exclude = ("user","likes")

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="",widget=forms.TextInput
                             (attrs={'class':'forms-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput
                             (attrs={'class':'forms-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput
                             (attrs={'class':'forms-control', 'placeholder': 'Last Name'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'