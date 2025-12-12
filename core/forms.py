from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ParentProfile, Enrollment


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )


class ParentProfileForm(forms.ModelForm):
    class Meta:
        model = ParentProfile
        fields = ("phone_number", "address", "occupation")


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ["child_name", "child_age", "class_group", "medical_info", "address"]
        widgets = {
            "child_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Child’s Full Name"}
            ),
            "child_age": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "placeholder": "Age in years"}
            ),
            "class_group": forms.Select(attrs={"class": "form-control"}),
            "medical_info": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Allergies or medical notes",
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Home Address",
                }
            ),
        }


class ParentLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
