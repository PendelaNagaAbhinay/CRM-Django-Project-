from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer, Order, Product
from django.core.exceptions import ValidationError
import re


# Registration Form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists. Please choose another.")

        if len(username) < 8:
            raise ValidationError("Username must be at least 8 characters long.")

        if not re.match(r'^[a-zA-Z]+$', username):
            raise ValidationError("Username must contain only letters.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email.endswith('@gmail.com'):
            raise ValidationError("Please use a valid Gmail address.")

        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")

        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character.")
        return password


# Login Form
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']  # Include the fields you want for registration


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['order_date']  # Exclude 'order_date' since it is auto-generated


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['order_name', 'status', 'description']  # Include the fields you want to display in the form
