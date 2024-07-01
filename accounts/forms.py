from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validator

from django import forms
from django.core.exceptions import ValidationError

class UserForm(forms.Form):
    # Your form fields here
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@gmail.com'):
            raise ValidationError('Please use a valid Gmail address.')
        return email

# creating Userform structure
class UserForm(forms.ModelForm):
    # For user registration form we are user User class as referance.
    password         = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','phone_no',]
    def clean(self):
        cleaned_data = super(UserForm,self).clean()
        password = cleaned_data.get('password')
        confirm_passwod = cleaned_data.get('confirm_password')
        
        if password != confirm_passwod:
            raise forms.ValidationError("password doesn't match")
         
        
class Userprofileform(forms.ModelForm):
    # we are setting the styles for the below 3 fields fromfront end side.
   address          = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Start typing...","requited":"required"}))
   profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}),validators=[allow_only_images_validator])
   cover_photo     = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator])
   class Meta:
        model = UserProfile
        fields = ['profile_picture','cover_photo','address','state','country','city','pin_code','langitude','lattitude']    
 
   # The below function is for to make the langitude and latittude both as read only fields.      
   def __init__(self, *args, **kwargs):
       super(Userprofileform, self).__init__(*args, **kwargs)
       for field in self.fields:
        if field == 'langitude' or field == 'lattitude':
            self.fields[field].widget.attrs['readonly'] = 'readonly'
            
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','phone_no']
    
