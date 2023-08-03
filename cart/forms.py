from django import forms

from .models import Customer, ShippingAddress


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'email',
            "company_name",
            "country",
            "address"
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', "placeholder": "First name"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', "placeholder": "Last name"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', "placeholder": "Email"}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', "placeholder": "Company name"}),
            'address': forms.TextInput(attrs={'class': 'form-control', "placeholder": "Address"}),
            'country': forms.Select(attrs={'class': 'w-100', "placeholder": "Country"}),
        }



class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            "town",
            "zip_code",
            "phone_number",
            "comment"
        ]
        widgets = {
            'town': forms.TextInput(attrs={'class': 'form-control', "placeholder": "Town"}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', "placeholder": "Zip_code"}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', "placeholder": "Phone_number"}),
            'comment': forms.Textarea(attrs={'class': 'form-control', "placeholder": "Comment"}),
        }