from django import forms
from .models import Post,Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
        labels = {
            "user_name": "Your Name",
            "user_email": "Your Email",
            "text": "Post Comment"
        }

        error_messages = {
            "user_name": {
                "required": "This field is required",
                "max_length": "This should not be longer length 50 words"
            }
            
        }

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
