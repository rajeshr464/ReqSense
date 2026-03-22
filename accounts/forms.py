from django import forms
from .models import User
from django.utils.safestring import mark_safe
from django.urls import reverse

class UserRegisterForm(forms.ModelForm):
    name = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['name', 'email']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            login_url = reverse('accounts:login')
            raise forms.ValidationError(mark_safe(f"Email already registered. Try to <a href='{login_url}' class='text-primary hover:underline font-bold'>Login here</a>."))
        return email
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('email', '')
        
        name_parts = self.cleaned_data.get('name', '').split(' ', 1)
        user.first_name = name_parts[0]
        if len(name_parts) > 1:
            user.last_name = name_parts[1]
            
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
