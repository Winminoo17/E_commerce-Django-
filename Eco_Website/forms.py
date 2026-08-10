from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms 
from .models import Profile


class PasswordChangeForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ('new_password1', 'new_password2', 'current_password')
        
        widgets = {
            'new_password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
            'current_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'})
        }
        
        labels = {
            'new_password1': '',
            'new_password2': '',
            'current_password': ''
        }
        
        help_texts = {
            'new_password1': '<span class="form-text text-muted">Your New Password</span>',
            'new_password2': '<span class="form-text text-muted">Your New Password Must Match</span>',
            'current_password': '<span class="form-text text-muted">Your Current Password</span>'
        }
        
class UpdateUserForm(UserChangeForm):
    password = None
    email = forms.EmailField(
        label="", 
        max_length=100, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted">Your Name</span>'
        

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="", 
        max_length=100, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted">Your Name</span>'
        
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<span class="form-text text-muted">Your Password</span>'
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted">Your Password Must Match</span>'

class UserInfoFrom(forms.ModelForm):
    phone = forms.CharField()
    address1 = forms.CharField()
    address2 = forms.CharField()
    state = forms.CharField()
    city = forms.CharField()
    zipcode = forms.CharField()
    country = forms.CharField()
    
    class Meta:
        model = Profile
        fields = ('phone', 'address1', 'address2', 'state', 'city', 'zipcode', 'country')
        
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 1'}),
            'address2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 2'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'})
        }
        
        